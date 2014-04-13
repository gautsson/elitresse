import Queue.PriorityQueue
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
	openSet = Queue.PriorityQueue()
	start = (heuristic_cost_estimate(world, goal), world)
	openSet.put(start)
	cameFrom = []

	g_score = [0]
	f_score = g_score + heuristic_cost_estimate(world, goal)

	while openSet is not []:
		current = openSet.get()

		if (isGoal(current, goal)):
			return reconstruct_path(cameFrom, goal)

		closedSet.append(current)

		for eachNeighbour in performMove(current):		
			if eachNeighbour in closedSet: # Fix later
				continue
			
			temporaryCost = g_score[current] + moveDistance(current, neighbor)

			if ((neighbor not in openSet) or (temporaryCost < g_score[neighbor]):
				cameFrom[neighbor] = current
				g_score[neighbor]  = temporaryCost
				f_score[neighbor]  = g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)

				if (neighbor not in openSet):
					openSet.put(neighbor)

def isGoal(world, goal):
	pass

def heuristic_cost_estimate(world, goal):
	pass

def reconstructPath(cameFrom, goal):
	pass

def moveDistance(from, to):
	pass


def pick(column):
	pass

def drop(column):
	pass





if __name__ == '__main__':

	world = [["e"],["a","l"],[],[],["i","h","j"],[],[],["k","g","c","b"],[],["d","m","f"]]
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


	print performMove(["onTop,c,a"], world)
	