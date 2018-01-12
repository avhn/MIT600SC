# 6.00 Problem Set 11
#
# ps11.py
#
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
from graph import Digraph, Edge, Node


# Problem 2: Building up the Campus Map

# Edge class outdoorDist and totalDist added
# Digraph class rewrited hasNode and created getNode, edgesOf
# childrenOf changed
    
class Stack(object):
    """
    Helper class to backtrack path for depth-first search.
    """

    def __init__(self):
        self.data = list()

    def getData(self):
        return self.data
    
    def push(self, item):
        self.data.insert(0, item)
        #self.data.append(item)
    def pop(self):
        item = self.data[0]
        del self.data[0]
        return item

    def showTop(self):
        return self.getData()[0]

    def getpath(self):

        return self.getData()[::-1]
    
    def __len__(self):
        return len(self.getData())

    def __str__(self):
        return str( self.getData() )


def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    graph = Digraph()
    mapFile = open(mapFilename, 'r')
    for line in mapFile:
        line = line.split()
        src, dest, totalDist, outdoorDist = \
        Node(line[0]), Node(line[1]), line[2], line[3]
        
        if not graph.hasNode(src):
            graph.addNode(src)
        if not graph.hasNode(dest):
            graph.addNode(dest)

        graph.addEdge( Edge(graph.getNode(src), graph.getNode(dest), totalDist, outdoorDist) )

    print("Loading map from file...")
    return graph

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and the constraints
#
class noSuchPath(Exception):
    pass

def depthfirst(digraph, start, end):
    """
    Brute-force style implemented depth-first algorithm.
    """

    stack = Stack()
    paths = list()

    def move():
        if len(stack) is 0:
            stack.push( digraph.getNode(start))
        
        for e in digraph.edgesOf( stack.showTop() ):
            if e.getDestination() in stack.getData():
                continue

            stack.push( e.getDestination() )

            if stack.showTop() is digraph.getNode(end):
                paths.append( stack.getpath() )
            else:
                move()

            stack.pop()
    move()
    return paths
    
def bruteForceSearch(digraph, start, end, maxTotalDist= 3000, maxDistOutdoors = 3000):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    all = depthfirst( digraph, start, end)

    shortest = None
    path = None
    for p in all:
        totalDist = 0
        outdoorDist = 0
        for node in range( len(p)-1 ):
            for e in digraph.edgesOf( p[node] ):
                if e.getDestination() is p[node+1]:
                    totalDist += e.gettotalDist()
                    outdoorDist += e.getoutdoorDist()

        if totalDist <= maxTotalDist and outdoorDist <= maxDistOutdoors:
            if path is None or totalDist < shortest:
                path = p
                shortest = totalDist

    if path is None:
        raise ValueError('No such path')
    return path
        
#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
class pathOptimizer(object):
    """
    Contains shortest current path and it's total distance
    """
    def __init__(self):
        self.dist = None
        self.path = list()

    def update(self, path, dist):
        self.dist = dist
        self.path = path

    def shortest(self):
        return self.dist

    def result(self):
        return self.path
    
def optimizedDfs(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Depth-first search with backtracking.
    """

    path = pathOptimizer()
    stack = Stack()
    
    def move(pathObject, totalDist = 0, outdoorsDist = 0):
        """
        Recursive function.
        """
        if totalDist > maxTotalDist or outdoorsDist > maxDistOutdoors:
            return
        if len(stack) is 0:
            stack.push( digraph.getNode(start))
        
        for e in digraph.edgesOf( stack.showTop() ):
            if e.getDestination() in stack.getData():
                continue

            stack.push( e.getDestination() )
            totalDist += e.gettotalDist()
            outdoorsDist += e.getoutdoorDist()
            
            if stack.showTop() is digraph.getNode(end) and totalDist <= maxTotalDist and outdoorsDist <= maxDistOutdoors:
                if pathObject.shortest() is None or pathObject.shortest() > totalDist:
                    pathObject.update(stack.getpath(), totalDist)
            else:
                move(pathObject, totalDist, outdoorsDist)
                
            stack.pop()
            totalDist -= e.gettotalDist()
            outdoorsDist -= e.getoutdoorDist()

    move(path)
    return path.result()
    
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    path = optimizedDfs(digraph, start, end, maxTotalDist, maxDistOutdoors)
    if len(path) is 0:
        raise ValueError('No such path')
    
    return path



#### Uncomment below when ready to test
if __name__ == '__main__':
    # Test cases
    digraph = load_map("mit_map.txt")

    LARGE_DIST = 1000000
    # Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    brutePath1 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    dfsPath1 = directedDFS(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "Brute-force: ", brutePath1
    print "DFS: ", dfsPath1

    # Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, 0)
    dfsPath2 = directedDFS(digraph, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "Brute-force: ", brutePath2
    print "DFS: ", dfsPath2

    # Test case 3
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
    dfsPath3 = directedDFS(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", brutePath3
    print "DFS: ", dfsPath3

    # Test case 4
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    brutePath4 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, 0)
    dfsPath4 = directedDFS(digraph, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "Brute-force: ", brutePath4
    print "DFS: ", dfsPath4

    # Test case 5
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    brutePath5 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
    dfsPath5 = directedDFS(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "Brute-force: ", brutePath5
    print "DFS: ", dfsPath5

    # Test case 6
    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    brutePath6 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, 0)
    dfsPath6 = directedDFS(digraph, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "Brute-force: ", brutePath6
    print "DFS: ", dfsPath6

    # Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(digraph, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
    try:
        directedDFS(digraph, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

    # Test case 8
    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(digraph, '10', '32', 100, LARGE_DIST)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
    try:
        directedDFS(digraph, '10', '32', 100, LARGE_DIST)
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

