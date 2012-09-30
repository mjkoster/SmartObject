'''
Created on Sep 15, 2012

SmartObject class

The SmartObject is the top level Resource pointed to by the URL

The base resource is a description, which for linked data is the default
resource returned by SmartObject.get() and is the object Descriptor 
(default return value)  The following equivalent references return all 
triples in the SmertObject.Description resource:

SmartObject.Description.get()
SmartObject.Description.get
SmartObject.Description()
SmartObject.Description
SmartObject.get()
SmartObject.get
SmartObject()
SmartObject

Practical instances of SmartObject will have additional resources 
such as ObservableProperty and Agent instances dynamically created
from resource constructors loaded into the top level Description resource 

Clone and composite SmartObject instances can be built from resource 
constructors of other SmartObjects

@author: mjkoster
'''
from RESTfulResource import RESTfulResource
from Description import Description

class SmartObject(RESTfulResource):
    
    def __init__(self):
        RESTfulResource.__init__(self)
        self.Description = Description(self)
        
    # Descriptor for SmartObject is the Description resource, 
    # to provide linked data compatibility
    # This is also available via the property interface: SmartObject
    
    @property
    def __get__(self):
        return self.Description.get()
    
    @property
    def __set__(self, (s,p,o)):
        self.Description.set((s,p,o))
        return
    
    @property
    def get(self):
        return self.Description.get()
    
    def set(self, (s,p,o)):
        self.Description.set((s,p,o))
        return
    
    def create(self,resource):
        super(SmartObject,self).create(resource) # override this?
        return
    
    def delete(self,resource):
        super(SmartObject,self).delete(resource) # override this?
        return
    