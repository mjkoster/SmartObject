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
from SmartObject.Observers import Observers
from SmartObject.PropertyOfInterest import PropertyOfInterest
from rdflib.term import Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, OWL

class ObjectService(SmartObject):

    def __init__(self):
        SmartObject.__init__(self) 
        import __builtin__
        __builtin__.SmartObjectServiceBaseDict = self.resources # make this a global reference
        
        self.defaultClass = 'SmartObject'
        # Use a smart object instance as a container for SmartObjects 
        # and create a Description resource for the RDF registry
        self.description = self.create('Description')
        
        
        # TEST
        # create a SmeartObjectbject the top level for a rough test
        # add some example triples describing the object and it's properties
        self.description.set((URIRef('testObject'), RDFS.Class, Literal('SmartObject')))
        self.description.set((URIRef('testObject/propertyOne'), RDFS.Resource, Literal('logEntry')))
        self.description.set((URIRef('testObject/propertyOne'), RDF.type, Literal('message')))
        self.description.set((URIRef('testObject/propertyTwo'), RDFS.Resource, Literal('temperature')))
        self.description.set((URIRef('testObject/propertyTwo'), RDF.type, Literal('sensor')))
        # create the object and it's properties using create

        self.testObject = self.create('testObject')
        self.testObject.description = self.testObject.create('Description')
        self.testObject.propertyOne = self.testObject.create('propertyOne')
        self.testObject.testObject = self.testObject.create('SmartObject')
        self.testObject.testObject.Description = self.testObject.testObject.create('Description')
        self.testObject.propertyOne.testProperty = self.testObject.propertyOne.create('PropertyOfInterest')
        self.testObject.propertyOne.testProperty.set(1234)
        '''
        self.testObject.propertyOne.PropertyOfInterest = \
            self.testObject.propertyOne.create('PropertyOfInterest', PropertyOfInterest)
        self.testObject.propertyTwo = self.testObject.create('propertyTwo', ObservableProperty)
        self.testObject.propertyTwo.PropertyOfInterest = \
            self.testObject.propertyTwo.create('PropertyOfInterest', PropertyOfInterest)
        self.testObject.propertyOne.set('Hello World')
        self.testObject.propertyTwo.set(98.6)
        print self.testObject.propertyOne.get() # PropertyOfInterest.get()
        print self.testObject.propertyTwo.get() # PropertyOfInterest.get()
        
        self.testObject.propertyThree = self.testObject.create('propertyThree', ObservableProperty)
        self.testObject.propertyThree.PropertyOfInterest = \
            self.testObject.propertyThree.create('PropertyOfInterest', PropertyOfInterest)       
        self.testObject.propertyTwo.observers = \
            self.testObject.propertyTwo.create('observers', Observers)
        self.testObject.propertyTwo.observers.set('http://localhost:8000/testObject/propertyThree')
        
        self.testObject.propertyTwo.set(99.7)
        '''
        
    