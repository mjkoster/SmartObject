'''
restObject 

Based on the restdata module from restlite, the Request method sequences
the URL path by resource and authenticates at each level. The bind method walks 
the SmartObject directory structures according to the path segments
(FIXME add semantic method based on structural triples?)
'''

import sys, json, base64, hashlib
import restlite

def hash(user, realm, password):
    '''MD5(user:realm:password) is used for storing user's encrypted password.'''
    return hashlib.md5('%s:%s:%s'%(user, realm, password)).hexdigest()

class Request(object):
    def __init__(self, env, start_response):
        self.env, self.start_response = env, start_response
        self.method = env['REQUEST_METHOD']
        self.pathItems = [x for x in env['PATH_INFO'].split('/') if x != '']
        self.user, self.access = None, 'drwxr-xr-x'
        
    def nextItem(self):
        if self.pathItems:
            item, self.pathItems = self.pathItems[0], self.pathItems[1:]
        else:
            item = None
        return item
        
    # returns (user, None) or (None, '401 Unauthorized')
    def getAuthUser(self, users, realm, addIfMissing=False):
        hdr = self.env.get('HTTP_AUTHORIZATION', None)
        if not hdr: 
            return (None, '401 Missing Authorization')
        authMethod, value = map(str.strip, hdr.split(' ', 1))
        if authMethod != 'Basic': 
            return (None, '401 Unsupported Auth Method %s'%(authMethod,))
        user, password = base64.b64decode(value).split(':', 1)
        hash_recv = hash(user, realm, password)
        if user not in users: 
            if addIfMissing: 
                users[user] = hash_recv
                return (user, '200 OK')
            else:
                return (user, '404 User Not Found')
        if hash_recv != users[user]: 
            return (user, '401 Not Authorized')
        return (user, '200 OK')
        
    # throw the 401 response with appropriate header
    def unauthorized(self, realm, reason='401 Unauthorized'):
        self.start_response(reason, [('WWW-Authenticate', 'Basic realm="%s"'%(realm,))])
        raise restlite.Status, reason
    
    def getBody(self):
        try: 
            self.env['BODY'] = self.env['wsgi.input'].read(int(self.env['CONTENT_LENGTH']))
        except (TypeError, ValueError): 
            raise restlite.Status, '400 Invalid Content-Length'
        if self.env['CONTENT_TYPE'].lower() == 'application/json' and self.env['BODY']: 
            try: 
                self.env['BODY'] = json.loads(self.env['BODY'])
            except: 
                raise restlite.Status, '400 Invalid JSON content'
        return self.env['BODY']
    
    def verifyAccess(self, user, type, obj):
        if not obj: 
            raise restlite.Status, '404 Not Found'
        if '_access' in obj: 
            self.access = obj['_access']
        if '_owner' in obj:
            self.user = obj['_owner']
        index = {'r': 1, 'w': 2, 'x': 3}[type]
        if not (user == self.user and self.access[index] != '-' \
                or user != self.user and self.access[6+index] != '-'):
            raise restlite.Status, '403 Forbidden'
    
    def represent(self, obj):
        prefix = self.env['SCRIPT_NAME'] + self.env['PATH_INFO']
        if isinstance(obj, list):
            result = [(':id', '%s/%d'%(prefix, i,)) if isinstance(v, dict) and '_access' in v else self.represent(v) for i, v in enumerate(obj)]
        elif isinstance(obj, dict):
            result = tuple([('%s:id'%(k,), '%s/%s'%(prefix, k)) if isinstance(v, dict) and '_access' in v else (k, self.represent(v)) for k, v in obj.iteritems() if not k.startswith('_')])
        else:
            result = obj
        return result
        
class RestObject(object):
    def __init__(self, objDict, users):
        self.objDict, self.users, self.realm = objDict, users, 'localhost'
        
    def traverse(self, objDict, item):
        if isinstance(objDict, dict): return objDict[item]
        elif isinstance(objDict, list): 
            try: index = int(item)
            except: raise restlite.Status, '400 Bad Request'
            if index < 0 or index >= len(objDict): raise restlite.Status, '400 Bad Request'
            return objDict[index]
        elif hasattr(objDict, item): return objDict.__dict__[item]
        else: return None
        
    def handler(self, env, start_response):               
        print 'restdata.handler()', env['SCRIPT_NAME'], env['PATH_INFO']
        request = Request(env, start_response)
        user, reason = request.getAuthUser(self.users, self.realm, addIfMissing=True)
        if not user or not reason.startswith('200'): 
            return request.unauthorized(self.realm, reason)
        current = self.data
        while len(request.pathItems) > 1:
            item = request.nextItem()
            request.verifyAccess(user, 'x', current)
            current = self.traverse(current, item)
        item = request.nextItem()
        
        if request.method == 'POST':
            if item:
                request.verifyAccess(user, 'x', current)
                current = self.traverse(current, item)
            if not isinstance(current, list): 
                raise restlite.Status, '405 Method Not Allowed'
            value = request.getBody()
            current += value
        elif request.method == 'PUT':
            value = request.getBody()
            request.verifyAccess(user, 'w', current)
            if isinstance(current, dict): 
                current[item] = value
            elif isinstance(current, list): 
                try: index = int(item)
                except: raise restlite.Status, '400 Bad Request'
                if index < 0: current.insert(0, value)
                elif index >= len(current): current.append(value)
                else: current[index] = value
            else: 
                current.__dict__[item] = value
        elif request.method == 'DELETE':
            request.verifyAccess(user, 'w', current)
            if isinstance(current, dict): 
                del current[item]
            elif isinstance(current, list): 
                try: index = int(item)
                except: raise restlite.Status, '400 Bad Request'
                if index < 0 or index >= len(current): raise restlite.Status, '400 Bad Request'
                else: del current[index]
            elif hasattr(current, item): 
                del current.__dict__[item]
        elif request.method == 'GET':
            if item:
                request.verifyAccess(user, 'x', current)
                current = self.traverse(current, item)
            request.verifyAccess(user, 'r', current)
            result = request.represent(current)
            type, value = restlite.represent(result, type=env.get('ACCEPT', 'application/json'))
            start_response('200 OK', [('Content-Type', type)])
            return [value]
        else: raise restlite.Status, '501 Method Not Implemented'

def bind(objDict, users=None):
    '''The bind method to bind the returned wsgi application to the supplied data and users.
    @param data the original Python data structure which is used and updated as needed.
    @param users the optional users dictionary. If missing, it disables access control.
    @return:  the wsgi application that can be used with restlite.
    '''
    restObject = RestObject(objDict, users)
    def handler(env, start_response):
        return restObject.handler(env, start_response)
    return handler
