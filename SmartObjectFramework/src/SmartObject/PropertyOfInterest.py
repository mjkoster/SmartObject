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
        
    # descriptor method?
    def __get__(self):
        return self.value
    
    def __set__(self,newValue):
        self.value=newValue
        return
        
    def get(self):
        return self.value
    
    def set(self,newValue):
        self.value=newValue
        return