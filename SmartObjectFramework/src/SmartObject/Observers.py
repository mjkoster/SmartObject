'''
Created on Sep 15, 2012

Observers class for observation of changes in a resource

Updated July 28, 2013 MJK - made a simple http ObserverPublisher prototype
Updated Aug 17, 2013 MJK - implemented new Observers-Observer pattern using config settings from dict(JSON)

To use the observer, create an observer subclass resource endpoint using http POST or the Python API

the observer subclass httpPublisher updates the endpoint at the specified URL with a JSON object 
representing the value of the Observable Property whenever the Observable Property is updated

other observer subclasses are httpSubscriber, which creates a remote httpPublisher, 
and handlerNotifier, which invokes the handleNotify method of handler

It doesn't work if you try to directly update the Property Of Interest

An Observer is created subordinate to the Observers resource, and configured with a particular observer 
class using a PUT (set) of a JSON (dictionary) settings object

@author: mjkoster
'''
from RESTfulResource import RESTfulResource
from urlparse import urlparse
import json
import httplib

class Observer(RESTfulResource):
    def __init__(self, parentObject=None, resourceDescriptor = {}):
        RESTfulResource.__init__(self, parentObject, resourceDescriptor)
        self._settings = {}
        self._baseObject = self.resources['baseObject']
        self._linkBaseDict = self.resources['baseObject'].resources
        self._thisURI =  self.resources['baseObject'].Properties.get('httpService') \
                    + self.resources['parentObject'].resources['parentObject'].Properties.get('pathFromBase')
        self._settings.update({'thisURI': self._thisURI})

    def _updateSettings(self):
        pass

    def get(self, Key=None):
        if Key != None :
            return self._settings[Key]
        else :
            return self._settings
        
    def set(self, newSettings):
        self._settings.update(newSettings) 
        self._updateSettings()       
        
    def notify(self, resource):
        self._notify(resource)
        
    def _notify(self, resource):
        pass

    def linkToRef(self, linkPath ):
        '''
        takes a path string and walks the object tree from a base dictionary
        returns a ref to the resource at the path endpoint
        '''
        self._currentDict = self._linkBaseDict
        self._pathElements = linkPath.split('/')
        for pathElement in self._pathElements[:-1] : # all but the last, which should be the endpoint
            if len(pathElement) > 0 : # first element is a zero length string for some reason
                self._currentDict = self._currentDict[pathElement].resources
        self._resource = self._currentDict[self._pathElements[-1] ]
        return self._resource        


class httpPublisher(Observer):
    def _notify(self,resource): # JSON only for now
        self._jsonObject = json.dumps(resource.get())
        self._uriObject = urlparse(self._settings['targetURI'])
        self._httpConnection = httplib.HTTPConnection(self._uriObject.netloc)
        self._httpConnection.request('PUT', self._uriObject.path, self._jsonObject, {"Content-Type" : "application/json" })
        return


class callbackNotifier(Observer):    
    def _notify(self,resource=None): # invoke the handler
        self.linkToRef(urlparse(self._settings['handlerURI']).path).handleNotify(resource)
        return
    

class httpSubscriber(Observer):
    def _updateSettings(self):
        self._thisURI = self._settings['thisURI']
        self._observerURI = self._settings['observerURI']
        self._observerName = self._settings['observerName']
        self._observerDescriptor = {'resourceName': self._observerName,\
                                    'resourceClass': 'httpPublisher' }
        self._observerSettings = {'targetURI': self._thisURI}
        self._jsonHeader = {"Content-Type" : "application/json" }        
        self._uriObject = urlparse(self._observerURI)
        self._httpConnection = httplib.HTTPConnection(self._uriObject.netloc)
        # create the named resource for the Observer
        self._httpConnection.request('POST', self._uriObject.path + '/Observers', \
                                     json.dumps(self._observerDescriptor), self._jsonHeader)
        self._httpConnection.getresponse()
        # configure the Observer
        self._httpConnection.request('PUT', self._uriObject.path + '/Observers' + '/' + self._observerName, \
                                     json.dumps(self._observerSettings), self._jsonHeader)
        self._httpConnection.getresponse()
        return
    
    
class Observers(RESTfulResource): # the Observers resource is a container for individual named Observer resources
    
    def __init__(self, parentObject=None, resourceDescriptor = {}):
        RESTfulResource.__init__(self, parentObject, resourceDescriptor)
        self._observers = {}
               
    def onUpdate(self,resource):
        self._onUpdate(resource)
        
    def _onUpdate(self, resource):
        for observer in self._observers :
            self._observers[observer].notify(resource)

    def get(self, Key=None):
        if Key == None :
            return self._observers.keys() # if no URI specified then return all observers
        return self._observer[Key] #return a handle to the observer object for python API
    
    # map the set operation to the create operation
    def set(self):
        pass
    
    # new create takes dictionary built from JSON object POSTed to parent resource
    def create(self, resourceDescriptor):
        resourceName = resourceDescriptor['resourceName']
        resourceClass = resourceDescriptor['resourceClass']
        if resourceName not in self.resources:
            # create new instance of the named class and add to resources directory, return the ref
            self.resources.update({resourceName : globals()[resourceClass](self, resourceDescriptor)}) 
            self._observers.update({resourceName: self.resources[resourceName]})            
        return self.resources[resourceName] # returns a reference to the created instance

    # delete removes an observer from the list, echoes None for failure
    def delete(self, observerName):
        if observerName in self._observers.keys() :
            self._observers.remove(observerName)
            self.resources.remove(observerName)
            return observerName
        return None
    
    