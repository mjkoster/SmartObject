'''
Created on Sep 15, 2012

SmartObject class

The SmartObject is the top level Resource pointed to by the URL

The base resource is a description, which for linked data is the default
resource returned by SmartObject.get() and is the object Descriptor 
The following equivalent references return all 
triples in the SmertObject.Description resource:

SmartObject
SmartObject.get()
SmartObject.Description
SmartObject.Description.get()

Practical instances of SmartObject will have additional resources 
such as ObservableProperty and Agent instances dynamically created
from resource constructors loaded into the top level Description resource 

Clone and composite SmartObject instances can be built from resource 
constructors of other SmartObjects

@author: mjkoster
'''
from RESTfulResource import RESTfulResource
from Description import Description
from Agent import Agent
from ObservableProperty import ObservableProperty

class SmartObject(RESTfulResource):
    
    def __init__(self):
        RESTfulResource.__init__(self)
        self.Description = Description(self)
        self.resources.add("Description")
        
    # Descriptor for SmartObject is the Description resource, 
    # to provide linked data compatibility
    # This is also available via the property interface: SmartObject
    
    def __get__(self, instance, cls):
        return self.get()
    
    def __set__(self, instance, (s,p,o)):
        self.set((s,p,o))
        return
    
    def get(self):
        return self.Description.get()
    
    def set(self, (s,p,o)):
        self.Description.set((s,p,o))
        return
