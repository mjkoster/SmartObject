'''
Created on Sep 15, 2012

Observers class for observation of changes in a resource

Updated July 28, 2013 MJK - made a simple http ObserverPublisher prototype
Updated Aug 17, 2013 MJK - implemented new Observers-Observer pattern using config settings from dict(JSON)

To use the observer, create a resource endpoint using http PUT, http POST or the Python API,
consisting of a URL string in the Observers resource. For example:

PUT /.../resource/Observer "http://<server>/<path>" 

creates an http publisher that updates the endpoint at the specified URL with a JSON object 
representing the value of the Observable Property whenever the Observable Property is updated

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
    def __init__(self, parentObject=None):
        RESTfulResource.__init__(self, parentObject)
        self._settings = {}
        self._observerClass = None
        self._observerInstance = None
        self._settings.update({'observerClass': None})
        self._baseObject = parentObject
        self._baseObjectDict = parentObject.resources['baseObject'].resources

    def get(self, Key=None):
        if Key != None :
            return self._settings[Key]
        else :
            return self._settings
        
    def set(self, newSettings):
        self._settings.update(newSettings)
        if newSettings.has_key('observerClass'):
            if newSettings['observerClass'] != self._observerClass: # create a new instance if observerClass is being set
                self._observerClass = self._settings['observerClass']
                self._observerInstance = self.newObserverInstance(self._settings)
                self._notify = self._observerInstance.notify #reflect the handler back 
    
    def newObserverInstance(self, settings): # make an instance, pass in the settings dict and return the handle
        if settings['observerClass'] == 'httpObserver' :
            return httpObserver(settings)
        if settings['observerClass'] == 'coapObserver' :
            return coapObserver(settings)
        if settings['observerClass'] == 'mqttObserver' :
            return mqttObserver(settings)
        if settings['observerClass'] == 'callbackObserver' :
            return callbackObserver(settings, self._baseObjectDict)
        if settings['observerClass'] == 'httpSubscriber' :
            return httpSubscriber(settings)
        
        
    def _notify(self, resource):
        pass
        
    def notify(self, resource):
        self._notify(resource)
        
        
class httpObserver(object):
    def __init__(self, settings):
        self._settings = settings
        self._httpHeader = {"Content-Type" : "application/json" }
        
    def notify(self,resource): # JSON only for now
        self._jsonObject = json.dumps(resource.get())
        self._uriObject = urlparse(self._settings['targetURI'])
        self._httpConnection = httplib.HTTPConnection(self._uriObject.netloc)
        self._httpConnection.request('PUT', self._uriObject.path, self._jsonObject, self._httpHeader)
        return

class coapObserver(object):
    def __init__(self, settings):
        pass
    
class mqttObserver(object):
    def __init__(self, settings):
        pass

class callbackObserver(object):
    def __init__(self, settings, linkBaseDict):
        self._settings = settings
        self._linkBaseDict = linkBaseDict
    
    def notify(self,resource=None): # invoke the handler
        self.linkToRef(urlparse(self._settings['handlerURI']).path).handleNotify(resource)
        return
    
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

class httpSubscriber(object):
    def __init__(self, settings):
        self._settings = settings
        self._subscriberURI = self._settings['subscriberURI']
        self._observerURI = self._settings['observerURI']
        self._observerName = self._settings['observerName']
        self._observerSettings = {'observerClass': 'httpObserver'}
        self._observerSettings.update({'targetURI': self._settings['subscriberURI']})

        self._httpHeader = {} 
        self._jsonHeader = {"Content-Type" : "application/json" }        
        self._uriObject = urlparse(self._observerURI)
        self._httpConnection = httplib.HTTPConnection(self._uriObject.netloc)
        # create the named resource for the Observer
        self._httpConnection.request('POST', self._uriObject.path + '/Observers', self._observerName, self._httpHeader)
        self._httpConnection.getresponse()
        # configure the Observer
        #self._httpConnection = httplib.HTTPConnection(self._uriObject.netloc)
        self._httpConnection.request('PUT', self._uriObject.path + '/Observers' + '/' + self._observerName, \
                                     json.dumps(self._observerSettings), self._jsonHeader)
        self._httpConnection.getresponse()
        return

    def notify(self, resource):
        pass
    
    
class Observers(RESTfulResource): # the Observers resource is a container for individual named Observer resources
    
    def __init__(self, parentObject=None):
        RESTfulResource.__init__(self, parentObject)
        self.defaultClass = 'Observer'
        self._observers = {}
               
    def onUpdate(self,resource):
        self._onUpdate(resource)
        
    def _onUpdate(self, resource):
        for observer in self._observers.keys():
            self._observers[observer].notify(resource)

    def get(self, Key=None):
        if Key == None :
            return self._observers.keys() # if no URI specified then return all observers
        return self._observer[Key] #return a handle to the observer object for python API
    
    # map the set operation to the create operation
    def set(self, observerName):
        self.create(observerName)
    
    # create adds an observer to the list FIXME use RESTfulResource create method
    def create(self, resourceName, className=None ) : 
        if resourceName not in self.resources :
            if className == None :
                if resourceName in self.wellKnownClasses :
                    className = resourceName
                else :
                    className = self.defaultClass 
                    # create new instance of the named class and add to resources directory, return the ref
            self.resources.update({resourceName : globals()[className](self)}) 
            self.resources[resourceName].resources.update({'resourceName': resourceName})
            self._observers.update({resourceName: self.resources['resourceName']})
        return self.resources[resourceName] # returns a reference to the created instance


    # delete removes an observer from the list, echoes None for failure
    def delete(self, observerName):
        if observerName in self._observers.keys() :
            self._observers.remove(observerName)
            self.resources.remove(observerName)
            return observerName
        return None
    
    