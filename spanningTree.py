import sys

# Classes
class Network: 
    
    def __init__(self, nodes=None, spanningTree=None):
        if nodes == None: 
            self.nodes = []
        else: 
            self.nodes = nodes
        if spanningTree == None: 
            self.spanningTree = []
        else: 
            self.spanningTree = spanningTree

class Node:
    
    def __init__(self, name, nodeID, links=None, rootLink=None, msgCnt=0):
        self.name = name
        self.nodeID = nodeID
        if links == None: 
            self.links = []
        else: 
            self.links = links
        if rootLink == None: 
            self.rootLink = self
        else: 
            self.rootLink = rootLink
        if msgCnt == None: 
            self.msgCnt = 0
        else: 
            self.msgCnt = msgCnt


class Link:
    
    def __init__(self, cost, msgs=None):
        self.cost = cost
        if msgs == None:
            self.msgs = []
        else: 
            self.msgs = msgs

class Message:
    
    def __init__(self, rootID, sumCosts=0):
        self.rootID = rootID
        self.sumCosts = sumCosts
