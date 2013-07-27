'''
Created on Oct 1, 2012

Service layer for SmartObjects usable for any RESTful objects 
Adds registry and methods for creating and removing objects

The service is itself based on a SmartObject resource pattern with 
SmartObjects as the created resources and a default Description 
resource containing descriptions of and links to the created 
SmartObjects

@author: mjkoster
'''
from SmartObject.SmartObject import SmartObject
from SmartObject.Description import Description
from SmartObject.ObservableProperty import ObservableProperty
from SmartObject.Observers import Observers
from SmartObject.PropertyOfInterest import PropertyOfInterest
from rdflib.term import Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, OWL

class ObjectService(SmartObject):

    def __init__(self):
        SmartObject.__init__(self) # initialize the service as a Smart Object
        import __builtin__
        __builtin__.SmartObjectServiceBaseDict = self.resources # make this a global reference
        
        self.defaultClass = 'SmartObject'
        # Use a smart object instance as a container for SmartObjects 
        # and create a Description resource for the RDF registry
        self.description = self.create('Description')
        
        # create the weather station resource template
        # first the description 
        
        self.description.set((URIRef('sensors/rhvWeather-01'), RDFS.Class, Literal('SensorSystem')))
        self.description.set((URIRef('sensors/rhvWeather-01'), RDF.type, Literal('WeatherSensor')))
        self.description.set((URIRef('sensors/rhvWeather-01'), RDFS.Resource, Literal('SmartObject')))
        
        self.sensors = self.create('sensors') # top level object
        self.sensors.description = self.sensors.create('Description')
        
        self.sensors.weather = self.sensors.create('rhvWeather-01', 'SmartObject')
        self.sensors.weather.description = self.sensors.weather.create('Description')

        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/outdoor_temperature'), RDFS.Resource, Literal('sensor')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/outdoor_temperature'), RDF.type, Literal('temperature')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/outdoor_humidity'), RDFS.Resource, Literal('sensor')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/outdoor_humidity'), RDF.type, Literal('humidity')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/sealevel_pressure'), RDFS.Resource, Literal('sensor')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/sealevel_pressure'), RDF.type, Literal('pressure')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/indoor_temperature'), RDFS.Resource, Literal('sensor')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/indoor_temperature'), RDF.type, Literal('temperature')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/indoor_humidity'), RDFS.Resource, Literal('sensor')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/indoor_humidity'), RDF.type, Literal('humidity')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/wind_gust'), RDFS.Resource, Literal('sensor')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/wind_gust'), RDF.type, Literal('speed')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/wind_speed'), RDFS.Resource, Literal('sensor')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/wind_speed'), RDF.type, Literal('speed')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/wind_direction'), RDFS.Resource, Literal('sensor')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/wind_direction'), RDF.type, Literal('direction')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/current_rain'), RDFS.Resource, Literal('sensor')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/current_rain'), RDF.type, Literal('depth')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/hourly_rain'), RDFS.Resource, Literal('sensor')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/hourly_rain'), RDF.type, Literal('depth')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/daily_rain'), RDFS.Resource, Literal('sensor')))
        self.sensors.weather.description.set((URIRef('sensors/rhvWeather-01/daily_rain'), RDF.type, Literal('depth')))

        self.sensors.weather.outdoor_temperature = self.sensors.weather.create('outdoor_temperature', 'ObservableProperty')
        self.sensors.weather.outdoor_temperature.create('PropertyOfInterest')
        
        self.sensors.weather.outdoor_humidity = self.sensors.weather.create('outdoor_humidity', 'ObservableProperty')
        self.sensors.weather.outdoor_humidity.create('PropertyOfInterest')
        
        self.sensors.weather.pressure = self.sensors.weather.create('sealevel_pressure', 'ObservableProperty')
        self.sensors.weather.pressure.create('PropertyOfInterest')
        
        self.sensors.weather.indoor_temperature = self.sensors.weather.create('indoor_temperature', 'ObservableProperty')
        self.sensors.weather.indoor_temperature.create('PropertyOfInterest')
        
        self.sensors.weather.indoor_humidity = self.sensors.weather.create('indoor_humidity', 'ObservableProperty')
        self.sensors.weather.indoor_humidity.create('PropertyOfInterest')
        
        self.sensors.weather.wind_gust = self.sensors.weather.create('wind_gust', 'ObservableProperty')
        self.sensors.weather.wind_gust.create('PropertyOfInterest')
        
        self.sensors.weather.wind_speed = self.sensors.weather.create('wind_speed', 'ObservableProperty')
        self.sensors.weather.wind_speed.create('PropertyOfInterest')
        
        self.sensors.weather.wind_direction = self.sensors.weather.create('wind_direction', 'ObservableProperty')
        self.sensors.weather.wind_direction.create('PropertyOfInterest')
        
        self.sensors.weather.current_rain = self.sensors.weather.create('current_rain', 'ObservableProperty')
        self.sensors.weather.current_rain.create('PropertyOfInterest')
 
        self.sensors.weather.hourly_rain = self.sensors.weather.create('hourly_rain', 'ObservableProperty')
        self.sensors.weather.hourly_rain.create('PropertyOfInterest')
 
        self.sensors.weather.daily_rain = self.sensors.weather.create('daily_rain', 'ObservableProperty')
        self.sensors.weather.daily_rain.create('PropertyOfInterest')
        
        
        
    