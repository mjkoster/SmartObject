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
               
    def onUpdate(self,resource):
        self.__onUpdate(resource)
        
    def __onUpdate(self, resource):
        for self.__observer in self.__observers:
            self.__notify(self.__observer, resource)
    
    def __notify(self, observer, resource):
        if type(observer) is not callable : # FIX this
            urlObject = urlparse(observer)
            if urlObject.scheme == 'http' :
                self.__httpNotify(observer, resource)
            elif urlObject.scheme == 'coap' :
                self.__coapNotify(observer, resource)
            elif urlObject.scheme == 'callback' :
                self.__callbackNotify(observer, resource)
        else : 
            observer(resource) # if it's a callable object
            
            
    def __httpNotify(self, targetURI, resource):
        # invoke method from http client interface
        # self.__httpNotifyHandler(targetURI, resource)
        print 'http notify stub'
    
    def __coapNotify(self, targetURI, resource):
        # invoke method from CoAP server interface
        # self.__coapNotifyHandler(targetURI, resource)
        print 'coap notify stub'
    
    def __callbackNotify(self, observer, resource):
        #call the function registered and pass the resource
        #invoke the handler through the Agent resource
        print 'callback notify stub'
    
    # match returns the supplied URL, else none. Supplying None returns all Observers
    def get(self, targetURI=None):
        if targetURI != None:
            if targetURI in self.__observers:
                return targetURI
            return None
        return self.__observers # if no URI specified then return all observers
        
    # map the set operation to the create operation
    def set(self, targetURI):
        self.create(targetURI)
    
    # create adds an observer to the list, echoes URI if created or exists
    def create(self, targetURI):
        if urlparse(targetURI).scheme not in self.__schemes:
            return None
        if targetURI not in self.__observers :
            self.__observers.append(targetURI) # append to the list
        return targetURI

    # delete removes an observer from the list, echoes None for failure
    def delete(self, targetURI):
        if targetURI in self.__observers :
            self.__observers.remove(targetURI)
            return targetURI
        return None
    
    