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
        self.resources = {} # the visible directory of resource names 
        self.value = []

    # when this resource is deleted, recursively delete all internal resources
    def __del__(self, instance):
        for self.__resource in self.resources :
            del self.__resource
        
    def __get__(self, instance, cls):
        return self.get()
    
    def __set__(self, instance, newValue):
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
        self.__resourceName = className(self) # make instance of named class
        self.resources += {resourceName : self.__resourceName} # add instance name to directory 
        return

    # for removing resources inside this resource
    def delete(self, resourceName) :
        del self.resources[resourceName] # remove object reference
        self.resources.remove(resourceName) # remove visible directory entry
        return
