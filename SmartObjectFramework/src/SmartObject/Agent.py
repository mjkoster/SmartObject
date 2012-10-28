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

# import AppHandlers # import a well known module


class AppHandler(object): # template and convenience methods for raw app handlers. Python app handler should extend this class
    def __init__(self) :
        self._propertyLinks = {}
    
    def _updateHandler(self):
        pass


class RESTfulEndpoint(object):
    def __init__(self, reference):
        self._resource = reference
        
    def get(self):
        return self._resource
    
    def set(self,newValue):
        self._resource = newValue
        return
    
    
class Handler(RESTfulResource):
    
    def __init__(self):
        RESTfulResource.__init__(self)
        self._propertyLinks = {}
        self._appHandlerName = None
        self._updateHandler = None # reference to _updateHandler method of AppHandler

    def appHandlerName(self):
        return self._appHandlerName
    
    def propertyLinks(self):
        return self._propertyLinks

    def updateHandler(self):
        return self._updateHandler
        
    def get(self):
        return self._appHandlerName
    
    def set(self,appHandlerName): # create an instance of a code object in this handler object
        self._appHandlerName = appHandlerName
        self._moduleName, self._className = self._appHandlerName.split('.')
        # from <self._moduleName> import <self._className> get the code object into the namespace
        self._appHandler = globals()[self._className]() # make instance of AppHandler by name
        # make a resource to read back the AppHandler class name
        self.resources.update( { 'AppHandler' : RESTfulEndpoint(self._appHandlerName)}) 
        # set up the property links resources
        if hasattr( self._appHandler, '_propertyLinks') :
            self._propertyLinks = self._appHandler._propertyLinks
            for self._propertyLinkName in self._propertyLinks.keys() : 
                self.resources.update({self._propertyLinkName : self._propertyLinks[self._propertyLinkName]})
                
        # set up the callable property to be invoked on callbacks
        if hasattr( self.appHandler, '_updateHandler' ) :
            self._updateHandler = self._appHandler._updateHandler
               


class Agent(RESTfulResource):
    
    def __init__(self):
        RESTfulResource.__init__(self)
                
        self.defaultClass = 'Handler'
        self._handlers = {}
        
    def get(self, handlerName=None):
        if handlerName == None:
            return self._handlers.keys() # to get the list of names
        else:
            if self._handlers.has_key(handlerName) :
                return self._handlers[handlerName] # to get reference to handler resources by handler name
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
        if className == self.defaultClass : # Handler class assumed
            self._handlers.update( {resourceName, self.resources[resourceName]} )
        return self.resources[resourceName] # returns a reference to the created instance

        # need to destroy instance of code module
        