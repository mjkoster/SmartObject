'''
Created on Sep 15, 2012

Observers class for observation of changes in a resource

Updated July 28, 2013 MJK - made a simple http ObserverPublisher prototype

To use the observer, create a resource endpoint using http PUT, http POST or the Python API,
consisting of a URL string in the Observers resource. For example:

PUT /.../resource/Observer "http://<server>/<path>" 

creates an http publisher that updates the endpoint at the specified URL with a JSON object 
representing the value of the Observable Property whenever the Observable Property is updated

It doesn't work if you try to directly update the Property Of Interest

http PUT of JSON is all that is implemented for now

This should be replaced with a graph based observer endpoint to provide configurable protocols, 
filters, and other scalable features

Handler observers are created using a URI of the form 'callback://local/<path_to_handler>
this creates a callback object that has a reference to the handler

@author: mjkoster
'''
from RESTfulResource import RESTfulResource
from urlparse import urlparse
import json
import httplib

class Observer(RESTfulResource):
    def __init__(self, parentObject=None):
        RESTfulResource.__init__(self, parentObject)

    
class httpHandler(object):
    def __init__(self, targetURI=None):
        self.targetURI = targetURI
        self.uriObject = urlparse(targetURI)
        self.httpServer = self.uriObject.netloc
        self.httpPath = self.uriObject.path
        
    def notify(self,resource): # JSON only for now
        self.jsonObject = json.dumps(resource.get())
        self.httpHeader = {"Content-Type" : "application/json" }
        self.httpConnection = httplib.HTTPConnection(self.httpServer)
        self.httpConnection.request('PUT', self.httpPath, self.jsonObject, self.httpHeader)
        return

class coapHandler(object):
    def __init__(self, targetURI = None):
        pass
    
class mqttHandler(object):
    def __init__(self, targetURI = None):
        pass

class callbackHandler(object):
    def __init__(self, targetURI = None, linkBaseDict = None ):
        self.targetURI = targetURI
        self._linkBaseDict = linkBaseDict
        self.uriObject = urlparse(targetURI)
        self._handlerService = self.uriObject.netloc
        self._handlerPath = self.uriObject.path
        self._appHandler = self.linkToRef(self._handlerPath)
        
    def notify(self,resource=None): # invoke the handler
        self._appHandler._updateHandler(resource)
        return
    
    def linkToRef(self, linkPath ):
        '''
        takes a path string and walks the object tree from a base dictionary
        returns a ref to the resource at the path endpoint
        '''
        self._linkPath = linkPath
        self._currentDict = self._linkBaseDict
        self._pathElements = linkPath.split('/')
        for pathElement in self._pathElements[:-1] : # all but the last, which should be the endpoint
            if len(pathElement) > 0 : # first element is a zero length string for some reason
                self._currentDict = self._currentDict[pathElement].resources
        self._resource = self._currentDict[self._pathElements[-1] ]
        return self._resource
    
class Observers(RESTfulResource):
    
    def __init__(self, linkBaseDict=None):
        RESTfulResource.__init__(self)
        self.__schemes = ['http', 'coap', 'mqtt', 'callback']
        self.__observers = []
        self.__handlers = {}
        self._linkBaseDict = linkBaseDict
               
    def onUpdate(self,resource):
        self.__onUpdate(resource)
        
    def __onUpdate(self, resource):
        for observer in self.__observers:
            self.__handlers[observer].notify(resource)

    # match returns the supplied URL, else none. Supplying None returns all Observers
    def get(self, targetURI=None):
        if targetURI != None:
            if targetURI in self.__observers:
                return targetURI
            return None
        return self.__observers # if no URI specified then return all observers
        
    # map the set operation to the create operation
    def set(self, targetURI):
        self.create(targetURI)
    
    # create adds an observer to the list, echoes URI if created or exists
    def create(self, targetURI):
        self.uriObject = urlparse(targetURI)
        if self.uriObject.scheme not in self.__schemes:
            return None       
        if targetURI not in self.__observers :
            self.__observers.append(targetURI) # append to the list
                    
        if self.uriObject.scheme == 'http' :
            self.newHandler = httpHandler(targetURI)
        elif self.uriObject.scheme == 'coap' :
            self.newHandler = coapHandler(targetURI)
        elif self.uriObject.scheme == 'mqtt' :
            self.newHandler = mqttHandler(targetURI)
        elif self.uriObject.scheme == 'callback' :
            self.newHandler = callbackHandler(targetURI, self._linkBaseDict)
                    
        self.__handlers.update({targetURI : self.newHandler})
        
        return self.newHandler # return a handle to the handler object

    # delete removes an observer from the list, echoes None for failure
    def delete(self, targetURI):
        if targetURI in self.__observers :
            self.__observers.remove(targetURI)
            return targetURI
        return None
    
    