from heapq import *
from copy import deepcopy

# Global variables which are temporarily here for testing
startWorld = [["c","b"],["a" ,"m"],["g"]]
#CHANGE LIST INDEXING IN PERFORMMOVE
startWorld1 = [["e"],["a","l"],[],[],["i","h","j"],[],[],["k","g","c","b"],[],["d","m","f"]]
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

#worldIdList = [(world,0)]

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
def getTopObject(world):
	balls = []
	for object in world:
		if object != []:
 			balls.append(object[-1])
 		else:
 			balls.append([])
 	return balls

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

# A function which does different things depending on which relation the source and target objects have
# def performMove(goal, world):
# 	#return["pick 1", "drop 2", "pick 3", "drop 2"]
# 	goal = ["onTop,c,a"]
# 	goalList = goal[0].split(",")
# 
# 	relation = goalList[0]
# 	sourceObject = goalList[1]
# 	targetObject = goalList[2]
# 
# 	sourceObjectStack = getObjectStack(sourceObject)
# 	targetObjectStack = getObjectStack(targetObject)
# 
# 	if relation == "onTop":
# 		if isTargetObjectOnTop(targetObject, world):
# 			return ["pick " + str(sourceObjectStack)]
# 		else:
# 			return ["pick " + str(targetObjectStack)]
# 
# 	elif relation == "inside":
# 		return "inside"
# 	elif relation == "above":
# 		return "dfsfd"
# 	elif relation == "under":
# 		return "under"
# 	elif relation == "beside":
# 		return "beside"
# 	elif relation == "leftOf":
# 		return "to the left"
# 	elif relation == "rightOf":
# 		return "to the right"

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
##

def solve(world, goal):
    relation, sourceObject, targetObject = goal
		
def search(world, goal):
    closedSet = []
    openSet = []

    #heappush(openSet, (5, 'write code'))

    g_score = 0
    h_score = 0
    f_score = 0

    startNode = Node(None, world, g_score, h_score, f_score)

    start = (0, startNode)
    heappush(openSet, start)
    print openSet

    while openSet != []:
        currentNode = heappop(openSet)[1]
        print "CURRENT: ", currentNode

        if (isGoal(currentNode.world, goal)):
            return reconstruct_path(currentNode)

        closedSet.append(currentNode)
        for neighbor in performMove(currentNode):
            print neighbor.world
        

        for neighbor in performMove(currentNode):
            print "hej"
            cost = currentNode.g + movementCost(currentNode, neighbor)		

            nodeInOpenSet = nodeInSet(openSet, neighbor)

            if (nodeInOpenSet != None and cost < nodeInOpenSet.g):
                removeNodeFromSet(nodeInOpenSet)

            nodeInOpenSet = nodeInSet(openSet, neighbor)
            nodeInClosedSet = nodeInSet(closedSet, neighbor)

            if (nodeInOpenSet != None and nodeInClosedSet != None):
                neighbor.g = cost
                neighbor.h = heuristic_cost_estimate(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h

                neighbor.parent = currentNode
                neighborTuple = (neighbor.f, neighbor)
                heappush(openSet, neighborTuple)

                
def nodeInSet(set, node):
    index = 0
    for compNode in set:
        if node.compareTo(compNode):
            return compNode
    return None

def removeNodeFromSet(set, node):
    [nodes for nodes in set if not node.compareTo(nodes)] 


def performMove(node):
    neighbors = list()    
    counter = 0

    for pickStack in range (getWorldLength(startWorld)):		
        for dropStack in range (getWorldLength(startWorld)):
            neighborNode = deepcopy(node)
            counter = counter + 1
            object = pick(neighborNode.world, pickStack)

            if (object == None):
                continue

            drop(neighborNode.world, dropStack, object)
            
            neighbors.append(neighborNode)
    print counter
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
  if node.parent.parent == None: # Base case
    print 'hej'
    parentNode, command = parseNode(node)
    return command + commandString
  else:
    print 'hej2'
    parentNode, command = parseNode(node)
    return reconstructPath(parentNode, command + commandString)
    

	
def parseNode(node):  
  #parentWorld = [["e"],["a","l"],[],[],["i","h","j"],[],[],["k","g","c","b"],[],["d","m","f"]] # OLD WORLD
	#currentWorld = [["e"],["a","l"],[],[],["i","h","j"],["f"],[],["k","g","c","b"],[],["d","m"]] # NEW WORLD
    parentNode = node.parent
 
    parentWorld = node.parent.world
 #   print parentWorld
    currentWorld = node.world
  #  print currentWorld
    worldLength = len (parentWorld)
    list = []

    world1concat = [value for sublist in parentWorld for value in sublist]
    world2concat = [value for sublist in currentWorld for value in sublist]
    pickString = ""
    dropString = ""

    if (len (world1concat) == len (world2concat)):

        for i in range(0,worldLength):
            if currentWorld[i] > parentWorld[i]:
                dropString = "drop " + str(i)
            if currentWorld[i] < parentWorld[i]:
                pickString = "pick " + str(i)

        list.append(pickString)
        list.append(dropString)
        return (parentNode, list)
    else:
        # This loop gets run if the last command is pick, i.e. the arm ends up holding an object
        changedElement = (set(world1concat) - set(world2concat)).pop()
        theStack = getObjectStack("f", parentWorld)
        newCommand = "pick " + str(theStack)
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

# Constraints:
# Balls must be in boxes or on the floor, otherwise they roll away
# Balls cannot support anything
# Small objects cannot support large objects
# Boxes cannot contain pyramids or planks of the same size
# Boxes can only be supported by tables or planks of the same size,
# but large boxes can also be supported by large bricks.

def getPlausibleStacks(world, object):
	stacks = getAllStacks(world)
	objDescrip = getObjectDescription(object)
	
	
	



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
	#print getStackHeight(world2, 0)
	#print heuristic_cost_estimate(startWorld, goal)
    
  testNode = Node(None, startWorld1, 0, 0, 0)
 
  
  #print neighbors
	
 #print performMove(world2)
	#print getTopObject(world2, 5)
  
  #  node1 = Node(None, startWorld1, 0, 0, 0)
  #  node2 = Node(node1, startWorld2, 0, 0, 0)
  #  node3 = Node(node2, startWorld3, 0, 0, 0)
  #  node4 = Node(node3, startWorld4, 0, 0, 0)
  #  node5 = Node(node4, startWorld5, 0, 0, 0)
  #  node6 = Node(node5, startWorld6, 0, 0, 0)
  #  node7 = Node(node6, startWorld7, 0, 0, 0)
  #  node8 = Node(node7, startWorld8, 0, 0, 0)
  #  node9 = Node(node8, startWorld9, 0, 0, 0)
  
  #node = Node(None, startWorld2, 0, 0, 0)
  #node2 = Node(node, startWorld, 4, 2, 6)
  #print parseNode(node2)
  #print reconstructPath(node9, [])
  pickAndDrop = search(world, goal)
  print pickAndDrop
