'''
Created on Oct 1, 2012

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

class HttpObjectService(ObjectService, restObject):
    
    def __init__(self):
        pass
    
    