'''
Created on Sep 15, 2012

Agent class. Contains reference to instance of 
class containing observer handlers and agent code 

Contains references to observer handlers

@author: mjkoster
'''

from RESTfulResource import RESTfulResource

class Agent(RESTfulResource):
    
    def __init__(self, agent):
        RESTfulResource.__init__(self)
        # reference to the code class to create an instance of 
        # can be passed in, or default on init, or be changed later
        if agent != None :
            self.create(agent)
        else :
            self.__agent = self # self what? FIXME
        # references to handler methods in the code class for observer notifications
        self.__handlers = []
        
    def __del__(self): # clean up any references on removal of agent
        pass
    
    @property
    def agent(self):
        return self.__agent
    @agent.setter
    def agent(self, agent): # creates a new agent
        self.__handlers.clear # no observers
        self.create(agent)
        return
    @agent.deleter
    def agent (self, agent):
        self.delete(agent)
    
    @property
    def handlers(self):
        return self.__handlers
    @handlers.setter
    def handlers(self, handler):
        self.__handlers += handler
        return
    @handlers.deleter
    def handlers(self, handler):
        if handler in self.__handlers:
            self.__handlers.remove(handler)
            return handler
        return None # return none to indicate no match
        
        
    def get(self):
        return self.__handlers
    
    def set(self, handler):
        self.__handlers += handler
        return
    
    def create(self, agent):
        self.__agent = agent()
        return
        
    def delete(self, agent):
        self.handlers.clear
        return
        # need to import and create instance of code module
        # creating instance init module should register observers as needed
        
        