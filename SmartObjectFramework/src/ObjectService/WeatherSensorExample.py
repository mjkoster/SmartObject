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
from rdflib.term import Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, OWL
from SmartObjectService import SmartObjectService
from time import sleep

if __name__ == '__main__' :
    
    baseObject = SmartObject() # create a Smart Object to serve as the base container for other Smart Objects and resources

    server = SmartObjectService(baseObject,8000) # make an instance of the service to listen on port 8000, baseObject is the object root
    print 'Service created'
    # set the default class for web API calls to create Smart Objects as named resources       
    baseObject.defaultClass = 'SmartObject'
    # and create a Description resource for the RDF registry
    baseObject.description = baseObject.create('Description')
    # this will create a resource of class Description rather than the default class because the name matches a well known class
        
    # create the weather station resource template
    # first the description 
    baseObject.description.set((URIRef('sensors/rhvWeather-01'), RDFS.Class, Literal('SmartObject')))
    baseObject.description.set((URIRef('sensors/rhvWeather-01'), RDFS.Resource, Literal('SensorSystem')))
    baseObject.description.set((URIRef('sensors/rhvWeather-01'), RDF.type, Literal('WeatherSensor')))
        
    baseObject.sensors = baseObject.create('sensors') # top level object container for sensors, default class is SmartObject
    sensors = baseObject.sensors
    
    sensors.defaultClass = 'SmartObject' # defaultClass is class for creating named objects 
    sensors.description = sensors.create('Description')
        
    sensors.weather = sensors.create('rhvWeather-01') # create a default class SmartObject for the weather sensor cluster
    sensors.weather.description = sensors.weather.create('Description') # create a Description and build an example graph

    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/outdoor_temperature'), RDFS.Resource, Literal('sensor')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/outdoor_temperature'), RDF.type, Literal('temperature')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/outdoor_humidity'), RDFS.Resource, Literal('sensor')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/outdoor_humidity'), RDF.type, Literal('humidity')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/sealevel_pressure'), RDFS.Resource, Literal('sensor')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/sealevel_pressure'), RDF.type, Literal('pressure')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/indoor_temperature'), RDFS.Resource, Literal('sensor')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/indoor_temperature'), RDF.type, Literal('temperature')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/indoor_humidity'), RDFS.Resource, Literal('sensor')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/indoor_humidity'), RDF.type, Literal('humidity')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/wind_gust'), RDFS.Resource, Literal('sensor')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/wind_gust'), RDF.type, Literal('speed')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/wind_speed'), RDFS.Resource, Literal('sensor')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/wind_speed'), RDF.type, Literal('speed')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/wind_direction'), RDFS.Resource, Literal('sensor')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/wind_direction'), RDF.type, Literal('direction')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/current_rain'), RDFS.Resource, Literal('sensor')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/current_rain'), RDF.type, Literal('depth')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/hourly_rain'), RDFS.Resource, Literal('sensor')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/hourly_rain'), RDF.type, Literal('depth')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/daily_rain'), RDFS.Resource, Literal('sensor')))
    sensors.weather.description.set((URIRef('sensors/rhvWeather-01/daily_rain'), RDF.type, Literal('depth')))
    
    # now create an Observable Property for each sensor output

    sensors.weather.outdoor_temperature = sensors.weather.create('outdoor_temperature', 'ObservableProperty')        
    sensors.weather.outdoor_humidity = sensors.weather.create('outdoor_humidity', 'ObservableProperty')        
    sensors.weather.pressure = sensors.weather.create('sealevel_pressure', 'ObservableProperty')        
    sensors.weather.indoor_temperature = sensors.weather.create('indoor_temperature', 'ObservableProperty')        
    sensors.weather.indoor_humidity = sensors.weather.create('indoor_humidity', 'ObservableProperty')        
    sensors.weather.wind_gust = sensors.weather.create('wind_gust', 'ObservableProperty')        
    sensors.weather.wind_speed = sensors.weather.create('wind_speed', 'ObservableProperty')        
    sensors.weather.wind_direction = sensors.weather.create('wind_direction', 'ObservableProperty')        
    sensors.weather.current_rain = sensors.weather.create('current_rain', 'ObservableProperty') 
    sensors.weather.hourly_rain = sensors.weather.create('hourly_rain', 'ObservableProperty') 
    sensors.weather.daily_rain = sensors.weather.create('daily_rain', 'ObservableProperty')
        
    # test the simple http observer publisher
    # first make an Observers resource for the Observable Property to be monitored
    pressure_observer = sensors.weather.pressure.create('Observers')
    # then create (or set) a URL endpoint to publish to, including the scheme
    pressure_observer.create('http://localhost:8000/sensors/rhvWeather-01/outdoor_temperature')
    # the publisher will use the scheme specified and update the URL endpoint whenever the OP is updated
    
    # test the creation of agents and handlers
    weatherAgent = sensors.weather.create('Agent') # create the Agent resource
    testHandler = weatherAgent.create('testHandler') # create a handler (default class in Agent)
    testHandler._objectPathBaseDict = baseObject.resources # hack to get a reference for object root
    testHandler.create('SmartObject.Agent.additionHandler') # associate an AppHandler subclass and make a code instance
    # hook up the property links to properties
    testHandler.settings()['addendLink1'] = 'sensors/rhvWeather-01/indoor_temperature'
    testHandler.settings()['addendLink2'] = 'sensors/rhvWeather-01/indoor_temperature'    
    testHandler.settings()['sumOutLink'] = 'sensors/rhvWeather-01/outdoor_humidity'
    # now create an Observers resource and a callback observer endpoint to invoke the handler on resource updates
    tempObserver = sensors.weather.indoor_temperature.create('Observers')
    tempObserver._linkBaseDict = baseObject.resources # hack base object in here too
    tempObserver.create('callback://local/sensors/rhvWeather-01/Agent/testHandler')
        
    server.start() # forks a server thread
    print 'httpd started'

    try:
    # register handlers etc.
        while 1: sleep(1)
    except KeyboardInterrupt: pass
    print 'got KeyboardInterrupt'

    