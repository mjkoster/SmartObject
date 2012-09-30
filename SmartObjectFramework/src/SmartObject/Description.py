'''
Created on Sep 15, 2012

Description class which is an instance of RDF graph from the rdflib Graph class
with consistent SmartObject interface methods. The parse and serialize methods 
work on the sub-graphs used by get and set methods for discovery and linkage

@author: mjkoster
'''

from RESTfulResource import RESTfulResource
from rdflib.graph import Graph

class Description (RESTfulResource, Graph):
    
    def __init__(self):
        RESTfulResource.__init__(self)
        Graph.__init__(self)
    
    # Descriptor method returns triples can be invoked via the 
    # property interface: SmartObject.Description  
    # Does the property decorator work for this?
    @property 
    def __get__(self, (s,p,o)):
        return Graph.triples((s,p,o))
    
    @property
    def __set__(self, (s,p,o)):
        Graph.set((s,p,o))
        return
    
    @property
    def get(self, (s,p,o)):
        return Graph.triples((s,p,o))
    
    def set(self, (s,p,o)):
        Graph.set((s,p,o))
        return
    
    def create(self, (s,p,o)):
        Graph.add((s,p,o))
        return
    
    def delete(self, (s,p,o)):
        Graph.remove((s,p,o))
        return
    
    def parse(self,source,fmt):
        g = Graph()
        return g.parse(source,format=fmt)
    
    def serialize(self,graph,fmt):
        return graph.serialize(format=fmt)
    
    
        