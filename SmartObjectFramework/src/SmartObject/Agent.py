'''
Created on Sep 15, 2012

Agent classes. Contains reference to instance of class containing observer 
handlers and code 

First create an instance of the Agent Class, then create a named Handler class instance under the Agent, 
then create an instance of the desired AppHandler code module under the named handler (using the module path)
by PUT (set) of a JSON object containing a dictionary of settings

for example myObserver.set({'handlerClass': 'SmartObject.Agent.additionHandler'})

@author: mjkoster
'''

from RESTfulResource import RESTfulResource


class AppHandler(object): # template and convenience methods for raw app handlers. Python app handler should extend this class
    def __init__(self, settings, linkBaseDict) : # object base resource dict is be passed in with settings
        self._linkCache = {}
        self._settings = settings # use the settings dictionary passed in            
        self._linkBaseDict = linkBaseDict   
  
        
    def linkToRef(self, linkPath):
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

    def _handleNotify(self, updateRef = None ): # override this for handling state changes from an observer
        pass


class additionHandler(AppHandler): # an example appHandler that adds two values together and stores the result
    # define a method for handling state changes in observed resources       
    def _handleNotify(self, updateRef = None ):
        # get the 2 addends, add them, and set the sum location
        self._addend1 = self.getByLink(self._settings['addendLink1'])
        self._addend2 = self.getByLink(self._settings['addendLink2'])
        self.setByLink( self._settings['sumOutLink'], self._addend1 + self._addend2 )


# simple print handler that echoes the value each time an observed resource is updated
class printHandler(AppHandler):
    def _handleNotify(self, resource) :
        print resource.resources['resourceName'], ' = ', resource.get()
 

class Handler(RESTfulResource):
    
    def __init__(self, parentObject=None):
        RESTfulResource.__init__(self, parentObject)
        self._settings = {} 
        self._appHandlerClassPath = None
        self._appHandlerClass = None
        self._linkBaseDict = self.resources['baseObject'].resources

    def importByPath(self,classPath):
        # separate the module path from the class,import the module, and return the class name
        self._components = classPath.split('.')
        self._module = __import__( '.'.join(self._components[:-1]) )
        self.appClass = self._components[-1]
        return self.appClass

    def appHandlerClass(self):
        return self._appHandlerClass
    
    def settings(self):
        return self._settings
            
    def handleNotify(self): # external method to override with method from appHandler
        pass
    
    def get(self, Key=None):
        if Key != None :
            return self.settings()[Key]
        else :
            return self.settings()
     
    def set(self, newSettings): # create an instance of a handler from settings dictionary
        self._settings.update(newSettings)
        if newSettings.has_key('handlerClass'):
            if newSettings['handlerClass'] != self._appHandlerClass: # create a new instance if handlerClass is being changed
                #note this requires handler class names be unique in the local environment
                #FIXME need to clean up old handler before creating new one
                self._appHandlerClassPath = self._settings['handlerClass']
                self._appHandlerClass = self.importByPath(self._appHandlerClassPath)
                self._appHandler = globals()[self._appHandlerClass](self._settings, self._linkBaseDict) # pass settings to the constructor
                
                if hasattr( self._appHandler, '_handleNotify' ) :
                    self.handleNotify = self._appHandler._handleNotify # reflect the appHandler handleNotify method 
                    

class Agent(RESTfulResource):
    
    def __init__(self, parentObject=None):
        RESTfulResource.__init__(self, parentObject)
        self._smartObjectBaseDict = self.resources['baseObject'].resources 
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
        if resourceName not in self.resources :
            if className == None :
                if resourceName in self.wellKnownClasses :
                    className = resourceName
                else :
                    className = self.defaultClass 
                    # create new instance of the named class and add to resources directory, return the ref
            self.resources.update({resourceName : globals()[className](self)}) 
            self.resources[resourceName].resources.update({'resourceName': resourceName})
            self._handlers.update({resourceName: self.resources['resourceName']})
        return self.resources[resourceName] # returns a reference to the created instance

        # need to destroy instance of code module
        