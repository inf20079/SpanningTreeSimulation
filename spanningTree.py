from ast import arg
from multiprocessing.connection import wait
import os
from pickle import FALSE
import string
import sys
import threading
import argparse
import time
from tabulate import tabulate

# Argparser
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filepath", help="Path to the .txt file that contains the Network specifications", default="./Inputdateien/graph.txt")
    parser.add_argument("-amsg", "--waitformsg", type=int, help="Amount of empty messages before stopping.", default=5)
    parser.add_argument("-t", "--showtraffic", type=bool, help="Shows every interaction. Slows down routing process.", default=True)
    parser.add_argument("-mit", "--maxitems", type=int, help="Max amount of items.", default=50)
    parser.add_argument("-mco", "--maxcost", type=int, help="Max cost.", default=50)
    parser.add_argument("-mid", "--maxid", type=int, help="Max ID.", default=50)
    args = parser.parse_args()
    return args

# Clear console
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

class TrafficHandler:

    def __init__(self, isTrafficEnabled=None, update=None):
        if isTrafficEnabled == None: 
            self.isTrafficEnabled = False
        else: 
            self.isTrafficEnabled = isTrafficEnabled
        if update == None: 
            self.update = False
        else: 
            self.update = update
        self.update = update

    def waitTrafficRelease(self):
        if self.isTrafficEnabled == True:
            while self.update == True:
                time.sleep(0.25)

    def showTraffic(self, network):
        if self.isTrafficEnabled == True and self.update == True:
            clearConsole()
            network.printData()
            time.sleep(0.5)
            self.update = False

    def updateTrue(self):
        self.update = True

    def setTrafficEnabled(self):
        self.isTrafficEnabled = True 

# Globals
startSignal = False
exitSignal = False
endSignal = 0
Traffic = TrafficHandler()
lock = threading.Lock()

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
    def from_graph_txt(cls, path, waitformsg, maxId, maxCost, maxItems):
        nodes = []
        links = []
        lowestNodeId = None
        # Reading nodes and links from file
        with open(path, 'r') as graph:
            amtLines = 0
            for line in graph:
                if amtLines > maxItems:
                    print("Error: Too many Items: {}".format(amtLines))
                    exit(1)
                if '=' in line:
                    line = line.replace(' ', '')
                    line = line.replace(';', '')
                    if int(line[2]) > maxId:
                        print("Error: Node ID to high: {}".format(line[2]))
                        exit(1)
                    elif int(line[2]) <= 0:
                        print("Error: ID cannot be lower or equal to null: {}".format(line[2]))
                        exit(1)
                    nodes.append(Node(line[0], int(line[2]), waitformsg))
                if ':' in line:
                    line = line.replace(' ', '')
                    line = line.replace(';', '')
                    if int(line[4:]) > maxCost:
                        print("Error: Cost to high: {}".format(line[4:]))
                        exit(1)
                    links.append(Link(line[0], line[2], int(line[4:])))
                amtLines = amtLines+1


        # Replacing name with id in Link objects
        for link in links:
            for node in nodes:
                if node.name == link.leftEnd and node.name != link.rightEnd:
                    link.leftEnd = int(node.nodeID)
                if node.name == link.rightEnd and node.name != link.leftEnd:
                    link.rightEnd = int(node.nodeID)
            if isinstance(link.leftEnd, str) or isinstance(link.rightEnd, str):
                print("Error: This Link has no connection to the network or is connected to the same node:")
                link.printData()
                exit(1)

        # Adding connections to nodes
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

        availableNodeIds = []
        for node in nodes:
            availableNodeIds.append(node.nodeID)
        availableNodeIdsSet = set(availableNodeIds)
        duplicates = len(availableNodeIds) != len(availableNodeIdsSet)
        if duplicates:
            print("Error: Node IDs contain duplicates")
            exit(1)

        return cls(nodes)

    # Fills spanning tree list
    def createSpanningtree(self):
        translation = {}
        for node in self.nodes:
            translation[node.nodeID] = node.name

        for i in range(0, len(self.nodes)):
            if self.nodes[i].nodeID == self.nodes[i].rootID:
                destination = [True, translation.get(self.nodes[i].nodeID), "", 0]
            elif self.nodes[i].nodeID == self.nodes[i].rootLink.leftEnd:
                destination = [False, translation.get(self.nodes[i].nodeID), translation.get(self.nodes[i].rootLink.rightEnd), self.nodes[i].rootCost]
            else:
                destination = [False, translation.get(self.nodes[i].nodeID), translation.get(self.nodes[i].rootLink.leftEnd), self.nodes[i].rootCost]
            self.spanningTree.append(destination)

    # print spanning tree
    def printSpanningtree(self):
        print("Spanningtree:")
        print(tabulate(self.spanningTree, headers=["Root", "leftEnd", "rightEnd", "Cost"]))

    # Exports spanning tree
    def exportSpanningtree(self, path):
        # Name of file
        split = path.split("/")
        # Write spanning tree to file
        with open("./Exportdateien/"+split[-1], 'w') as graph:
            graph.write("Spanning-Tree of "+split[-1]+" {\n\n")
            for link in self.spanningTree:
                if link[0]:
                    graph.write("   Root: "+ link[1] +";\n")
            for link in self.spanningTree:
                if not link[0]:
                    graph.write("   "+ link[1] + " - " + link[2] + ";\n")
            graph.write("\n}")

    # Prints object data formatted
    def printData(self):
        print("Network: spanningTree={}, nodes:". format(self.spanningTree))
        for node in self.nodes:
            node.printData()

    # Tests for 
    def testIntegrity(self):
        rootNode = None
        for node in self.nodes:
            if node.nodeID <= 0:
                print("Error: Null is not allowed as node ID")
                exit(1)
            elif rootNode == None:
                rootNode = node
            elif rootNode != None and node.nodeID == rootNode.nodeID:
                print("Error: Duplicate Root-ID")
                exit(1)
            elif rootNode != None and node.nodeID < rootNode.nodeID:
                rootNode = node

class Node(threading.Thread):
    
    def __init__(self, name, nodeID, waitformsg=None, links=None, rootID=None, rootCost=None, rootLink=None, msgCnt=0):
        threading.Thread.__init__(self)
        self.name = name
        self.nodeID = nodeID
        if waitformsg == None: 
            self.waitformsg = 5
        else: 
            self.waitformsg = waitformsg
        if links == None: 
            self.links = []
        else: 
            self.links = links
        if rootID == None: 
            self.rootID = nodeID
        else: 
            self.rootID = nodeID
        if rootCost == None: 
            self.rootCost = 0
        else: 
            self.rootCost = rootCost
        if rootLink == None: 
            self.rootLink = None
        else: 
            self.rootLink = rootLink
        if msgCnt == None: 
            self.msgCnt = 0
        else: 
            self.msgCnt = msgCnt

    # Rooting Protocoll
    def run(self):
        global startSignal, endSignal, lock, exitSignal, Traffic
        msg = None
        iterationsWithoutMsg = 0
        endFlag = False

        #Initialize algorithm
        self.sendBroadcast(self.rootID)

        # Loop
        while not exitSignal:
            lock.acquire()
            msgAvailable = self.checkIfMsgAvailable()
            lock.release()

            if startSignal and msgAvailable:
                # Reset msg flag
                msgAvailable = False
                # Wait for release (if showtraffic enabled)
                Traffic.waitTrafficRelease()
                # Receive new msg
                lock.acquire()
                link, msg = self.receiveBroadcast()
                lock.release()
                # Check for new root
                if not (msg.rootID < self.rootID or msg.rootID == self.rootID and (msg.sumCosts+link.cost) < self.rootCost):
                    # set update (if showtraffic is enabled)
                    Traffic.updateTrue()
                else:
                    # Replace root
                    self.rootID = msg.rootID
                    self.rootCost = msg.sumCosts+link.cost
                    self.rootLink = link
                    # Send new root
                    lock.acquire()
                    self.sendBroadcast(self.rootID, self.rootCost)
                    lock.release()
                    iterationsWithoutMsg = 0
                    # set update (if showtraffic is enabled)
                    Traffic.updateTrue()
            else:
                iterationsWithoutMsg = iterationsWithoutMsg+1

            # Polling for new msg
            if iterationsWithoutMsg >= self.waitformsg:
                lock.acquire()
                endSignal = endSignal+1
                lock.release()
                while not msgAvailable and not exitSignal:
                    time.sleep(0.1)
                    lock.acquire()
                    msgAvailable = self.checkIfMsgAvailable()
                    lock.release()
                if not exitSignal:
                    lock.acquire()
                    endSignal = endSignal-1
                    lock.release()
                    iterationsWithoutMsg = 0

            time.sleep(0.01)

    # Prints object data formatted
    def printData(self):
        print("Node: name={}, nodeID={}, rootID={}, rootCost={}, rootLink={}, msgCnt={}, links:". format(self.name, self.nodeID, self.rootID, self.rootCost, self.rootLink, self.msgCnt))
        for link in self.links:
            link.printData()

    # Creates and sends the defined message 
    def sendUnicast(self, link, rootID, sumCosts=0):
        if self.nodeID == link.leftEnd:
            destination = link.rightEnd
        else:
            destination = link.leftEnd
        msg = Message(self.nodeID, destination, rootID, sumCosts)
        link.msgs.append(msg)

    # Sends a message to all links
    def sendBroadcast(self, rootID, sumCosts=0):
            for link in self.links:
                self.sendUnicast(link, rootID, sumCosts)

    def checkIfMsgAvailable(self):
        for link in self.links:
            for i in range(0, len(link.msgs)):
                if self.nodeID == link.msgs[i].destination:
                    return True
        return False

    # Grabs the first found message and returns it
    def receiveUnicast(self, link):
        for i in range(0, len(link.msgs)):
            if self.nodeID == link.msgs[i].destination:
                self.msgCnt = self.msgCnt+1
                return link.msgs.pop(i)

    # Grabs the first message from all links
    def receiveBroadcast(self):
        for link in self.links:
            msg = self.receiveUnicast(link)
            if msg != None: return link, msg
        return None, None

class Link:
    
    def __init__(self, leftEnd, rightEnd, cost, msgs=None):
        self.leftEnd = leftEnd
        self.rightEnd = rightEnd
        self.cost = cost
        if msgs == None:
            self.msgs = []
        else: 
            self.msgs = msgs

    # Prints object data formatted
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

    # Prints object data formatted
    def printData(self):
        print("Message: Source={}, Destination={}, rootID={}, sumCosts={}".format(self.source, self.destination, self.rootID, self.sumCosts))


def main():
    global startSignal, endSignal, exitSignal, Traffic

    # Parse arguments
    args = parseArgs()
    print("Selected file: {}\n".format(args.filepath))
    input("Press enter to continue...")

    # Load the network from the text file
    clearConsole()
    print("Loading network...")
    network = Network.from_graph_txt(args.filepath, args.waitformsg, args.maxid, args.maxcost, args.maxitems)
    print("Loaded network:")
    network.printData()
    input("\nPress enter to continue...")

    # Show Traffic
    if args.showtraffic == True:
        Traffic.setTrafficEnabled()

    # Start node Threads
    for node in network.nodes:
        node.start()

    # Start routing
    startSignal = True

    # Show Traffic
    while not exitSignal:
        # Show network traffic
        Traffic.showTraffic(network)
        lock.acquire()
        if endSignal >= len(network.nodes):
            exitSignal = True
        lock.release()
        time.sleep(0.01)

    # Stop threads
    for node in network.nodes:
        node.join()
    
    # Create spanning tree
    clearConsole()
    network.createSpanningtree()
    print("Finished Network:")
    network.printData()
    print("\n")
    network.printSpanningtree()
    network.exportSpanningtree(args.filepath)

if __name__ == "__main__":
    main()