'''
Created on Sep 15, 2012

Agent classes. Contains reference to instance of class containing observer 
handlers and code 

First create an instance of the Agent Class, then create a named Handler class instance under the Agent, 
then create an instance of the desired AppHandler code module under the named handler (using the module path)

At this point, the appHandler class name, update handler callable method, and a dictionary
of property link names to property link resources are published, to enable connection
of the handler to it's input and output properties. 

Global reference to base object dictionary is not working but hacked in an app level fix passing the 
reference to a property of the handler resource to use starting up an appHandler instance inside

Provided RESTfulDictElementEndpoint to create a REST endpoint with a resources dictionary for each external property
of a handler, such that the property can be updated using a web method.

Added RESTfulDictEndpoint to allow PUT of JSON to update dictionary

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

        
class RESTfulEndpoint(object): # create a resource endpoint from a property reference
    def __init__(self, reference):
        self.resources = {}
        self._resource = reference # this only happens on init of the RESTfulEndpoint
        
    def get(self):
        return self._resource
    
class RESTfulDictEndpoint(object): # create a resource endpoint from a property reference
    def __init__(self, dictReference):
        self.resources = {}
        self._resource = dictReference # this only happens on init of the RESTfulEndpoint
        
    def get(self):
        return self._resource
    
    def set(self,newDict):
        self._resource.update(newDict)
        return

class RESTfulDictElementEndpoint(object):   
    def __init__(self, resourceName, dict=None):
        self.resources = {}
        if dict==None :
            self._dict = self.resources # to create endpoints under endpoints
        else:
            self._dict = dict  
        self._resourceName = resourceName
            
    def get(self):
        return self._dict[self._resourceName]
    
    def set(self,newValue):
        self._dict.update( {self._resourceName : newValue} )
        return 

    def create(self, resourceName):
        self.resources.update( {resourceName : RESTfulDictElementEndpoint(resourceName)} ) # make an endpoint with internal dict
        return
    
    def delete(self, resourceName):
        del self.resources[resourceName]
        return


class additionHandler(AppHandler): # an example appHandler that adds two values together and stores the result
    def __init__(self, linkBaseDict=None):
        AppHandler.__init__(self, linkBaseDict)
        # create the input and output links 
        self._propertyLinks = {}
        # publish them with names as an index 
        self._propertyLinks.update({'addend1' : None})
        self._propertyLinks.update({'addend2' : None})
        self._propertyLinks.update({'sumOut' : None})
       
    # define a method for handling state changes in observed resources       
    def _updateHandler(self, updateRef = None ):
        # get the 2 addends, add them, and set the sum location
        self._addend1 = self.getByLink(self._propertyLinks['addend1'])
        self._addend2 = self.getByLink(self._propertyLinks['addend2'])
        self.setByLink( self._propertyLinks['sumOut'], self._addend1 + self._addend2 )
        


class Handler(RESTfulResource):
    
    def __init__(self, baseDict=None):
        RESTfulResource.__init__(self)
        self._propertyLinks = None 
        self._appHandlerName = None
        self._objectPathBaseDict = baseDict

    def importByPath(self,classPath):
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
    
    def create(self,appHandlerPath): # create an instance of a code object: import module and make instance of class
        self._appHandlerPath = appHandlerPath
        self._appHandlerName = self.importByPath(self._appHandlerPath) # returns the class to make instance of...
        self._appHandler = globals()[self._appHandlerName](self._objectPathBaseDict) # pass in the object path root
        # make a resource to read back the AppHandler class name
        self.resources.update( { 'AppHandler' : RESTfulEndpoint(self._appHandlerName)}) 
        # set up the property links resources 
        if hasattr( self._appHandler, '_propertyLinks') :
            self._propertyLinks = self._appHandler._propertyLinks
            self.resources.update( { 'propertyLinks' : RESTfulDictEndpoint(self._propertyLinks)})
            # set up a REST endpoint for each propertyLink entry
            for propertyLink in self._propertyLinks.keys() :
                self.resources.update( {propertyLink : RESTfulDictElementEndpoint(propertyLink, self._propertyLinks)} )           
        # set up the callable property to be invoked on callbacks
        if hasattr( self._appHandler, '_updateHandler' ) :
            self._updateHandler = self._appHandler._updateHandler # hack local property for now
               


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
        