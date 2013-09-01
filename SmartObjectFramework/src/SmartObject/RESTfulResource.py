'''
Created on Sep 29, 2012

Base Class for RESTfulResources in SmartObject

Extends the Resource class

This class will be extended by Description, Observers,
ObservableProperty, PropertyOfInterest, and Agent resource classes

Instances of this class are created and deleted from within 
the scope of enclosing classes

Extends the Resource class with methods to parse content-types 
to internal resource representations and to serialize resources 
to content types

@author: mjkoster
'''
from Resource import Resource

class RESTfulEndpoint(object): # create a resource endpoint from a property reference
    def __init__(self, reference):
        self.resources = {}
        self._resource = reference # this only happens on init of the RESTfulEndpoint
        
    def get(self):
        return self._resource
    
    def set(self, newValue):
        self._resource = newValue
        
    
class RESTfulDictEndpoint(object): # create a resource endpoint from a property reference
    def __init__(self, dictReference):
        self.resources = {}
        self._resource = dictReference # this only happens on init of the RESTfulEndpoint
    
    def getList(self, key=None):
        if key == None:
            return self._resource.keys()
        else:
            return self._resource[key]
        
    def dict(self):
        return self._resource
    
    def get(self, key=None):
        if key == None:
            return self._resource
        else:
            return self._resource[key]
        
    def set(self,dictUpdate):
        self._resource.update(dictUpdate)
        return

    def update(self,dictUpdate):
        self._resource.update(dictUpdate)
        return


class RESTfulDictElementEndpoint(object):   
    def __init__(self, resourceName, newDict=None):
        self.resources = {}
        self._resourceName = resourceName
        if newDict==None :
            self._dict = self.resources # to create endpoints under endpoints
        else:
            self._dict = newDict  
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
 

class RESTfulResource(Resource) :
    
    # when this resource is created
    def __init__(self, parentObject=None, resourceName=''):
        Resource.__init__(self)
        self.Resources = RESTfulDictEndpoint(self.resources) #make resources endpoint
        # make properties resource and it's endpoint
        self._properties = {}
        self.Properties = RESTfulDictEndpoint(self._properties)
        # make an entry in resources to point to properties
        self.Resources.update({'Properties': self.Properties})
        
        self.resources.update({'thisObject': self})
        self.resources.update({'resourceName': resourceName}) 

        if parentObject == None : #no parent means this is a base object
            self.resources.update({'baseObject': self})
            self.resources.update({'parentObject': self})
            self.resources.update({'pathFromBase': ''})
        else :
            self.resources.update({'parentObject' : parentObject.resources['thisObject']})
            self.resources.update({'baseObject': parentObject.resources['baseObject'] })
            self.resources.update({'pathFromBase': self.resources['parentObject'].resources['pathFromBase'] \
                                   + '/' + self.resources['resourceName']})

        self.Properties.update({'resourceName': resourceName}) 
        self.Properties.update({'pathFromBase': self.resources['pathFromBase']})
            
        self._parseContentTypes = ['*/*'] 
        self._serializeContentTypes = ['*/*']
        self.defaultResources = None
        self.defaultClass = 'RESTfulResource' # class name, override in derived classes
        self.wellKnownClasses = [ 'Description' , 'Observers' , 'PropertyOfInterest' , 'SmartObject' , 'RESTfulResource' , 'Agent' ]


    def create(self, resourceName, className=None ) : 
        if resourceName not in self.resources :
            if className == None :
                if resourceName in self.wellKnownClasses :
                    className = resourceName
                else :
                    className = self.defaultClass 
                    # create new instance of the named class and add to resources directory, return the ref
            self.resources.update({resourceName : globals()[className](self, resourceName)}) 
            #self.resources[resourceName].resources.update({'resourceName': resourceName})
        return self.resources[resourceName] # returns a reference to the created instance

      
""" Default representation is JSON, XML also supported
    Add parse and serialize for RDF graph, etc. for richer 
    representation than JSON
    # Convert representation to native type
    def parse(self, content) :
        def types(self):
            return(self.parserContent_types)
        return content.value ;

    # Convert native type to representation
    def serialize(self, resource) :
        def types(self):
            return(self.serializerContent_types)
        return resource.str
"""


