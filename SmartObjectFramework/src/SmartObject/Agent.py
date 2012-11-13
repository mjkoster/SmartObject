'''
Created on Sep 15, 2012

Agent class. Contains reference to instance of class containing observer 
handlers and code 

First create an instance of the Agent Class, then create a named handler
and set the desired appHandler code module to the named handler

At this point, the appHandler class name, update handler callable method, and a dictionary
of property link names to property link resources are published, to enable connection
of the handler to it's input and output properties. 

@author: mjkoster
'''

from RESTfulResource import RESTfulResource


class AppHandler(object): # template and convenience methods for raw app handlers. Python app handler should extend this class
    def __init__(self, linkBaseDict = None) : # object base resource dict can be passed in
        if linkBaseDict is None :
            
            try:
                import __builtin__
                self.linkBaseDict = __builtin__.eval('SmartObjectServiceBaseDict')
            except AttributeError:
                print 'SmartObjectServiceBaseDict not found'
            
        else:
            self.linkBaseDict = linkBaseDict
                
        self._propertyLinks = {} 
        self._linkCache = {}
  
        
    def linkToRef(self, linkPath ):
        '''
        takes a path string and walks the object tree from a base dictionary
        returns a ref to the resource at the path endpoint
        store translations in a hash cache for fast lookup after the first walk
        '''
        self._linkPath = linkPath
        
        if self._linkPath in self.linkCache.keys() :
            return self._linkCache[self._linkPath]
        # cache miss, walk path and update cache at end
        self._currentDict = self._linkBaseDict
        self._pathElements = linkPath.split('/')
        
        for pathElement in self._pathElements[0:-1] : # all but the last, which should be the endpoint
            self._currentDict = self.currentDict[pathElement].resources
            
        self._resource = self._currentDict[self._pathElements[-1] ]
        self._linkCache.update({ self._linkPath : self._resource })
        return self._resource
       
        
    def getByLink(self, linkPath):
        return self.linkToRef(linkPath).get()

    def setByLink(self, linkPath, newValue):
        self.linkToRef(linkPath).set(newValue)

    def _updateHandler(self, updateRef = None ): # override this for handling state changes from an observer
        pass


class additionHandler(AppHandler): # an example appHandler 
    def __init__(self):
        AppHandler.__init__(self)
        # create the input and output link properties
        self._addend1Link = None
        self._addend2Link = None
        self._sumOutLink = None
        # publish them with some names as an index
        self._propertyLinks = { 'addend1' : self._addend1Link,
                               'addend2' : self._addend2Link,
                               'sumOut' : self._sumOutLink
                               }
        
        # define a method for handling state changes in observed resources       
        def _updateHandler(self, updateRef = None ):
                '''
                get the 2 addends, add them, and set the sum location
                '''
                self._addend1 = self.getByLink(self._addend1Link)
                self._addend2 = self.getByLink(self._addend2Link)
                self.setByLink( self._sumOutLink, self._addend1 + self._addend2 )
                
            
class RESTfulEndpoint(object): # create a resource endpoint from a property reference
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
        self._propertyLinks = None 
        self._appHandlerName = None
        self._updateHandler = None # reference to _updateHandler method of AppHandler

    def importByName(self,classPath):
        module = __import__(classPath)
        components = classPath.split('.')
        for component in components[1:]:
            module = getattr(module, component)
            return module

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
        self._appHandlerClass = self.importByName(appHandlerName)
        self._appHandler = self._appHandlerClass() # make instance of AppHandler by name
        # make a resource to read back the AppHandler class name
        self.resources.update( { 'AppHandler' : RESTfulEndpoint(self._appHandlerName)}) 
        # set up the property links resources
        if hasattr( self._appHandler, '_propertyLinks') :
            self._propertyLinks = self._appHandler._propertyLinks
            self.resources.update( { 'propertyLinks' : RESTfulEndpoint(self._propertyLinks)})
            for self._propertyLinkName in self._propertyLinks.keys() : 
                self.resources.update({self._propertyLinkName : \
                                       RESTfulEndpoint(self._propertyLinks[self._propertyLinkName]) })
                
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
        