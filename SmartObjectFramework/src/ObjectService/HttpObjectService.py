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
        self.env, self.start_response = env, start_response
        restObject.Request.__init__(self.env, self.start_response)
        

class RestObject(restObject.RestObject):
    def __init__(self, objDict, users):
        RestObject.__init__(objDict, users)
        
        
    def _handleGET(self, currentResource):
        restObject.RestObject._handleGET(self, currentResource) # default GET
    
    def _handlePUT(self, currentResource):
        restObject.RestObject._handlePUT(self, currentResource) # default PUT
    
    def _handlePOST(self, currentResource):
        restObject.RestObject._handlePOST(self, currentResource) # default POST
    
    def _handleDELETE(self, currentResource):
        restObject.RestObject._handleDELETE(self, currentResource) # default DELETE


class HttpObjectService(ObjectService):
    
    def __init__(self):
        objectHandler = restObject.bind(ObjectService.__init__(self), users=None) 
        #bind to root resource dictionary returned by ObjectService constructor  
        #bind returns the RestObject handler which uses the Request object
        # the handler calls the overriding _handleXX methods in this module
        routes = [(r'GET,PUT,POST,DELETE /.*',objectHandler() )]
        return routes
                  
        
if __name__ == '__main__' :
    import sys
    from wsgiref.simple_server import make_server
    # HttpObjectService constructor method creates a Smart Object service and 
    # returns a constructor for a restlite router instance
    routes = HttpObjectService()
    httpd = make_server('', 8000, restlite.router(routes))
    try: httpd.serve_forever()
    except KeyboardInterrupt: pass
    
    