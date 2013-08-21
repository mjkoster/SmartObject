'''
Created on July 26, 2013

Example service created for a weather sensor. An Arduino POSTs simple JSON value-only updates to the
REST endpoints defined by the Observable Property created for each sensor output. An example graph is 
created to demonstrate how endpoints can be discovered by reading the graph meta data

@author: mjkoster
'''
from SmartObject.SmartObject import SmartObject
from SmartObject.Description import Description
from SmartObject.ObservableProperty import ObservableProperty
from SmartObject.Observers import Observers
from SmartObject.PropertyOfInterest import PropertyOfInterest
from SmartObject.Agent import AppHandler
from rdflib.term import Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, OWL
from SmartObjectService import SmartObjectService
from time import sleep
import sys


# simple print handler that echoes the value each time an observed resource is updated
class printHandler(AppHandler):
    def _handleNotify(self, resource) :
        print resource.resources['resourceName'], ' = ', resource.get()
        

if __name__ == '__main__' :
    print 'path = ', sys.path
    baseObject = SmartObject() # create a Smart Object to serve as the base container for other Smart Objects and resources
    server = SmartObjectService(baseObject,8000) # make an instance of the service to listen on port 8000, baseObject is the object root
    server.start() # forks a server thread
    print 'httpd started at', server.resources['httpService']

    # set the default class for web API calls to create Smart Objects as named resources       
    baseObject.defaultClass = 'SmartObject'
    # and create a Description resource for the RDF registry
    baseObject.description = baseObject.resources['Description']        
    # create the weather station resource template
    # first the description 
    baseObject.description.set((URIRef('sensors/rhvWeather-01'), RDFS.Class, Literal('SmartObject')))
    baseObject.description.set((URIRef('sensors/rhvWeather-01'), RDFS.Resource, Literal('SensorSystem')))
    baseObject.description.set((URIRef('sensors/rhvWeather-01'), RDF.type, Literal('WeatherSensor')))
        
    baseObject.sensors = baseObject.create('sensors') # top level object container for sensors, default class is SmartObject
    sensors = baseObject.sensors    
    sensors.defaultClass = 'SmartObject' # defaultClass is class for creating named objects 
    sensors.description = sensors.create('Description')
        
    weather = sensors.create('rhvWeather-01') # create a default class SmartObject for the weather sensor cluster
    weather.description = weather.resources['Description'] # create a Description and build an example graph

    weather.description.set((URIRef('sensors/rhvWeather-01/outdoor_temperature'), RDFS.Resource, Literal('sensor')))
    weather.description.set((URIRef('sensors/rhvWeather-01/outdoor_temperature'), RDF.type, Literal('temperature')))
    weather.description.set((URIRef('sensors/rhvWeather-01/outdoor_humidity'), RDFS.Resource, Literal('sensor')))
    weather.description.set((URIRef('sensors/rhvWeather-01/outdoor_humidity'), RDF.type, Literal('humidity')))
    weather.description.set((URIRef('sensors/rhvWeather-01/sealevel_pressure'), RDFS.Resource, Literal('sensor')))
    weather.description.set((URIRef('sensors/rhvWeather-01/sealevel_pressure'), RDF.type, Literal('pressure')))
    weather.description.set((URIRef('sensors/rhvWeather-01/indoor_temperature'), RDFS.Resource, Literal('sensor')))
    weather.description.set((URIRef('sensors/rhvWeather-01/indoor_temperature'), RDF.type, Literal('temperature')))
    weather.description.set((URIRef('sensors/rhvWeather-01/indoor_humidity'), RDFS.Resource, Literal('sensor')))
    weather.description.set((URIRef('sensors/rhvWeather-01/indoor_humidity'), RDF.type, Literal('humidity')))
    weather.description.set((URIRef('sensors/rhvWeather-01/wind_gust'), RDFS.Resource, Literal('sensor')))
    weather.description.set((URIRef('sensors/rhvWeather-01/wind_gust'), RDF.type, Literal('speed')))
    weather.description.set((URIRef('sensors/rhvWeather-01/wind_speed'), RDFS.Resource, Literal('sensor')))
    weather.description.set((URIRef('sensors/rhvWeather-01/wind_speed'), RDF.type, Literal('speed')))
    weather.description.set((URIRef('sensors/rhvWeather-01/wind_direction'), RDFS.Resource, Literal('sensor')))
    weather.description.set((URIRef('sensors/rhvWeather-01/wind_direction'), RDF.type, Literal('direction')))
    weather.description.set((URIRef('sensors/rhvWeather-01/current_rain'), RDFS.Resource, Literal('sensor')))
    weather.description.set((URIRef('sensors/rhvWeather-01/current_rain'), RDF.type, Literal('depth')))
    weather.description.set((URIRef('sensors/rhvWeather-01/hourly_rain'), RDFS.Resource, Literal('sensor')))
    weather.description.set((URIRef('sensors/rhvWeather-01/hourly_rain'), RDF.type, Literal('depth')))
    weather.description.set((URIRef('sensors/rhvWeather-01/daily_rain'), RDFS.Resource, Literal('sensor')))
    weather.description.set((URIRef('sensors/rhvWeather-01/daily_rain'), RDF.type, Literal('depth')))
    
    # now create an Observable Property for each sensor output

    weather.outdoor_temperature = weather.create('outdoor_temperature')        
    weather.outdoor_humidity = weather.create('outdoor_humidity')        
    weather.pressure = weather.create('sealevel_pressure')        
    weather.indoor_temperature = weather.create('indoor_temperature')        
    weather.indoor_humidity = weather.create('indoor_humidity')        
    weather.wind_gust = weather.create('wind_gust')        
    weather.wind_speed = weather.create('wind_speed')        
    weather.wind_direction = weather.create('wind_direction')        
    weather.current_rain = weather.create('current_rain') 
    weather.hourly_rain = weather.create('hourly_rain') 
    weather.daily_rain = weather.create('daily_rain')
        
        
    # test the simple http observer publisher 
    # make a named observer resource
    httpPressureObserver = weather.pressure.resources['Observers'].create('httpPressureObserver')
    # configure the Observer to be an httpObserver and it's URI to PUT updates to
    # the publisher will use the scheme specified and update the URL endpoint whenever the OP is updated
    httpPressureObserver.set({'observerClass': 'httpObserver', \
                              'targetURI': 'http://localhost:8000/sensors/rhvWeather-01/outdoor_temperature'})


    # test the http Subscriber, which creates a remote observer at the location observerURI
    # make a named subscriber resource
    humiditySubscriber = weather.outdoor_humidity.resources['Observers'].create('humiditySubscriber')
    # configure the subscriber to create a remote Observer
    humiditySubscriber.set({'observerClass': 'httpSubscriber', \
                          'observerURI': 'http://localhost:8000/sensors/rhvWeather-01/sealevel_pressure', \
                          'observerName': 'humiditySubObserver' })


    # test the creation of agents and handlers
    weatherAgent = weather.resources['Agent'] # get a handle to the Agent resource
    testHandler = weatherAgent.create('testHandler') # create a handler resource (default class in Agent)
    #  make a code instance and configure the settings
    testHandler.set({'handlerClass': 'SmartObject.Agent.additionHandler', \
                     'addendLink1':'sensors/rhvWeather-01/indoor_temperature', \
                     'addendLink2': 'sensors/rhvWeather-01/indoor_temperature', \
                     'sumOutLink': 'sensors/rhvWeather-01/outdoor_humidity'})     
    # now create an Observers resource and a callback observer endpoint 
    callbackTempObserver = weather.indoor_temperature.resources['Observers'].create('callbackTempObserver')
    # configure the Observer to be a callback observer pointing to the testHandler
    callbackTempObserver.set({'observerClass': 'callbackObserver', \
                              'handlerURI': 'callback:///sensors/rhvWeather-01/Agent/testHandler'})


    # test the use of the class defined in this file for a handler instance
    printHandler = weatherAgent.create('printHandler')    
    printHandler.set({'handlerClass': 'WeatherSensorExample.printHandler'})
    #printHandler.set({'handlerClass': 'SmartObject.Agent.printHandler'})
    tempPrintObserver = weather.indoor_temperature.resources['Observers'].create('tempPrintObserver')
    tempPrintObserver.set({'observerClass': 'callbackObserver', \
                          'handlerURI': 'callback:///sensors/rhvWeather-01/Agent/printHandler'})

    try:
    # register handlers etc.
        while 1: sleep(1)
    except KeyboardInterrupt: pass
    print 'got KeyboardInterrupt'

    