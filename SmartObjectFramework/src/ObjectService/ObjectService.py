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
from rdflib.term import Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, OWL

class ObjectService(SmartObject):

    def __init__(self):
        SmartObject.__init__(self) 
        # Use a smart object instance as a container for SmartObjects 
        # and create a Description resource for the RDF registry
        self.description = self.create('description', Description)
        # TEST
        # create a SmeartObjectbject the top level for a rough test
        # add some example triples describing the object and it's properties
        self.description.set((URIRef('testObject'), RDFS.Class, Literal('SmartObject')))
        self.description.set((URIRef('testObject/propertyOne'), RDFS.Resource, Literal('logEntry')))
        self.description.set((URIRef('testObject/propertyOne'), RDF.type, Literal('message')))
        self.description.set((URIRef('testObject/propertyTwo'), RDFS.Resource, Literal('temperature')))
        self.description.set((URIRef('testObject/propertyTwo'), RDF.type, Literal('sensor')))
        # create the object and it's properties using create
        self.testObject = self.create('testObject', SmartObject)
        self.testObject.propertyOne = self.testObject.create('propertyOne', ObservableProperty)
        self.testObject.propertyOne.PropertyOfInterest = \
            self.testObject.propertyOne.create('PropertyOfInterest', PropertyOfInterest)
        self.testObject.propertyTwo = self.testObject.create('propertyTwo', ObservableProperty)
        self.testObject.propertyTwo.PropertyOfInterest = \
            self.testObject.propertyTwo.create('PropertyOfInterest', PropertyOfInterest)
        self.testObject.propertyOne.set('Hello World')
        self.testObject.propertyTwo.set(98.6)
        print self.testObject.propertyOne.get() # PropertyOfInterest.get()
        print self.testObject.propertyTwo.get() # PropertyOfInterest.get()
        
    