from heapq import *

world = [["e"],["a","l"],[],[],["i","h","j"],[],[],["k","g","c","b"],[],["d","m","f"]]
world2 = [["e"],["l"],[],[],["i","h","j"],[],[],["k","g","c","b"],[],["d","m","f","a"]]
world3 = [["e"],["a","l"],[],[],["i","h","j"],[],[],["k","g","c","b"],[],["d","m","f"]]

worldIdList = [(world,0)]

goal = ["onTop,c,a"]
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


#
# Lots of helper functions which I wrote...
#

# Gets the number of stacks in the world
def getWorldLength(world):
	return len(world)

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
# Crucial functions which are used!
#


def test():
	return ["pick 1", "drop 2"]


# 
def getObjectStack(object):
	stack = 0
	for item in world:
		if object in item:
			return stack
		else:
			stack = stack+1

# A function which does different things depending on which relation the source and target objects have
def performMove(goal, world):
	#return["pick 1", "drop 2", "pick 3", "drop 2"]
	goal = ["onTop,c,a"]
	goalList = goal[0].split(",")

	relation = goalList[0]
	sourceObject = goalList[1]
	targetObject = goalList[2]

	sourceObjectStack = getObjectStack(sourceObject)
	targetObjectStack = getObjectStack(targetObject)

	if relation == "onTop":
		if isTargetObjectOnTop(targetObject, world):
			return ["pick " + str(sourceObjectStack)]
		else:
			return ["pick " + str(targetObjectStack)]

	elif relation == "inside":
		return "inside"
	elif relation == "above":
		return "dfsfd"
	elif relation == "under":
		return "under"
	elif relation == "beside":
		return "beside"
	elif relation == "leftOf":
		return "to the left"
	elif relation == "rightOf":
		return "to the right"

# Checks whether the target object is on top of a stack or not
def isTargetObjectOnTop(targetObject, world):
	topList = getTopObject(world)
	if targetObject in topList:
		return True
	else:
		return False


###
#
#
#
# TEST FUNCTIONS SEARCH BELOW HERE:
#
#
#
##


def checkStuff(object):
	stack = 0
	for item in world:
		if object in item:
			return stack
		else:
			stack = stack+1

def searchForPickUp(world, goal):
	closedSet = []
	openSet = []
	
	# heappush(openSet, (5, 'write code'))
	# heappush(openSet, (7, 'release product'))
	# heappush(openSet, (10, 'write spec'))
	# heappush(openSet, (3, 'create tests'))
	# return heappop(openSet)

	start = heuristic_cost_estimate(goal)
	heappush(openSet, (start, world))
	cameFrom = []

	g_score = [0]
	f_score = g_score[0] + heuristic_cost_estimate(goal)
	currentID = 0

	while openSet != []:
		current = heappop(openSet)
		print "CURRENT: ", current

		if (isGoal(current, goal)):
			return reconstruct_path(cameFrom, goal)

		closedSet.append(current)

		for eachNeighbour in performMove(goal, world):		
			if eachNeighbour in closedSet: # Fix later
				continue
			
			print current[1]
			print eachNeighbour[1]
			# temporaryCost = g_score[currentID] + moveDistance(current[1], eachNeighbour[1])
			currentID = currentID + 1

	# 		if ((neighbor not in openSet) or (temporaryCost < g_score[neighbor]):
	# 			cameFrom[neighbor] = current
	# 			g_score[neighbor]  = temporaryCost
	# 			f_score[neighbor]  = g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)

	# 			if (neighbor not in openSet):
	# 				openSet.put(neighbor)

def heuristic_cost_estimate(goal):
	goalList = goal[0].split(",")
	relation, objA, objB = goalList
	
	locA = getLocation(objA)
	locB = getLocation(objB)

	return abs((locA[1] - getStackHeight(locA[0])) + (locB[1] - getStackHeight(locB[0])))

def reconstructPath(cameFrom, goal):
	pass

def moveDistance(fromNode, toNode):
	start = -1
	end = -1
	
	for column in range(getWorldLength(world)):
		if (len(fromNode[column]) != len(toNode[column]) and start == -1):
			start = column
		elif (len(fromNode[column]) != len(toNode[column]) and end == -1):
			end = column
			
	return abs(end - start)	

def pick(column):
	return world.pop(column)

def drop(column):
	world.append(object)

#
def getLocation(object):	
	for column in range(getWorldLength(world)):
		for row in range(getStackHeight(column)):
			if object == getObject(column, row):
				return (column, row)

def getStackHeight(stack):
	return len(world[stack])

def getObject(column, row):
	return world[column][row]

# Checks whether the goal has been satisfied or not
def isGoal(world, goal):
	goalList = goal[0].split(",")

	relation = goalList[0]
	sourceObject = goalList[1]
	targetObject = goalList[2]

	sourceObjectLocation = getLocation(sourceObject)
	targetObjectLocation = getLocation(targetObject)

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

if __name__ == '__main__':
	# print performMove(["onTop,c,a"], world)
	#print getLocation("a")
	# print heuristic_cost_estimate(goal)
	# print moveDistance(world, world2)
	print searchForPickUp(world, goal)
	# print worldIdList
