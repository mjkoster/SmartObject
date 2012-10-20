'''
Created on Sep 15, 2012

ObservableProperty class to hold the PropertyOfInterest and it's description 
and potential observers

The Descriptor Property is the ObservableProperty, 
which has it's value as it's Descriptor Property
allowing the value of the ObservableProperty to be 
it's Descriptor Property

Thus the value of a smart object Observable Properties 
can be referenced by <SmartObject>.<ObservableProperty>
e.g.:

display(room.temperature) 
"room" is the name of the SmartObject and "temperature" is the name of an 
ObservableProperty of the "room" object

thermostat.setting = 77
"thermostat" is the name of the object and "setting" is the name of the
ObservableProperty being manually set

@author: mjkoster
'''
from RESTfulResource import RESTfulResource
from PropertyOfInterest import PropertyOfInterest
from Description import Description
from Observers import Observers

class ObservableProperty(RESTfulResource):
    
    def __init__(self):
        RESTfulResource.__init__(self) 
        # create an instance of PropetyOfInterest to hold the observable type default
        # self.create('PropertyOfInterest', PropertyOfInterest)
      
    def __get__(self, instance, cls):
        if self.hasattr('PropertyOfInterest'):
            return self.PropertyOfInterest
    
    def __set__(self, instance, newValue):
        if self.hasattr('PropertyOfInterest'):
            self.PropertyOfInterest = newValue
          
    def get(self):
        if self.hasattr('PropertyOfInterest'):
            return self.PropertyOfInterest
    
    def set(self, newValue):
        if self.hasattr('PropertyOfInterest'):
            self.PropertyOfInterest = newValue
        
