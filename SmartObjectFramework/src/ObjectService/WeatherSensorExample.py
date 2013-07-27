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
       
    baseObject.defaultClass = 'SmartObject'
    # Use a smart object instance as a container for SmartObjects 
    # and create a Description resource for the RDF registry
    baseObject.description = baseObject.create('Description')
        
    # create the weather station resource template
    # first the description 
    baseObject.description.set((URIRef('sensors/rhvWeather-01'), RDFS.Class, Literal('SensorSystem')))
    baseObject.description.set((URIRef('sensors/rhvWeather-01'), RDF.type, Literal('WeatherSensor')))
    baseObject.description.set((URIRef('sensors/rhvWeather-01'), RDFS.Resource, Literal('SmartObject')))
        
    baseObject.sensors = baseObject.create('sensors') # top level object container for sensors, default class is SmartObject
    sensors = baseObject.sensors
    sensors.description = baseObject.sensors.create('Description')
        
    sensors.weather = sensors.create('rhvWeather-01', 'SmartObject') # create a SmartObject for the weather sensor cluster
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
    
    # now create an Observable Property for each sensor output, each with a PropertyOfInterest class to hold the observation values

    sensors.weather.outdoor_temperature = sensors.weather.create('outdoor_temperature', 'ObservableProperty')
    sensors.weather.outdoor_temperature.create('PropertyOfInterest')
        
    sensors.weather.outdoor_humidity = sensors.weather.create('outdoor_humidity', 'ObservableProperty')
    sensors.weather.outdoor_humidity.create('PropertyOfInterest')
        
    sensors.weather.pressure = sensors.weather.create('sealevel_pressure', 'ObservableProperty')
    sensors.weather.pressure.create('PropertyOfInterest')
        
    sensors.weather.indoor_temperature = sensors.weather.create('indoor_temperature', 'ObservableProperty')
    sensors.weather.indoor_temperature.create('PropertyOfInterest')
        
    sensors.weather.indoor_humidity = sensors.weather.create('indoor_humidity', 'ObservableProperty')
    sensors.weather.indoor_humidity.create('PropertyOfInterest')
        
    sensors.weather.wind_gust = sensors.weather.create('wind_gust', 'ObservableProperty')
    sensors.weather.wind_gust.create('PropertyOfInterest')
        
    sensors.weather.wind_speed = sensors.weather.create('wind_speed', 'ObservableProperty')
    sensors.weather.wind_speed.create('PropertyOfInterest')
        
    sensors.weather.wind_direction = sensors.weather.create('wind_direction', 'ObservableProperty')
    sensors.weather.wind_direction.create('PropertyOfInterest')
        
    sensors.weather.current_rain = sensors.weather.create('current_rain', 'ObservableProperty')
    sensors.weather.current_rain.create('PropertyOfInterest')
 
    sensors.weather.hourly_rain = sensors.weather.create('hourly_rain', 'ObservableProperty')
    sensors.weather.hourly_rain.create('PropertyOfInterest')
 
    sensors.weather.daily_rain = sensors.weather.create('daily_rain', 'ObservableProperty')
    sensors.weather.daily_rain.create('PropertyOfInterest')
        
    server.start()
    print 'httpd started'

    try:
    # register handlers etc.
        while 1: sleep(1)
    except KeyboardInterrupt: pass
    print 'got KeyboardInterrupt'

    