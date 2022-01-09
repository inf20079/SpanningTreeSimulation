import sys
import json
from threading import Thread
from typing import NewType

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

    def print():
        pass

    @classmethod
    def from_graph_txt(cls, path):
        
        nodes = []
        links = []
        with open(path, 'r') as graph:
            for line in graph:
                if '=' in line:
                    line = line.replace(' ', '')
                    line = line.replace(';', '')
                    nodes.append(Node(line[0], int(line[2])))
                if ':' in line:
                    line = line.replace(' ', '')
                    line = line.replace(';', '')
                    links.append(Link(line[0], line[2], int(line[4:])))
        for node in nodes:
            links_for_node = []
            for link in links:
                if node.name == link.leftEnd or node.name == link.rightEnd:
                    links_for_node.append(link)
            node.links = links_for_node
        return cls(nodes)

    def printData(self):
        print("Network: spanningTree={}, nodes:". format(self.spanningTree))
        for node in self.nodes:
            node.printData()


class Node:
    
    def __init__(self, name, nodeID, links=None, rootLink=None, msgCnt=0):
        self.name = name
        self.nodeID = nodeID
        if links == None: 
            self.links = []
        else: 
            self.links = links
        if rootLink == None: 
            self.rootLink = nodeID
        else: 
            self.rootLink = rootLink
        if msgCnt == None: 
            self.msgCnt = 0
        else: 
            self.msgCnt = msgCnt

    def printData(self):
        print("Node: name={}, nodeID={}, rootLink={}, msgCnt={}, links:". format(self.name, self.nodeID, self.rootLink, self.msgCnt))
        for link in self.links:
            link.printData()


class Link:
    
    def __init__(self, leftEnd, rightEnd, cost, msgs=None):
        self.leftEnd = leftEnd
        self.rightEnd = rightEnd
        self.cost = cost
        if msgs == None:
            self.msgs = []
        else: 
            self.msgs = msgs

    def printData(self):
        print("Link: leftEnd={}, rightEnd={}, cost={}, msgs:". format(self.leftEnd, self.rightEnd, self.cost))
        for msg in self.msgs:
            msg.printData()


class Message:
    
    def __init__(self, source, destination, rootID, sumCosts=0):
        self.source = source
        self.destination = destination
        self.rootID = rootID
        self.sumCosts = sumCosts

    def printData(self):
        print("Message: Source={}, Destination={}, rootID={}, sumCosts={}".format(self.source, self.destination, self.rootID, self.sumCosts))

if __name__ == "__main__":
    network = Network.from_graph_txt('./Inputdateien/graph.txt')
    network.exportJSON('./Inputdateien/abnd.txt')