'''
Created on Sep 15, 2012

Description class which is an instance of RDF graph from the rdflib Graph class
with consistent SmartObject interface methods. The parse and serialize methods 
work on the sub-graphs used by get and set methods for discovery and linkage

@author: mjkoster
'''

from RESTfulResource import RESTfulResource
from rdflib.graph import Graph
from Observers import Observers

class RespGraph(Graph):
    # add a method to convert to XML for RESTlite represent method
    def _xml_(self):
        return self.serialize(format='xml')
 
class Description (RESTfulResource):
    
    def __init__(self):
        RESTfulResource.__init__(self)
        self.graph = Graph()
        self.parseContentTypes = ['application/rdf+xml', 'text/rdf+n3' ]
        self.serializeContentTypes = [ 'text/xml', 'application/rdf+xml', 'application/x-turtle' , 'text/rdf+n3' ]
        self.fmt = { 'text/xml' : 'xml', 
               'application/rdf+xml' : 'xml',
               'application/x-turtle' : 'turtle',
               'text/rdf+n3' : 'n3',
               'text/plain' : 'nt'
               }
        

    # Description get method returns triples can be invoked via the 
    # property interface: SmartObject.Description  
    # Does the property decorator work for this?

    def get(self, (s,p,o) = (None,None,None)):
        # return a graph consisting of the matching triples
        g = RespGraph()
        for triple in self.graph.triples((s,p,o)) :
            g.add(triple)
        return g
    
    def set(self, newValue):
        self.setTriple(newValue)
    
    def create(self, newValue):    
        self.createTriple(newValue)
    
    def delete(self, newValue):
        self.deleteTriple(newValue)
    
    def setTriple(self, (s,p,o) ):
        self.graph.set((s,p,o))
        return
            
    def createTriple(self, (s,p,o) ):
        self.graph.add( (s,p,o) )
        
    def deleteTriple(self, (s,p,o) ):
        self.graph.remove( (s,p,o) )

    def setGraph(self, g):
        self.graph += g 
        return
    
    def createGraph(self, g):
        self.graph = g
        return
    
    def deleteGraph(self, g):
        self.graph -= g
        return

    # exposed methods for converting sub graphs 
    def parse(self,source, cType):
        g = Graph()
        return g.parse(source,format=self.fmt[cType])
    
    def serialize(self,graph, cType): 
        return graph.serialize(format=self.fmt[cType])
       
    
        