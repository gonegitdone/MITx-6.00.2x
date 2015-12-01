# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed mapGraph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.mapGraph.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed mapGraph representing the map
    """
    print "Loading map from file..."
    mapGraph = WeightedDigraph()
    mapFile = open(mapFilename, 'r')
    lines = [line.rstrip() for line in mapFile.readlines()]
    for line in lines:
        lineSplit = line.split(' ')
        srcNode = Node(lineSplit[0])
        destNode = Node(lineSplit[1])
        totDist = lineSplit[2]
        outsideDist = lineSplit[3]
        if not mapGraph.hasNode(srcNode):
            mapGraph.addNode(srcNode)
        if not mapGraph.hasNode(destNode):
            mapGraph.addNode(destNode)
        edge = WeightedEdge(srcNode, destNode, totDist, outsideDist)
        mapGraph.addEdge(edge)
    return mapGraph


# In this box, define a variable called `nodes`. Set it equal to the value you get
#  by calling `mitMap.nodes`

        

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

# load_map('mit_map.txt')

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

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
    def getAllPaths(graph, start, end, path = [], goodPaths = []):
        ''' assumes graph is a Digraph
            assumes start and end are nodes in graph
            returns a list of all good paths from start to end
        '''
        path = path + [start]
        if start == end:
            goodPaths.append(path)
            return path
        for node in graph.childrenOf(Node(start)):
            if str(node) not in path: #avoid cycles
                getAllPaths(graph, str(node), end, path, goodPaths)
        return goodPaths

    def getShortestPath(graph, goodPaths, maxTotalDistance, maxOutdoorDistance):
            '''
                returns the shortest path from a list of goodPaths constrained my the max allowable
                total and outdoor distances.
                Raise a value error if no path is found which meets the given criteria
            '''
            shortestPath = []
            shortestDist = float(maxTotalDistance)
            for path in goodPaths:
                # print 'len of current path: ', len(path), '\ncuurent path: ', path
                totalDist = 0.0
                totalOutdoorDist = 0.0
                for node in range(len(path)-1):
                    for NodeDest, (NodeTotalDist, NodeOutdoorDist) in graph.edges[Node(path[node])]:
                        if str(NodeDest) == path[node + 1]:
                            totalDist += NodeTotalDist
                            totalOutdoorDist += NodeOutdoorDist
                            break # to save time
                if (totalDist <= maxTotalDistance) and (totalOutdoorDist <= maxOutdoorDistance) and (totalDist <= shortestDist):
                    shortestPath = path
                    shortestDist = totalDist
            if len(shortestPath) == 0:
                raise ValueError
            return shortestPath

    goodPaths = getAllPaths(digraph, start, end)
    shortestPath = getShortestPath(digraph, goodPaths, float(maxTotalDist), float(maxDistOutdoors))
    return shortestPath


#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

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
    # Initialise lists & variables
    stack = []
    stack.append([[start], (0, 0)])
    shortestDist = maxTotalDist + 1.0
    shortestPath = []
    totalDist = 0.0
    outdoorDist = 0.0
    # While there are still items in the stack, continue to look for paths
    while len(stack) != 0:
        # print 'current stack', stack
        currentStackItem = stack.pop()
        path = currentStackItem[0] # extract path list for current stack item
        currentNode = path[-1] # Last node in path list for current stack item
        # Extract the destination Node and distances from the current nodes edge
        for nodeDest, (nodeTotalDist, nodeOutdoorDist) in digraph.edges[Node(currentNode)]:
            # Initialise distances for current stack item for each node edge
            # this is done for every node edge so the distances are initialised and summed correctly
            totalDist = currentStackItem[1][0]
            outdoorDist = currentStackItem[1][1]
            if str(nodeDest) not in path:    # Avoid cycles
                newPath = path + [str(nodeDest)] # add node to path
                totalDist += nodeTotalDist  # add to path total distance
                outdoorDist += nodeOutdoorDist  # add to path outdoor total distance
                # print 'new path: ', newPath
                # print 'totalDist: ', totalDist, '\tNode distance: ', nodeTotalDist
                # print 'outdoor dist: ', outdoorDist, '\tNode outdoor distance: ', nodeOutdoorDist
                # if any of the distances exceed the constraints continue back to 'edge' for loop to process new nodeDest
                if (totalDist > shortestDist) or (totalDist > maxTotalDist) or (outdoorDist > maxDistOutdoors):
                    continue    # back to 'edge' for loop without executing the code below
                stack.append([newPath, (totalDist, outdoorDist)])
                # print 'stack length: ', len(stack), '\t current stack: ', stack
                # Compare current destination node with the end to see if path complete
                if str(nodeDest) == end:
                    shortestPath = newPath  # new shortest path found
                    shortestDist = totalDist
                    # print 'new shortest path found: ', shortestPath
                    # print 'new shortest distance: ', shortestDist
    # print shortestPath
    if len(shortestPath) == 0:
        raise ValueError
    return shortestPath




# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':
    #Test cases
    mitMap = load_map("mit_map.txt")
    # print isinstance(mitMap, Digraph)
    # print isinstance(mitMap, WeightedDigraph)
    # print 'nodes', mitMap.nodes
    print 'edges', mitMap.edges


    LARGE_DIST = 1000000

#     ##Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "Brute-force: ", brutePath1
    print "DFS: ", dfsPath1
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

    ##Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
    dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "Brute-force: ", brutePath2
    print "DFS: ", dfsPath2
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

    ##Test case 3
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", brutePath3
    print "DFS: ", dfsPath3
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

    ##Test case 4
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
    dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "Brute-force: ", brutePath4
    print "DFS: ", dfsPath4
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

    ##Test case 5
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "Brute-force: ", brutePath5
    print "DFS: ", dfsPath5
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

    ##Test case 6
    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
    dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "Brute-force: ", brutePath6
    print "DFS: ", dfsPath6
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

    ##Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'

    try:
        directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'

    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

    ##Test case 8
    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
    except ValueError:
        bruteRaisedErr = 'Yes'

    try:
        directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
    except ValueError:
        dfsRaisedErr = 'Yes'

    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr
