'''
Created on Sep 15, 2012

PropertyOfInterest class for exposing custom methods for 
instances of arbitrary types. Typed property pattern

@author: mjkoster
'''
from RESTfulResource import RESTfulResource

class PropertyOfInterest(RESTfulResource):
    
    def __init__(self):
        RESTfulResource.__init__(self)

    def __get__(self, instance, cls):
        return self.value
    
    def __set__(self, instance, newValue):
        self.value=newValue
        return
    
    def get(self):
        return self.value
    
    def set(self,newValue):
        self.value=newValue
        return