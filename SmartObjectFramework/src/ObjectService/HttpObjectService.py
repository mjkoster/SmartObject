'''
Created on Oct 18, 2012

Create a RESTlite instance of a http server for SmartObjects. 
based on wsgi/restlite with the restObject extensions to match object path segments 
to resource names e.g. the URL path: /object1/barometricPressure/Description/Observers 
maps to the python API identifier: object1.barometricPressure.Description.Observers

@author: mjkoster
'''

import wsgiref
import urllib
from restlite import restlite
from restlite import restObject
from ObjectService import ObjectService

# Extend restObject classes with content handlers and provide a local bind method to pick up local extensions
class Request(restObject.Request):
    def __init__(self, env, start_response):
        self.env, self.start_response = env, start_response
        restObject.Request.__init__(self.env, self.start_response)
        

class RestObject(restObject.RestObject):
    def __init__(self, objDict, users):
        restObject.RestObject.__init__(self, objDict, users)
        
        
    def _handleGET(self, currentResource):
        # if it's a Dictionary class, invoke the serializer
        if hasattr(currentResource,'serialize') : # see if the resource has a serialize method
            responseTypes = currentResource.serializeContentTypes # get the list of content types 
            responseType = self.env.get( 'ACCEPT', responseTypes[0]) # check requested type, make default type if none requested
            if responseType in responseTypes: # if requested type is in the set of types, return serialized type
                self.start_response('200 OK', [('Content-Type', responseType)]) 
                return currentResource.serialize( currentResource.get(), responseType )
        return restObject.RestObject._handleGET(self, currentResource) # default GET
    
    def _handlePUT(self, currentResource):
        if hasattr(currentResource, 'parse') :
            requestType = self.env.get('Content-Type')
            if requestType in currentResource.parseContentTypes :
                currentResource.set( currentResource.parse( self.getBody() , requestType ))
        restObject.RestObject._handlePUT(self, currentResource) # default PUT
    
    def _handlePOST(self, currentResource):
        if hasattr(currentResource, 'parse') :
            requestType = self.env.get('Content-Type')
            if requestType in currentResource.parseContentTypes :
                currentResource.create( currentResource.parse( self.getBody() , requestType ))
        restObject.RestObject._handlePOST(self, currentResource) # default POST
    
    def _handleDELETE(self, currentResource):
        restObject.RestObject._handleDELETE(self, currentResource) # default DELETE


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


class HttpObjectService(object):
    
    def __init__(self, objectService): # get a handle to the Object Service root dictionary
        self.objectService = objectService
        self.objectHandler = bind(self.objectService, users=None) 
        #bind to root resource dictionary passed to constructor  
        #bind returns the RestObject handler which uses the Request object
        # the handler calls the overriding _handleXX methods in this module
        self.routes = [(r'GET,PUT,POST,DELETE ', self.objectHandler )]
        return 
                  
# Standalone service mode
if __name__ == '__main__' :
    import sys
    from wsgiref.simple_server import make_server
    # Create a Smart Object service,, return a reference to the top level resources dict
    objectService = ObjectService()
    httpObjectService = HttpObjectService(objectService.resources)
    httpd = make_server('', 8000, restlite.router(httpObjectService.routes))
    print("Heres the server\n")
    try: httpd.serve_forever()
    except KeyboardInterrupt: 
        print("stopping\n")
        pass
    
    