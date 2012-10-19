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

class HttpObjectService(ObjectService):
    
    def __init__(self):
        objectHandler = restObject.bind(ObjectService.__init__(self), users=None) 
        #bind to root resource dictionary returned by ObjectService init method  
        restlite.routes = [('rGET,PUT,POST,DELETE /.*',objectHandler() )]
                  
        
    
    
    