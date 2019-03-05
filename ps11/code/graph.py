# 6.00 Problem Set 11
#
# graph.py
#
# A set of data structures to represent graphs
#


class Node(object):
    def __init__(self, name):
        self.name = str(name)

    def getName(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)


class Edge(object):
    def __init__(self, src, dest, totalDist, outdoorDist):
        self.src = src
        self.dest = dest

        self.totalDist = int(totalDist)
        self.outdoorDist = int(outdoorDist)

    def getSource(self):
        return self.src

    def getDestination(self):
        return self.dest

    def gettotalDist(self):
        return self.totalDist

    def getoutdoorDist(self):
        return self.outdoorDist

    def __str__(self):
        return str(self.src) + '->' + str(self.dest)


class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        self.nodes = set([])
        self.edges = {}
        self.paths = {}

    def addNode(self, node):
        if self.hasNode(node):
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[self.getNode(node)] = []
            self.paths[self.getNode(node)] = []

    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(self.hasNode(src) and self.hasNode(dest)):
            raise ValueError('Node not in graph')
        self.edges[self.getNode(src)].append( edge )
        self.paths[self.getNode(src)].append(self.getNode(dest))

    def childrenOf(self, node):
        return self.paths.get(self.getNode(node), [])

    def edgesOf(self, node):
        return self.edges.get(self.getNode(node), [])

    def getNode(self, node):
        if type(node) is str:
            node = Node(node)
        if type(node) is Node:
            for n in self.nodes:
                if n == node:
                    return n
        elif type(node) is int or type(node) is float:
            for n in self.nodes:
                if float(n.getName()) == node:
                    return n

    def hasNode(self, node):
        if type(node) is Node:
            for n in self.nodes:
                if n == node:
                    return True
        elif type(node) is int or type(node) is float:
            for n in self.nodes:
                if float(n.getName()) == node:
                    return True

        return False

    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = res + str(k) + '->' + str(d) + '\n'
        return res[:-1]
