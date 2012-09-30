'''
Created on Sep 15, 2012

Base Class for Resources in SmartObject

This class will be extended by RESTfulResource to add content-type support

Contains methods for resource-oriented services:
create, delete, set, and get are meant to be 
extended or overridden by concrete class instances 
for content-specific interaction

@author: mjkoster
'''
class Resource(object) :
    
    # when this resource is created
    def __init__(self):
        self.resources = {}
        self.value = []

    # when this resource is deleted, recursively delete all internal resources
    def __del__(self):
        for self.__resource in self.resources :
            del self.__resource
        
    def __get__(self):
        return self.get
    
    def __set__(self, newValue):
        self.set(newValue)
        return

    # return the default contents of this resource
    #@Resource.getter - would this decorator work?
    def get(self) :
        return(self.value)

    # update the default contents of this resource
    #@Resource.setter
    def set(self, newValue) :
        self.value=newValue
        return
      
    # for adding resources inside this resource
    def create(self, resourceName, className) :
        self.resourceName = className(self) # make instance of named class
        self.resources.add(resourceName) # add instance name to resources 
        return

    # for removing resources inside this resource
    def delete(self, resourceName) :
        del self.resourceName 
        self.resources.remove(resourceName)
        return
