'''
Created on Sep 15, 2012

Observers class for observation of changes in a resource

@author: mjkoster
'''
from RESTfulResource import RESTfulResource
from urlparse import urlparse

class Observers(RESTfulResource):
    
    def __init__(self):
        RESTfulResource.__init__(self)
        self.__schemes = ['http', 'coap', 'callback']
        self.__observers = []
        
    def __get__(self, instance, cls):
        return self.get()
    
    def __set__(self, instance, targetURI):
        self.set(targetURI)
        
    def onUpdate(self,resource):
        self.__onUpdate(resource)
        
    def __onUpdate(self, resource):
        for self.__observer in self.__observers:
            self.__notify(self.__observer, resource)
    
    def __notify(self, targetURL, resource):
        urlObject = urlparse(targetURL)
        if urlObject.scheme == 'http' :
            self.__httpPostNotify(targetURL, resource)
        elif urlObject.scheme == 'coap' :
            self.__coapGetNotify(targetURL, resource)
        elif urlObject.scheme == 'callback' :
            self.__callbackNotify(targetURL, resource)
            
    def __httpPostNotify(self, targetURL, resource):
        pass # invoke method from http client interface
    
    def __coapGetNotify(self, targetURL, resource):
        pass # invoke method from CoAP server interface
    
    def __callbackNotify(self, targetURL, resource):
        #call the fuction registered and pass the resource
        self.__handler = urlparse(targetURL).path
        self.__handler(resource)        #invoke the handler global 
    
    # match returns the supplied URL. Supplying None returns all Observers
    def get(self, targetURI):
        if targetURI != None:
            if targetURI in self.__observers:
                return targetURI
            return None
        return self.__observers
        
    # map the set operation to the create operation
    def set(self, targetURI):
        self.create(targetURI)
    
    # create adds an observer to the list, echoes URI if created or exists
    def create(self, targetURI):
        if urlparse(targetURI).scheme not in self.__schemes:
            return None
        if targetURI not in self.__observers :
            self.__observers += targetURI # append to the list
        return targetURI

    # delete removes an observer from the list, echoes None for failure
    def delete(self, targetURI):
        if targetURI in self.__observers :
            self.__observers.remove(targetURI)
            return targetURI
        return None
    
    