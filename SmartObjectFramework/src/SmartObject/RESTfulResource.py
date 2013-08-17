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

class RESTfulResource(Resource) :
    
    # when this resource is created
    def __init__(self, parentObject=None):
        Resource.__init__(self)
        
        self.resources.update({'thisObject': self})
        if parentObject == None :
            self.resources.update({'baseObject': self})
            self.resources.update({'parentObject': self})
        else :
            self.resources.update({'parentObject' : parentObject.resources['thisObject']})
            self.resources.update({'baseObject': parentObject.resources['baseObject'] })
            
        self._parseContentTypes = [] 
        self._serializeContentTypes = []
        self.defaultClass = 'RESTfulResource' # class name, override in derived classes
        self.wellKnownClasses = [ 'Description' , 'Observers' , 'PropertyOfInterest' , 'SmartObject' , 'RESTfulResource' , 'Agent' ]


    def create(self, resourceName, className=None ) : 
        if className == None :
            if resourceName in self.wellKnownClasses :
                className = resourceName
            else :
                className = self.defaultClass 
        # create new instance of the named class, pass the resource dict to the constructor, 
        # add to resources directory, return the ref
        self.resources.update({resourceName : globals()[className](self)}) 
        print className
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


