'''
Created on Sep 15, 2012

PropertyOfInterest class for exposing custom methods for 
instances of arbitrary types

@author: mjkoster
'''
from RESTfulResource import RESTfulResource

class PropertyOfInterest(RESTfulResource):
    
    def __init__(self):
        RESTfulResource.__init__(self)
        
    # Descriptor property
    @property 
    def __get__(self):
        return self.value
    
    @property
    def __set__(self,newValue):
        self.value=newValue
        return
        
    @property
    def get(self):
        return self.value
    
    def set(self,newValue):
        self.value=newValue
        return