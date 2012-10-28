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

class SmartObjectHandler(RESTfulResource):
    
    def __init__(self):
        RESTfulResource.__init__(self)
        self._propertyLinks = []
        self._codeModule = None

    def codeModule(self):
        return self._codeModule
    
    def propertyLinks(self):
        return self._propertyLinks

    def updateMethod(self):
        return self._updateMethod
    
    def _updateMethod(self):
        pass
    
    def get(self):
        return self._codeModule
    
    def set(self,codeModule):
        self._codeModule = codeModule


class Agent(RESTfulResource):
    
    def __init__(self, agent):
        RESTfulResource.__init__(self)
        # reference to the code class to create an instance of 
        # can be passed in on the constructor, or default on init, or be changed later
        self.defaultClass = 'SmartObjectHandler'
        self.__handlers = {}
        
    def get(self, handlerName=None):
        if handlerName == None:
            return self._handlers.keys()
        else:
            if self._handlers.has_key(handlerName) :
                return self._handlers[handlerName]
        return None
    
    '''    
    def create(self, resourceName, className = 'Handler') :
        # create new instance of the named class and add to resources directory, return the ref
        self.resources.update({resourceName : className()}) 
        if className == 'Handler' :
            handler = SmartObjectHandler(resourceName) # name of code object
        return self.resources[resourceName]
    '''    
    def create(self, resourceName, className=None ) : 
        if className == None :
            if resourceName in self.wellKnownClasses :
                className = resourceName
            else :
                className = self.defaultClass 
        # create new instance of the named class and add to resources directory, return the ref
        self.resources.update({resourceName : globals()[className]()}) 
        if className == self.defaultClass : # Handler class
            self._handlers.update( {resourceName, self.resources[resourceName]} )
        return self.resources[resourceName] # returns a reference to the created instance

 
    def delete(self, handlerName):
        RESTfulResource.delete(handlerName)    
        # and more...
        return
        # need to destroy instance of code module
        