'''
Created on Sep 15, 2012

Agent class. Contains reference to instance of class containing observer 
handlers and code 

First create an instance of the Agent Class, then create a named handler
and set the desired appHandler code module to the named handler

At this point, the appHandler class name, update handler callable method, and a dictionary
of property link names to property link resources are published, to enable connection
of the handler to it's input and output properties. 

Global reference to base object dictionary is not working but hacked in an app level fix passing the 
reference to a property of the handler resource to use starting up an appHandler instance inside

@author: mjkoster
'''

from RESTfulResource import RESTfulResource


class AppHandler(object): # template and convenience methods for raw app handlers. Python app handler should extend this class
    def __init__(self, linkBaseDict = None) : # object base resource dict can be passed in
        if linkBaseDict is None :
            
            try:
                import __builtin__
                self._linkBaseDict = __builtin__.eval('SmartObjectServiceBaseDict')
            except :
                print 'SmartObjectServiceBaseDict not found'
            
        else:
            self._linkBaseDict = linkBaseDict
                
        self._propertyLinks = {} 
        self._linkCache = {}
  
        
    def linkToRef(self, linkPath ):
        '''
        takes a path string and walks the object tree from a base dictionary
        returns a ref to the resource at the path endpoint
        store translations in a hash cache for fast lookup after the first walk
        '''
        self._linkPath = linkPath
        if self._linkPath in self._linkCache.keys() :
            return self._linkCache[self._linkPath]
        # cache miss, walk path and update cache at end
        self._currentDict = self._linkBaseDict
        self._pathElements = linkPath.split('/')
        for pathElement in self._pathElements[:-1] : # all but the last, which should be the endpoint
            self._currentDict = self._currentDict[pathElement].resources
        self._resource = self._currentDict[self._pathElements[-1] ]
        self._linkCache.update({ self._linkPath : self._resource })
        return self._resource
        
    def getByLink(self, linkPath):
        return self.linkToRef(linkPath).get()

    def setByLink(self, linkPath, newValue):
        self.linkToRef(linkPath).set(newValue)

    def _updateHandler(self, updateRef = None ): # override this for handling state changes from an observer
        pass


class additionHandler(AppHandler): # an example appHandler that adds two values together and stores the result
    def __init__(self, linkBaseDict=None):
        AppHandler.__init__(self, linkBaseDict)
        # create the input and output link properties
        self._addend1Link = 'uninitialized'
        self._addend2Link = 'uninitialized'
        self._sumOutLink = 'uninitialized'
        # publish them with some names as an index
        self._propertyLinks = {'addend1' : self._addend1Link,
                               'addend2' : self._addend2Link,
                               'sumOut' : self._sumOutLink
                               }
        
    # define a method for handling state changes in observed resources       
    def _updateHandler(self, updateRef = None ):
        # get the 2 addends, add them, and set the sum location
        self._addend1 = self.getByLink(self._propertyLinks['addend1'])
        self._addend2 = self.getByLink(self._propertyLinks['addend2'])
        self.setByLink( self._propertyLinks['sumOut'], self._addend1 + self._addend2 )
        
        
class RESTfulEndpoint(object): # create a resource endpoint from a property reference
    def __init__(self, reference):
        self._resource = reference # this only happens on init of the RESTfulEndpoint
        self.resources = {}
        
    def get(self):
        return self._resource
    
    def set(self,newValue):
        self._resource = newValue
        return 
    
    
class Handler(RESTfulResource):
    
    def __init__(self, baseDict=None):
        RESTfulResource.__init__(self)
        self._propertyLinks = None 
        self._appHandlerName = None
        self._objectPathBaseDict = baseDict
        #self._updateHandler = None # reference to _updateHandler method of AppHandler

    def importByName(self,classPath):
        # separate the module path from the class,import the module, and return the class name
        self._components = classPath.split('.')
        self._module = __import__( '.'.join(self._components[:-1]) )
        self.appClass = self._components[-1]
        return self.appClass

    def appHandlerName(self):
        return self._appHandlerName
    
    def propertyLinks(self):
        return self._propertyLinks

    def updateHandler(self):
        return self._updateHandler
        
    def _updateHandler(self): # internal method to override
        pass
    
    def get(self):
        return self._appHandlerName
    
    def create(self,appHandlerPath): # create an instance of a code object in this handler object, import module and make instance of class
        self._appHandlerPath = appHandlerPath
        self._appHandlerName = self.importByName(self._appHandlerPath)
        self._appHandler = globals()[self._appHandlerName](self._objectPathBaseDict) # pass in the object path root
        # make a resource to read back the AppHandler class name
        self.resources.update( { 'AppHandler' : RESTfulEndpoint(self._appHandlerName)}) 
        # set up the property links resources
        if hasattr( self._appHandler, '_propertyLinks') :
            self._propertyLinks = self._appHandler._propertyLinks
            self.resources.update( { 'propertyLinks' : RESTfulEndpoint(self._propertyLinks)})
            for self._propertyLinkName in self._propertyLinks.keys() : 
                self.resources.update({self._propertyLinkName : \
                                       RESTfulEndpoint(self._propertyLinks[self._propertyLinkName]) })
        # does this reference get stale when the propertyLinks are set?
        
        # set up the callable property to be invoked on callbacks
        if hasattr( self._appHandler, '_updateHandler' ) :
            self._updateHandler = self._appHandler._updateHandler
               


class Agent(RESTfulResource):
    
    def __init__(self, SmartObjectBaseDict=None):
        RESTfulResource.__init__(self)
        self._smartObjectBaseDict = SmartObjectBaseDict # should agent and handler each have a base object?
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
            self._handlers.update( {resourceName : self.resources[resourceName]} )
        return self.resources[resourceName] # returns a reference to the created instance

        # need to destroy instance of code module
        