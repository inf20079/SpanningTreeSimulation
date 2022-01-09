from os import name
import sys
from threading import Thread
import argparse

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

        for link in links:
            for node in nodes:
                if node.name == link.leftEnd:
                    link.leftEnd = int(node.nodeID)
                if node.name == link.rightEnd:
                    link.rightEnd = int(node.nodeID)
            if isinstance(link.leftEnd, str) or isinstance(link.rightEnd, str):
                print("Error: This Link has no connection to the network:")
                link.printData()
                exit(1)

        for node in nodes:
            links_for_node = []
            for link in links:
                if node.nodeID == link.leftEnd:
                    links_for_node.append(link)
                if node.nodeID == link.rightEnd:
                    links_for_node.append(link)
            node.links = links_for_node
            if node.links == []:
                print("Error: This node has no connection to the network:")
                node.printData()
                exit(1)

        return cls(nodes)

    def printData(self):
        print("Network: spanningTree={}, nodes:". format(self.spanningTree))
        for node in self.nodes:
            node.printData()

    def testIntegrity(self):
        pass


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

    def sendMsg(self, link, rootID, sumCosts=0):
        if self.nodeID == link.leftEnd:
            destination = link.rightEnd
        else:
            destination = link.leftEnd
        msg = Message(self.nodeID, destination, rootID, sumCosts)
        link.msgs.append(msg)

    def receiveMsg(self, link):
        link.printData()
        print(self.nodeID)
        for i in range(0, len(link.msgs)):
            if self.nodeID == link.msgs[i].destination:
                self.msgCnt = self.msgCnt+1
                return link.msgs.pop(i)


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
        print("Link: leftEnd={},  rightEnd={}, cost={}, msgs:". format(self.leftEnd, self.rightEnd, self.cost))
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

# Argparser
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filepath", help="Path to the .txt file that contains the Network specifications", default="./Inputdateien/graph.txt")
    args = parser.parse_args()
    return args

def main():
    # Parse arguments
    args = parseArgs()
    print("Selected file: {}\n".format(args.filepath))
    # Load the network from the text file
    print("Loading network...")
    network = Network.from_graph_txt(args.filepath)
    print("Loaded network:")
    network.printData()
    network.nodes[0].sendMsg(network.nodes[0].links[0], 5, 6)
    network.printData()
    msg = network.nodes[1].receiveMsg(network.nodes[1].links[0])
    msg.printData()
    network.printData()


if __name__ == "__main__":
    main()