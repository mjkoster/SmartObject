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
    
    # Description method returns triples can be invoked via the 
    # property interface: SmartObject.Description  
    # Does the property decorator work for this?
    def __get__(self, (s,p,o)):
        return self.triples((s,p,o))
    
    def __set__(self, (s,p,o)):
        self.set((s,p,o))
        return
    
    def get(self, (s,p,o)):
        return self.triples((s,p,o))
    
    def set(self, (s,p,o)):
        self.set((s,p,o))
        return
    
    def create(self, (s,p,o)):
        self.add((s,p,o))
        return
    
    def delete(self, (s,p,o)):
        self.remove((s,p,o))
        return
    
    def parse(self,source,fmt):
        g = Graph()
        return g.parse(source,format=fmt)
    
    def serialize(self,graph,fmt):
        return graph.serialize(format=fmt)
    
    
        