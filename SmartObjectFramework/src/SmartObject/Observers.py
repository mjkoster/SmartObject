'''
Created on Sep 15, 2012

Observers class for observation of changes in a resource

@author: mjkoster
'''
from RESTfulResource import RESTfulResource

class Observers(RESTfulResource):
    
    def __init__(self):
        RESTfulResource.__init__(self)