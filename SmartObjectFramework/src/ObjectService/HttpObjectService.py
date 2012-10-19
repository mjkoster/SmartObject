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

class Request(restObject.Request):
    def __init__(self, env, start_response):
        restObject.Request.__init__(env, start_response)
        

class RestObject(restObject.RestObject):
    def __init__(self, objDict, users):
        RestObject.__init__(objDict, users)
        
        
    def _handleGET(self, currentResource):
        restObject.RestObject._handleGET(self, currentResource)
    
    def _handlePUT(self, currentResource):
        pass
    
    def _handlePOST(self, currentResource):
        pass
    
    def _handleDELETE(self, currentResource):
        pass
    
    

class HttpObjectService(ObjectService):
    
    def __init__(self):
        objectHandler = restObject.bind(ObjectService.__init__(self), users=None) 
        #bind to root resource dictionary returned by ObjectService init method  
        #bind returns the RestObject handler which uses the Request object
        # the handler calls the overriding _handleXX methods in this module
        
        restlite.routes = [('rGET,PUT,POST,DELETE /.*',objectHandler() )]
                  
        
    
    
    