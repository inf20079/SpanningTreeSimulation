import os
import sys
import threading
import argparse
import time

# Globals
startSignal = False
exitSignal = False
endSignal = 0
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
    def from_graph_txt(cls, path, iterations):
        nodes = []
        links = []
        # Reading nodes and links from file
        with open(path, 'r') as graph:
            for line in graph:
                if '=' in line:
                    line = line.replace(' ', '')
                    line = line.replace(';', '')
                    nodes.append(Node(line[0], int(line[2]), iterations))
                if ':' in line:
                    line = line.replace(' ', '')
                    line = line.replace(';', '')
                    links.append(Link(line[0], line[2], int(line[4:])))

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

        return cls(nodes)

    # Print spanningtree
    def createSpanningtree(self):
        for i in range(0, len(self.nodes)):
            if self.nodes[i].nodeID == self.nodes[i].rootID:
                destination = "Root: "+str(self.nodes[i].nodeID)
            elif self.nodes[i].nodeID == self.nodes[i].rootLink.leftEnd:
                destination = str(self.nodes[i].nodeID)+" - "+str(self.nodes[i].rootLink.rightEnd)
            else:
                destination = str(self.nodes[i].nodeID)+" - "+str(self.nodes[i].rootLink.leftEnd)
            self.spanningTree.append(destination)

    # print spanning tree
    def printSpanningtree(self):
        print("Spanningtree:")
        for link in self.spanningTree:
            print(link)

    # Prints object data formatted
    def printData(self):
        print("Network: spanningTree={}, nodes:". format(self.spanningTree))
        for node in self.nodes:
            node.printData()

    def testIntegrity(self):
        pass


class Node(threading.Thread):
    
    def __init__(self, name, nodeID, iterations=None, links=None, rootID=None, rootCost=None, rootLink=None, msgCnt=0):
        threading.Thread.__init__(self)
        self.name = name
        self.nodeID = nodeID
        if iterations == None: 
            self.iterations = 10
        else: 
            self.iterations = iterations
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
        global startSignal, endSignal, lock, exitSignal
        msg = None

        #Initialize algorithm
        self.sendBroadcast(self.rootID)

        # Loop
        while not exitSignal:
            while startSignal and self.msgCnt < self.iterations:
                # Receive new msg
                lock.acquire()
                link, msg = self.receiveBroadcast()
                lock.release()
                # Check for new root
                if msg == None or not (msg.rootID < self.rootID or msg.rootID == self.rootID and (msg.sumCosts+link.cost) < self.rootCost):
                    break
                # Replace root
                self.rootID = msg.rootID
                self.rootCost = msg.sumCosts+link.cost
                self.rootLink = link
                # Send new root
                lock.acquire()
                self.sendBroadcast(self.rootID, self.rootCost)
                lock.release()
            time.sleep(0.01)
            # Signal protocoll end
            if self.msgCnt >= self.iterations:
                    endSignal = endSignal+1

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

# Argparser
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filepath", help="Path to the .txt file that contains the Network specifications", default="./Inputdateien/graph.txt")
    parser.add_argument("-i", "--iterations", type=int, help="Path to the .txt file that contains the Network specifications", default=10)
    args = parser.parse_args()
    return args

# Clear console
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def main():
    global startSignal, endSignal, exitSignal

    # Parse arguments
    args = parseArgs()
    print("Selected file: {}\n".format(args.filepath))
    input("Press enter to continue...")
    # Load the network from the text file
    print("Loading network...")
    network = Network.from_graph_txt(args.filepath, args.iterations)
    print("Loaded network:")
    clearConsole()
    network.printData()
    input("Press enter to continue...")
    # Start node Threads
    for node in network.nodes:
        node.start()
    # Start routing
    startSignal = True
    # Show Traffic
    while endSignal < len(network.nodes):
        time.sleep(0.01)
    # Exit threads
    exitSignal = True
    # Stop threads
    for node in network.nodes:
        node.join()
    # Create Spanning 
    clearConsole()
    network.createSpanningtree()
    network.printSpanningtree()
    input("Press enter to quit...")
    


if __name__ == "__main__":
    main()