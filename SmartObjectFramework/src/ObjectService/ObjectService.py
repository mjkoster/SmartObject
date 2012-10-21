'''
Created on Oct 1, 2012

Service layer for SmartObjects usable for any RESTful objects 
Adds registry and methods for creating and removing objects

The service is itself based on a SmartObject resource pattern with 
SmartObjects as the created resources and a default Description 
resource containing descriptions of and links to the created 
SmartObjects

@author: mjkoster
'''
from SmartObject.SmartObject import SmartObject
from SmartObject.Description import Description
from SmartObject.ObservableProperty import ObservableProperty
from SmartObject.PropertyOfInterest import PropertyOfInterest

class ObjectService(SmartObject):

    def __init__(self):
        SmartObject.__init__(self) 
        # Use a smart object instance as a container for SmartObjects 
        # and create a Description resource for the RDF registry
        self.Description = self.create('Description', Description)
        self.testProperty = self.create('testProperty', ObservableProperty) #make a decorator for resourceName
        self.testProperty.PropertyOfInterest = \
            self.testProperty.create('PropertyOfInterest', PropertyOfInterest)
        self.testProperty.set('happy birthday Catt')
        self.testProperty = 'happy birthday Catt' # doesn't work 
        print self.testProperty
        
    