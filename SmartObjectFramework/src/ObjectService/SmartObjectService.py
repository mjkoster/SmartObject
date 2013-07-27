'''
Created on JUl 25,2013

SmartObjectService is for embedding an http smart object server in a python program

@author: mjkoster
'''

from HttpObjectService import HttpObjectService
from CoapObjectService import CoapObjectService
from ObjectService import ObjectService
from restlite import restlite
import threading
from time import sleep


class SmartObjectService(object):
    
    def __init__(self, baseObject=None):
        if baseObject != None: 
            self.baseObject = baseObject
        else: 
            self.baseObject = ObjectService()
        
        import __builtin__
        __builtin__.SmartObjectSevice = self.baseObject # set global reference to the service
    
        
        
    def _startHttpObjectService(self):
        from wsgiref.simple_server import make_server
        # HttpObjectService constructor method creates a Smart Object service and 
        # returns a constructor for a restlite router instance
        self.httpObjectService = HttpObjectService(self.baseObject)
        self.httpd = make_server('', 8000, restlite.router(self.httpObjectService.routes))
        try: self.httpd.serve_forever()
        except KeyboardInterrupt: pass
    
    def _startCoapObjectService(self):
        # Use similar pattern for CoAP service, emulate with another http server for now
        from wsgiref.simple_server import make_server
        # coapObjectServices = CoapObjectService(self.objectService)
        # self.coapd = make_server('', 61616, restlite.router(coapObjectService.routes))
        self.coapObjectService = HttpObjectService(self.baseObject)
        self.coapd = make_server('', 8001, restlite.router(self.coapObjectService.routes))
        try: self.coapd.serve_forever()
        except KeyboardInterrupt: pass
        
            
if __name__ == '__main__' :
    
    server = SmartObjectService() # make an instance of the gateway and start a thread for each service interface  
    print 'Gateway started'
    
    httpThread = threading.Thread(target = server._startHttpObjectService)
    httpThread.daemon = True
    httpThread.start()
    print 'httpd started'
    
    coapThread = threading.Thread(target = server._startCoapObjectService)
    coapThread.daemon = True
    coapThread.start()
    print 'coapd started'
    
    # start agents here
    try:
        # register handlers etc.
        while 1: sleep(1)
    except KeyboardInterrupt: pass
    print 'got KeyboardInterrupt'
    
