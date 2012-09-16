'''
Created on Sep 15, 2012

Abstract Class for Resources in SmartObject

This class will be extended by Description, Subscription,
ObservableProperty, PropertyOfInterest, and Agent classes

Instances of this class are created and deleted from within 
the scope of enclosing classes

Contains methods for RESTful resource-oriented services:
create, delete, set, and get are meant to be 
extended or overridden by concrete class instances 
for content-specific interaction

@author: mjkoster
'''
class Resource :
    
    # when this resource is created
    def __init__(self):
        self.resources = {};
        self.value = [];

    # when this resource is deleted
    def __del__(self):
        pass
    
    # for adding resources inside this resource
    def create(self, resource) :
        self.resources.add(resource);

    # for removing resources inside this resource
    def delete(self, resource) :
        self.resources.remove(resource);
    
    # update the default contents of this resource
    def set(self, newValue) :
        self.value=newValue;
     
    # return the default contents of this resource
    def get(self) :
        return(self.value);

