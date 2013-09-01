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
from os import system
from socket import gethostname, getfqdn


class SmartObjectService(object):
    
    def __init__(self, baseObject=None, port=8000): # if no service given, create a default service object
        self._port = port  # default port 8000
        self._baseObject = baseObject
        self.resources = self._baseObject.resources
        
    def start(self): 
        httpThread = threading.Thread(target = self._startHttpObjectService)
        httpThread.daemon = True
        httpThread.start()
        self._baseObject.Properties.update({'httpService': 'http://' + gethostname() + ':' + repr(self._port)})
       
    def _startHttpObjectService(self):
        from wsgiref.simple_server import make_server
        # HttpObjectService constructor method creates a Smart Object service and 
        # returns a constructor for a restlite router instance
        self.httpObjectService = HttpObjectService(self._baseObject)
        self.httpd = make_server('', self._port, restlite.router(self.httpObjectService.routes))
        try: self.httpd.serve_forever()
        except KeyboardInterrupt: pass
    
    def _startCoapObjectService(self):
        # Use similar pattern for CoAP service, emulate with another http server for now
        from wsgiref.simple_server import make_server
        # coapObjectServices = CoapObjectService(self.objectService)
        # self.coapd = make_server('', 61616, restlite.router(coapObjectService.routes))
        self.coapObjectService = HttpObjectService(self._baseObject)
        self.coapd = make_server('', self._port, restlite.router(self.coapObjectService.routes))
        try: self.coapd.serve_forever()
        except KeyboardInterrupt: pass
        
            
if __name__ == '__main__' :
    
    server = SmartObjectService(ObjectService(),8000) # make an instance of the service
    print 'Service created'
    server.start() # and start the listener
    print 'httpd started'

    # start agents here
    try:
        # register handlers etc.
        while 1: sleep(1)
    except KeyboardInterrupt: pass
    print 'got KeyboardInterrupt'
    
