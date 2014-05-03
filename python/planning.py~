from heapq import *
from copy import deepcopy

# Global variables which are temporarily here for testing
#startWorld = [["a", "c","b"],["m"],["g"]]
#CHANGE LIST INDEXING IN PERFORMMOVE
startWorld1 = [["e"],["a","l"],[],[],["i","h","j"],[],[],["k","g","b","c"],[],["d","m","f"]]
startWorld2 = [["e"],["a"],["l"],[],["i","h","j"],[],[],["k","g","c","b"],[],["d","m","f"]]
startWorld3 = [[],["a"],["l"],[],["i","h","j","e"],[],[],["k","g","c","b"],[],["d","m","f"]]
startWorld4 = [[],["a"],["l"],[],["i","h","j","e"],[],[],["k","g","c","b"],["f"],["d","m"]]
startWorld5 = [[],["a"],["l"],[],["i","h","j"],["e"],[],["k","g","c","b"],["f"],["d","m"]]
startWorld6 = [[],["a"],["l"],[],["i","h"],["e"],["j"],["k","g","c","b"],["f"],["d","m"]]
startWorld7 = [["h"],["a"],["l"],[],["i"],["e"],["j"],["k","g","c","b"],["f"],["d","m"]]
startWorld8 = [["h","a"],[],["l"],[],["i"],["e"],["j"],["k","g","c","b"],["f"],["d","m"]]
startWorld9 = [["h","a"],[],["l"],[],["i"],[],["j"],["k","g","c","b"],["f"],["d","m"]]

world = [["c","b"],["a" ,"m"],["g"]]

world2 = [["e"],["m"],[]]
world3 = [["e"],["a","l"],[],[],["i","h","j"],[],[],["k","g","c","b"],[],["d","m","f"]]

#worldIdList = [(world,0)]""

startWorld = [["e"],["a","l"],[],["c","d","f"]]
goal = ["onTop", "c", "a"]
objects = {
    "a": { "form":"brick",   "size":"large",  "color":"green" },
    "b": { "form":"brick",   "size":"small",  "color":"white" },
    "c": { "form":"plank",   "size":"large",  "color":"red"   },
    "d": { "form":"plank",   "size":"small",  "color":"green" },
    "e": { "form":"ball",    "size":"large",  "color":"white" },
    "f": { "form":"ball",    "size":"small",  "color":"black" },
    "g": { "form":"table",   "size":"large",  "color":"blue"  },
    "h": { "form":"table",   "size":"small",  "color":"red"   },
    "i": { "form":"pyramid", "size":"large",  "color":"yellow"},
    "j": { "form":"pyramid", "size":"small",  "color":"red"   },
    "k": { "form":"box",     "size":"large",  "color":"yellow"},
    "l": { "form":"box",     "size":"large",  "color":"red"   },
    "m": { "form":"box",     "size":"small",  "color":"blue"} }


class Node:
    # parent, world, g, h, f
    
    def __init__(self, parent, world, g, h, f):
        self.parent = parent
        self.world = world

        self.g = g
        self.h = h
        self.f = f
   
    def compareTo(self, node):
       return self.world == node.world 

class Rules:

    def __init__(self):
        ruleList = list()
            
        ruleList.append(ballInBox())

    def applyRules(self, object, stack):
        if stackHeight(stack) == 0:
            return True
        else:
            object = getObjectDescription(object)
            stackObject = stack[stackHeight(stack)-1]


    def ballInBox(self, object, stackObject):
        if object["form"] == "ball" and not (stackObject["form"] == "box"):
            return False
        else:
            return True

#    def ballCannotSupport(self, object, stackObject):


#    def smallObjectSupport(self, object, stackObject:

#    def boxCannotContain(self, object, stackObject):


#    def boxSupported(self, object, stackObject):

#    def largeBoxSupported(self, object, stackObject):




        # Constraints:
# Balls must be in boxes or on the floor, otherwise they roll away
# Balls cannot support anything
# Small objects cannot support large objects
# Boxes cannot contain pyramids or planks of the same size
# Boxes can only be supported by tables or planks of the same size,
# but large boxes can also be supported by large bricks.

    

#
# Lots of helper functions here below:
#

# Gets the number of stacks in the world

# Returns a list of the stacks in the world
def getAllStacks(world):
    return range(len(world))

# Gets all the empty stacks in the world
def getEmptyStacks(world):
    x = []
    for stack, object in enumerate(world):
        if not object:
            x.append(stack)
    return x

# Gets the top objects on the stacks which are in the world
# def getTopObject(world):
#    balls = []
#    for object in world:
#        if object != []:
#            balls.append(object[-1])
#        else:
#            balls.append([])
#    return balls

# Gets an ordered list of all the objects in the world
def getOrderedListOfObjects(world):
    orderedList = [item for sublist in world for item in sublist]
    orderedList.sort()
    return orderedList

# Gets the stack positions of all the balls which are on the top of a stack
# (There's a rule that no objects are allowed to be put upon balls)
def getStacksWithBallsOnTop(world):
    topBalls = []
    topBallStacks = []
    topObjectsInWorld = getTopObject(world)
    for object in topObjectsInWorld:
        if object != []:
            a = ''.join(object)
            objectForm = objects[a].get("form")
            if objectForm == "ball":
                topBalls.append(objectForm)
            else:
                topBalls.append([])
        else: 
            topBalls.append([])
    for stack, item in enumerate(topBalls):
        if item is "ball":
            topBallStacks.append(stack)
    return topBallStacks

# Gets the stack positions where small objects are on top of the stack
# (Small objects cannot hold large objects)
def getStacksWithSmallObjectsOnTop(world):
    smallObjects = []
    topSmallObjectStacks = []
    topObjectsInWorld = getTopObject(world)
    for object in topObjectsInWorld:
        if object != []:
            a = ''.join(object)
            objectForm = objects[a].get("size")
            if objectForm == "small":
                smallObjects.append(objectForm)
            else:
                smallObjects.append([])
        else: 
            smallObjects.append([])
    for stack, item in enumerate(smallObjects):
        if item is "small":
            topSmallObjectStacks.append(stack)
    return topSmallObjectStacks


#
# More useful functions
#

# Test function used to pass commands to the shrdlite.py file and from there to the GUI
def test():
    return ["pick 1", "drop 2"]


# Gets the stack of an object
def getObjectStack(object, world):
    stack = 0
    for item in world:
        if object in item:
            return stack
        else:
            stack = stack+1

# Checks whether the target object is on top of a stack or not
def isTargetObjectOnTop(targetObject, world):
    topList = getTopObject(world)
    if targetObject in topList:
        return True
    else:
        return False

def checkStuff(object):
    stack = 0
    for item in world:
        if object in item:
            return stack
        else:
            stack = stack+1




###
#
#
#
# TEST FUNCTIONS SEARCH BELOW HERE:
#
#
#
#
        
def search(world, goal):
    closedSet = []
    openSet = []

    #heappush(openSet, (5, 'write code'))

    gScore = 0
    hScore = 0
    fScore = 0
    
    startNode = Node(None, world, gScore, hScore, fScore)

    startTuple = (0, startNode)
    heappush(openSet, startTuple)

    while openSet != []:
        currentNode = heappop(openSet)[1]

        if (isGoal(currentNode.world, goal)):
            return reconstructPath(currentNode, list())

        closedSet.append(currentNode)

        for neighbor in performMove(currentNode):
            cost = currentNode.g + movementCost(currentNode, neighbor)      

            nodeInOpenSet = isNodeInOpenSet(openSet, neighbor)

            if (nodeInOpenSet[1] != None and cost < nodeInOpenSet[1].g):
                removeNodeFromSet(openSet, nodeInOpenSet[0])

            nodeInClosedSet = isNodeInClosedSet(closedSet, neighbor)

            if (nodeInOpenSet[1] == None and nodeInClosedSet == None):
                neighbor.g = cost
                neighbor.h = heuristic_cost_estimate(neighbor.world, goal)
                neighbor.f = neighbor.g + neighbor.h

                neighbor.parent = currentNode
                neighborTuple = (neighbor.f, neighbor)
                heappush(openSet, neighborTuple)

                
def isNodeInOpenSet(openSet, node):
    index = 0
    for compNode in openSet:
        if node.compareTo(compNode[1]):
            return (index, compNode[1])
        index = index + 1
    
    return (0, None)

def isNodeInClosedSet(closedSet, node):
    for compNode in closedSet:
        if node.compareTo(compNode):
            return compNode
    
    return None

def removeNodeFromSet(set, index):
    set.pop(index)

    #[[n for n in nested [nodeP for nodes in set if not nodeP[1].compareTo(node)] 


def performMove(node):
    neighbors = list()    

    for pickStack in range (getWorldLength(startWorld)):        
        for dropStack in range (getWorldLength(startWorld)):
            neighborNode = deepcopy(node)
            object = pick(neighborNode.world, pickStack)

            if (object == None):
                continue

            drop(neighborNode.world, dropStack, object)
            
            neighbors.append(neighborNode)
    return neighbors    

def getTopObject(world, stack):
    stackHeight = getStackHeight(world,stack)
    if stackHeight == 0:
        return None
    else:
        return world[stack][stackHeight-1]

def pick(world, stack):
    if (getStackHeight(world, stack) > 0):
        return world[stack].pop()
    else:
        return None


def drop(world, stack, object):
    return world[stack].append(object)

def heuristic_cost_estimate(world, goal):
    relation, objA, objB = goal	
    locA = getLocation(world, objA)
    locB = getLocation(world, objB)
    return abs((locA[1] - getStackHeight(world, locA[0])) + (locB[1] - getStackHeight(world, locB[0])))


def reconstructPath(node, commandString):
    if node.parent == None: # Base case
        return commandString
    else:
        parentNode, command = parseNode(node)
        return reconstructPath(parentNode, command + commandString)


def parseNode(node):  
    #parentWorld = [["e"],["a","l"],[],[],["i","h","j"],[],[],["k","g","c","b"],[],["d","m","f"]] # OLD WORLD
    #currentWorld = [["e"],["a","l"],[],[],["i","h","j"],["f"],[],["k","g","c","b"],[],["d","m"]] # NEW WORLD
    parentNode = node.parent

    parentWorld = node.parent.world
    currentWorld = node.world
    worldLength = len (parentWorld)
    list = []

    world1concat = [value for sublist in parentWorld for value in sublist]
    world2concat = [value for sublist in currentWorld for value in sublist]
    pickString = ""
    dropString = ""

    if (len (world1concat) == len (world2concat)):

        for i in range(0,worldLength):
            if currentWorld[i] < parentWorld[i]:
                pickString = "pick " + str(i)
                
            if currentWorld[i] > parentWorld[i]:
                dropString = "drop " + str(i)
          
        list.append(pickString)
        list.append(dropString)
            

        return (parentNode, list)
    elif (len (world1concat) > len (world2concat)):
        # This loop gets run if the last command is pick, i.e. the arm ends up holding an object
        changedElement = (set(world1concat) - set(world2concat)).pop()
        theStack = getObjectStack(changedElement, parentWorld)
        newCommand = "pick " + str(theStack)
        list.append(newCommand)
        return (parentNode, list)
    else:
        # This loop gets run if the first command is a pick, i.e. if the arm was holding an object
        changedElement = (set(world2concat) - set(world1concat)).pop()
        theStack = getObjectStack(changedElement, currentWorld)
        newCommand = "drop " + str(theStack)
        list.append(newCommand)
        return (parentNode, list)

def movementCost(fromNode, toNode):
    fromWorld = fromNode.world
    toWorld = toNode.world
    start = -1
    end = -1

    for column in range(getWorldLength(startWorld)):
        if (len(fromWorld[column]) != len(toWorld[column]) and start == -1):
            start = column
        elif (len(fromWorld[column]) != len(toWorld[column]) and end == -1):
            end = column

    return abs(end - start) 


# Checks whether the goal has been satisfied or not
def isGoal(world, goal):
    relation, sourceObject, targetObject = goal

    sourceObjectLocation = getLocation(world, sourceObject)
    targetObjectLocation = getLocation(world, targetObject)

    if relation == "onTop" or relation == "inside":
        if sourceObjectLocation[0] == targetObjectLocation[0] and sourceObjectLocation[1] == targetObjectLocation[1] + 1:
            return True
        else:
            return False
    elif relation == "above":
        if sourceObjectLocation[0] == targetObjectLocation[0] and sourceObjectLocation[1] > targetObjectLocation[1]:
            return True
        else:
            return False
    elif relation == "under":
        if sourceObjectLocation[0] == targetObjectLocation[0] and sourceObjectLocation[1] < targetObjectLocation[1]:
            return True
        else:
            return False
    elif relation == "beside":
        if sourceObjectLocation[0] == targetObjectLocation[0] + 1 or sourceObjectLocation[0] == targetObjectLocation[0] - 1:
            return True
        else:
            return False
    elif relation == "leftOf":
        if sourceObjectLocation[0] < targetObjectLocation[0]:
            return True
        else:
            return False
    elif relation == "rightOf":
        if sourceObjectLocation[0] > targetObjectLocation[0]:
            return True
        else:
            return False


# Utility functions
def getWorldLength(world):
    return len(world)

def getStackHeight(world, stack):
    return len(world[stack])

def getObject(world, column, row):
    return world[column][row]

def getObjectDescription(object):
    return objects[object]

def getLocation(world, object): 
    for column in range(getWorldLength(startWorld)):
        for row in range(getStackHeight(world, column)):
            if object == getObject(world, column, row):
                return (column, row)


if __name__ == '__main__':
    node1 = Node(None, startWorld1, 0, 0, 0)
    node2 = Node(node1, startWorld2, 0, 0, 0)
    node3 = Node(node2, startWorld3, 0, 0, 0)
    node4 = Node(node3, startWorld4, 0, 0, 0)
    node5 = Node(node4, startWorld5, 0, 0, 0)
    node6 = Node(node5, startWorld6, 0, 0, 0)
    node7 = Node(node6, startWorld7, 0, 0, 0)
    node8 = Node(node7, startWorld8, 0, 0, 0)
    node9 = Node(node8, startWorld9, 0, 0, 0)

    #print reconstructPath(node9, [])

    #startWorld = [["e"],["a","l"],[],[],["i","h","j"],[],[],["k","g","c","b"],[],["d","m","f"]]
    pickAndDrop = search(startWorld, goal)
    print pickAndDrop
