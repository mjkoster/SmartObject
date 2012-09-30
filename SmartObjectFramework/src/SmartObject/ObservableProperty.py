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

class ObservableProperty(RESTfulResource):
    
    def __init__(self):
        RESTfulResource.__init__(self) 
        self.PropertyOfInterest = PropertyOfInterest(self)  
      
    def __get__(self):
        return self.PropertyOfInterest
    
    def __set__(self,newValue):
        self.PropertyOfInterest - newValue
          
    def get(self):
        return self.PropertyOfInterest.get()
    
    def set(self, newValue):
        self.PropertyOfInterest = newValue # use Descriptor Property interface