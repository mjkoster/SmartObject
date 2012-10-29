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
from restlite import restlite
import threading
from time import sleep


class GatewayObjectService(object):
    
    def __init__(self):
        self.objectService = ObjectService()
        import __builtin__
        __builtin__.SmartObjectSevice = self.objectService # set global reference to the service
        
    def _startHttpObjectService(self):
        from wsgiref.simple_server import make_server
        # HttpObjectService constructor method creates a Smart Object service and 
        # returns a constructor for a restlite router instance
        self.httpObjectService = HttpObjectService(self.objectService)
        self.httpd = make_server('', 8000, restlite.router(self.httpObjectService.routes))
        try: self.httpd.serve_forever()
        except KeyboardInterrupt: pass
    
    def _startCoapObjectService(self):
        # Use similar pattern for CoAP service, emulate with another http server for now
        from wsgiref.simple_server import make_server
        # coapObjectServices = CoapObjectService(self.objectService)
        # self.coapd = make_server('', 61616, restlite.router(coapObjectService.routes))
        self.coapObjectService = HttpObjectService(self.objectService)
        self.coapd = make_server('', 8001, restlite.router(self.coapObjectService.routes))
        try: self.coapd.serve_forever()
        except KeyboardInterrupt: pass
        
            
if __name__ == '__main__' :
    
    gateway = GatewayObjectService() # make an instance of the gateway and start a thread for each service interface  
    print 'Gateway started'
    
    httpThread = threading.Thread(target = gateway._startHttpObjectService)
    httpThread.daemon = True
    httpThread.start()
    print 'httpd started'

    coapThread = threading.Thread(target = gateway._startCoapObjectService)
    coapThread.daemon = True
    coapThread.start()
    print 'coapd started'

    # start agents here
    try:
        # register handlers etc.
        while 1: sleep(1)
    except KeyboardInterrupt: pass
    print 'got KeyboardInterrupt'
    
