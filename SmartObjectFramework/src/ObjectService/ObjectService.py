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
        self.create('Description', Description)
        self.create('testProperty', ObservableProperty)
        self.resources['testProperty'].create('PropertyOfInterest', PropertyOfInterest)
        self.resources['testProperty'].set(1234)
        #self.resources['testProperty'].resources['PropertyOfInterest'].set(1234)
        
    