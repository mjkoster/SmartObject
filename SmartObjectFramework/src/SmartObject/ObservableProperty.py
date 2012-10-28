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
        self.defaultClass = 'PropertyOfInterest'
        # default return property of interest
    def get(self):
        if 'PropertyOfInterest' in self.resources :
            return self.resources['PropertyOfInterest'].get()
        return None
    
    def set(self, newValue):
        if 'PropertyOfInterest' in self.resources :
            self.resources['PropertyOfInterest'].set(newValue)
            if 'Observers' in self.resources :
                self.resources['Observers'].onUpdate() # invoke the callable 
                
    def create(self, resourceName, className=None ) : 
        if className == None :
            if resourceName in self.wellKnownClasses :
                className = resourceName
            else :
                className = self.defaultClass 
        # create new instance of the named class and add to resources directory, return the ref
        self.resources.update({resourceName : globals()[className]()}) 
        return self.resources[resourceName] # returns a reference to the created instance


