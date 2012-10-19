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
    def __init__(self):
        Resource.__init__(self)
        self.content_types = [] 
        
    # when this resource is deleted
    def __del__(self):
        Resource.__del__(self)
    
    # Convert representation to native type
    def parse(self, content) :
        def types(self):
            return(self.content_types)
        return content.value ;

    # Convert native type to representation
    def serialize(self, resource) :
        def types(self):
            return(self.content_types)
        return resource.str



