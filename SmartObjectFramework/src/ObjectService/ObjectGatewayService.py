'''
Created on Oct 1, 2012

ObjectGatewayService is an ObjectService with two interfaces, an http web interface
and a coap constrained network interface

@author: mjkoster

'''
from httpInterface import httpInterface
from coapInterface import coapInterface
from ObjectService import ObjectService

class ObjectGatewayService(ObjectService, httpInterface, coapInterface):
    
    def __init__(self):
        pass
    