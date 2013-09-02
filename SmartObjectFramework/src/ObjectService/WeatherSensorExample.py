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
        print resource.Properties.get('resourceName'), ' = ', resource.get()
        

if __name__ == '__main__' :
    # print 'path = ', sys.path
    baseObject = SmartObject() # create a Smart Object to serve as the base container for other Smart Objects and resources
    server = SmartObjectService(baseObject) # make an instance of the service, baseObject is the object root
    server.start(8000) # forks a server thread to listen on port 8000
    print 'httpd started at', baseObject.Properties.get('httpService')

    # make a reference to thhe baseObject Description resource
    baseObject.description = baseObject.Resources.get('Description')       
    # create the weather station resource template
    # first the description 
    baseObject.description.set((URIRef('sensors/rhvWeather-01'), RDFS.Class, Literal('SmartObject')))
    baseObject.description.set((URIRef('sensors/rhvWeather-01'), RDFS.Resource, Literal('SensorSystem')))
    baseObject.description.set((URIRef('sensors/rhvWeather-01'), RDF.type, Literal('WeatherSensor')))
    
    # sensors resource under the baseObject for all sensors    
    sensors = baseObject.create({'resourceName': 'sensors',\
                                 'resourceClass': 'SmartObject'}) # top level object container for sensors, default class is SmartObject
    #weather resource under sensors for the weather sensor    
    weather = sensors.create({'resourceName': 'rhvWeather-01', \
                             'resourceClass': 'SmartObject'}) # create a default class SmartObject for the weather sensor cluster

    # make a reference to the weather sensor object Description and build an example graph
    weather.description = weather.Resources.get('Description')
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

    outdoor_temperature = weather.create({'resourceName': 'outdoor_temperature',\
                                          'resourceClass': 'ObservableProperty'})
    
    outdoor_humidity = weather.create({'resourceName': 'outdoor_humidity',\
                                        'resourceClass': 'ObservableProperty'})
    
    pressure = weather.create({'resourceName': 'sealevel_pressure',\
                                'resourceClass': 'ObservableProperty'})
    
    indoor_temperature = weather.create({'resourceName': 'indoor_temperature',\
                                          'resourceClass': 'ObservableProperty'})
    
    indoor_humidity = weather.create({'resourceName': 'indoor_humidity',\
                                        'resourceClass': 'ObservableProperty'})
    
    wind_gust = weather.create({'resourceName': 'wind_gust',\
                                'resourceClass': 'ObservableProperty'})
    
    wind_speed = weather.create({'resourceName': 'wind_speed',\
                                  'resourceClass': 'ObservableProperty'})
    
    wind_direction = weather.create({'resourceName': 'wind_direction',\
                                    'resourceClass': 'ObservableProperty'})
    
    current_rain = weather.create({'resourceName': 'current_rain',\
                                    'resourceClass': 'ObservableProperty'})
    
    hourly_rain = weather.create({'resourceName': 'hourly_rain',\
                                  'resourceClass': 'ObservableProperty'})
    
    daily_rain = weather.create({'resourceName': 'daily_rain',\
                                 'resourceClass': 'ObservableProperty'})
 
    # test the simple http observer publisher 
    # make a named observer resource
    httpPressureObserver = pressure.Resources.get('Observers').create({'resourceName': 'httpPressureObserver',\
                                                                  'resourceClass': 'Observer'})  
    # configure the Observer to be an httpObserver and it's URI to PUT updates to
    # the publisher will use the scheme specified and update the URL endpoint whenever the OP is updated
    httpPressureObserver.set({'observerClass': 'httpObserver', \
                              'targetURI': 'http://localhost:8000/sensors/rhvWeather-01/outdoor_temperature'})

    # test the http Subscriber, which creates a remote observer at the location observerURI
    # make a named subscriber resource
    humiditySubscriber = outdoor_humidity.Resources.get('Observers').create({'resourceName': 'humiditySubscriber',\
                                                                         'resourceClass': 'Observer'})
    # configure the subscriber to create a remote Observer
    humiditySubscriber.set({'observerClass': 'httpSubscriber', \
                          'observerURI': 'http://localhost:8000/sensors/rhvWeather-01/sealevel_pressure', \
                          'observerName': 'humiditySubObserver' })

    # test the creation of agents and handlers
    weatherAgent = weather.Resources.get('Agent') # get a handle to the Agent resource
    testHandler = weatherAgent.create({'resourceName': 'testHandler',\
                                       'resourceClass': 'Handler'}) # create a handler resource (default class in Agent)
    #  make a code instance and configure the settings
    testHandler.set({'handlerClass': 'SmartObject.Agent.additionHandler', \
                     'addendLink1':'sensors/rhvWeather-01/indoor_temperature', \
                     'addendLink2': 'sensors/rhvWeather-01/indoor_temperature', \
                     'sumOutLink': 'sensors/rhvWeather-01/outdoor_humidity'})     

    # now create an Observers resource and a callback observer endpoint 
    callbackTempObserver = indoor_temperature.Resources.get('Observers').create({'resourceName': 'callbackTempObserver',\
                                                                                    'resourceClass': 'Observer'})
    # configure the Observer to be a callback observer pointing to the testHandler
    callbackTempObserver.set({'observerClass': 'callbackObserver', \
                              'handlerURI': 'callback:///sensors/rhvWeather-01/Agent/testHandler'})

    # test the use of the class defined in this file for a handler instance
    printHandler = weatherAgent.create({'resourceName': 'printHandler',\
                                       'resourceClass': 'Handler'})    

    printHandler.set({'handlerClass': 'WeatherSensorExample.printHandler'})
    #printHandler.set({'handlerClass': 'SmartObject.Agent.printHandler'})

    tempPrintObserver = indoor_temperature.Resources.get('Observers').create({'resourceName': 'tempPrintObserver',\
                                                                                 'resourceClass': 'Observer'})
    
    tempPrintObserver.set({'observerClass': 'callbackObserver', \
                          'handlerURI': 'callback:///sensors/rhvWeather-01/Agent/logPrintHandler'})

    logPrintHandler = weatherAgent.create({'resourceName': 'logPrintHandler',\
                                           'resourceClass': 'logPrintHandler'})
    
    
    try:
    # register handlers etc.
        while 1: sleep(1)
    except KeyboardInterrupt: pass
    print 'got KeyboardInterrupt'

    