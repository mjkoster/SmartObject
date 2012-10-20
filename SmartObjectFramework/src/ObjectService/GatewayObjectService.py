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

class GatewayObjectService(object):
    
    def __init__(self):
        self.objectService = ObjectService.__init__(self)
        # objectService constructor returns ref to it's resources dictionary
    
    def _startHttpObjectService(self):
        from wsgiref.simple_server import make_server
        # HttpObjectService constructor method creates a Smart Object service and 
        # returns a constructor for a restlite router instance
        routes = HttpObjectService(self.objectService)
        self.httpd = make_server('', 8000, restlite.router(routes))
        try: self.httpd.serve_forever()
        except KeyboardInterrupt: pass
    
    def _startCoapObjectService(self):
        """
        Use similar pattern for CoAP service
        from wsgiref.simple_server import make_server
        routes = CoapObjectService(self.objectService)
        self.coapd = make_server('', 61616, restlite.router(routes))
        try: self.coapd.serve_forever()
        except KeyboardInterrupt: pass
        """
        
            
if __name__ == '__main__' :
    gateway = GatewayObjectService() # make an instance of the gateway and start threads 
    httpThread = threading.Thread(target = gateway._startHttpObjectService)
    # coapThread = threading.Thread(target = gateway._startCoapObjectService)
    httpThread.daemon = True
    httpThread.start()
    # coapThread.daemon = True
    # coapThread.start()
    
    # start agents here
    try:
        # register handlers etc.
        while 1: pass
    except KeyboardInterrupt: pass
    
    
