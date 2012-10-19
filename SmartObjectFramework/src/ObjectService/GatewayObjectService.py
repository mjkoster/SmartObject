'''
Created on Oct 1, 2012

GatewayObjectService is an ObjectService with two interfaces, an http web interface
and a coap constrained network interface, constructed of the two interface services 
referencing a common ObjectService

@author: mjkoster
'''

from HttpObjectService import HttpObjectService
from CoapObjectService import CoapObjectService
from ObjectService import ObjectService

class GatewayObjectService(HttpObjectService, CoapObjectService):
    
    def __init__(self):
        HttpObjectService.__init__(self)
        CoapObjectService.__init__(self)
    
    