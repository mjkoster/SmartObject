'''
Created on Sep 15, 2012

Agent class. Contains reference to instance of class containing observer 
handlers and code 

Contains references to observer handlers which are expected to be used only
by Agent code i.e. not exposed to service interfaces but may allow inspection 
for debug. 

@author: mjkoster
'''

from RESTfulResource import RESTfulResource

class Handler(RESTfulResource):
    pass

class Agent(RESTfulResource):
    
    def __init__(self, agent):
        RESTfulResource.__init__(self)
        # reference to the code class to create an instance of 
        # can be passed in on the constructor, or default on init, or be changed later
        self.__handlers = []
        
    def get(self, handler=None):
        if handler == None:
            return self.__handlers
        else:
            if self[handler] :
                return self.__handlers[handler]
        return None
    
    def set(self, handler):
        self.handler.set # what to do, what to do...
        return
    
    def create(self, resourceName, className) :
        # create new instance of the named class and add to resources directory, return the ref
        self.resources.update({resourceName : className()}) 
        if className == 'Handler' :
            handler = Handler() # where is code object
        return self.resources[resourceName]
     
    def delete(self, handlerName):
        RESTfulResource.delete(handlerName)    
        # and more...
        return
        # need to destroy instance of code module
        