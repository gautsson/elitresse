from heapq import *
from copy import *
from gc import *

class Planner:
    
    def __init__(self, world, holding, objects):
        self.startWorld = world
        self.holding = holding
        self.objects = objects

      #  print gc.isenabled()
    #
    # Node class, which storesI information about all the states the world goes through
    #

    class Node:
        def __init__(self, parent, world, g, h, f):
            self.parent = parent
            self.world = world

            self.g = g
            self.h = h
            self.f = f
   
        def compareTo(self, node):
            return self.world == node.world 
    #
    # Rules class which holds the constraints
    #
    class Rules:
        def __init__(self, objects):
            self.ruleList = [self.ballInBox, self.notSupportedByBall, self.smallBeneathLarge,
                    self.containedInBox, self.boxIsSupported]
            self.objects = objects

        def applyRules(self, objectId, stackObjectId):
            object = self.objects[objectId]
            stackObject = self.objects[stackObjectId]

            for rule in self.ruleList:
                if rule(object, stackObject) == False:
                    return False

            return True

        # Balls must be in boxes or on the floor, otherwise they roll away 

        def ballInBox(self, object, stackObject): 
            if object["form"] == "ball":
                if stackObject["form"] == "box":
                    return True
                else:
                    return False

        # Balls cannot support anything

        def notSupportedByBall(self, object, stackObject):
            return not stackObject["form"] == "ball"

        # Small objects cannot support large objects

        def smallBeneathLarge(self, object, stackObject):
            if stackObject["size"] == "small" and object["size"] == "large":
                return False
            else:
                return True

        # Boxes cannot contain pyramids or planks of the same size

        def containedInBox(self, object, stackObject):
        #Boxes cannot contain pyramids or planks of the same size
        #ASK THE SUPERVISOR ABOUT THIS. Should small boxes be able to contain large pyramids or large planks ?!? Because according
        #to the specification, they should!
            if stackObject["form"] == "box":
                if object["form"] == "pyramid" and object["size"] == stackObject["size"]:
                    return False
                elif object["form"] == "plank" and object["size"] == stackObject["size"]:
                    return False
                else:
                    return True
            else:
                return True

        # Boxes can only be supported by tables or planks of the same size,
        # but large boxes can also be supported by large bricks.

        def boxIsSupported(self, object, stackObject):
        # Boxes can only be supported by tables or planks of the same size,
        # but large boxes can also be supported by large bricks.
            if object["form"] == "box":
                if stackObject["form"] == "table" and object["size"] == stackObject["size"]:
                    return True
                elif stackObject["form"] == "plank" and object["size"] == stackObject["size"]:
                    return True
                elif object["size"] == "large" and stackObject["form"] == "brick" and stackObject["size"] == "large":
                    return True
                else:
                    return False

# ----------------------------------------------------------

# Gets the stack of an object
    def getObjectStack(self, object, world):
        stack = 0
        for item in world:
            if object in item:
                return stack
            else:
                stack = stack+1

    # Starting function
    def startPlanning(self, goal):
        # Getting the relations, the source object and the target object
        # Example goal: ["move,leftOf,f,e"]
        #above f,e
        emptyStacks = self.getEmptyStacks(self.startWorld) 

        goalList = goal.split(",")
        command = goalList[0]

        if command == "move":
            relation = goalList[1]
            sourceObject = goalList[2]
            targetObject = goalList[3]

            #If the relation is above, onTop or inside, we check whether the constraints allow the goal to be executed
            
            #if preConstraintCheck(sourceObject, targetObject):
            return self.search(goal)
        
        elif command == "take":
            object = goalList[1]

            if self.holding:
                if self.holding == object:
                    return ["I am already holding the object"]
                else:
                    self.search(goal)
            else:
                self.holding = self.pick(self.startWorld, [stack for stack in range(len(self.startWorld)) if stack not in emptyStacks][0])
                self.search(goal)
        
        elif command == "put":
            relation = goalList[1]
            targetObject = goalList[2]

            goal = "move" + "," + relation + "," + self.holding + "," + targetObject
            
            #if preConstraintCheck(sourceObject, targetObject):
            
            print goal
            if not emptyStacks:
                print "1"
                for stack in len(self.startWorld):
                    if self.drop(self.startWorld, stack, self.holding):
                        return self.search(goal)
                    
            else:
                print "2"
                self.drop(self.startWorld, emptyStacks[0], self.holding)
                print self.startWorld
                return self.search(goal)
        
    def preConstraintCheck(self, relation, sourceObject, targetObject):
        rules = self.Rules(self.objects)

        return rules.applyRules(sourceObject, targetObject)
#
# The search function, our pride and joy
#

    def search(self, goal): 
        goalList = goal.split(",")
        command = goalList[0]

        closedSet = []
        openSet = []

        gScore = 0
        hScore = 0
        fScore = 0
    
        startNode = self.Node(None, self.startWorld, gScore, hScore, fScore)

        startTuple = (0, startNode)
        heappush(openSet, startTuple)

        while openSet != []:
            #for node in openSet:
            #    val, node = node
            #    print node.world
            currentNode = heappop(openSet)[1]

            if (self.isGoal(currentNode.world, goal)):
                return self.reconstructPath(currentNode, list())

            closedSet.append(currentNode)

            for neighbor in self.performMove(currentNode, command):
                cost = currentNode.g + self.movementCost(currentNode, neighbor)      

                nodeInOpenSet = self.isNodeInOpenSet(openSet, neighbor)

                if (nodeInOpenSet[1] != None and cost < nodeInOpenSet[1].g):
                    self.removeNodeFromSet(openSet, nodeInOpenSet[0])

                nodeInClosedSet = self.isNodeInClosedSet(closedSet, neighbor)

                if (nodeInOpenSet[1] == None and nodeInClosedSet == None):
                    neighbor.g = cost
                    neighbor.h = self.heuristic_cost_estimate(neighbor.world, goal)
                    neighbor.f = neighbor.g + neighbor.h
                    
                    neighbor.parent = currentNode
                    neighborTuple = (neighbor.f, neighbor)
                    heappush(openSet, neighborTuple)

#
# Helper functions for the search function 
#

    def isNodeInOpenSet(self, openSet, node):
        index = 0
        for compNode in openSet:
            if node.compareTo(compNode[1]):
                return (index, compNode[1])
            index = index + 1
    
        return (0, None)

    def isNodeInClosedSet(self, closedSet, node):
        for compNode in closedSet:
            if node.compareTo(compNode):
                return compNode
    
        return None

    def removeNodeFromSet(self, set, index):
        set.pop(index)

#A command is passed to performMove, where 
# 0 corresponds to do a pick and a drop
# 1 correponds to do a pick command
# 2 corresponds to do a drop command

    def performMove(self, node, command):
        neighbors = list()
        
        if command == "take":
            for dropStack in [stack for stack in range (len(self.startWorld))]:        
                for pickStack in [stack for stack in range (len(self.startWorld)) if not stack == dropStack]:
                    neighborNode = deepcopy(node)
                    yugff
                    if not self.drop(neighborNode.world, dropStack, self.holding):
                        continue
                    
                    tryHolding = self.pick(neighborNode.world, pickStack)
                    
                    if tryHolding == None:
                        continue
                    else:
                        self.holding = tryHolding

                    neighbors.append(neighborNode)
        
        elif command == "move":
            for pickStack in [stack for stack in range (len(node.world)) if (len (node.world[stack]) > 0)]:        
                for dropStack in [stack for stack in range (len(self.startWorld)) if not stack == pickStack]:
                    neighborNode = deepcopy(node)
                    object = self.pick(neighborNode.world, pickStack)

                    if (object == None):
                        continue

                    if not self.drop(neighborNode.world, dropStack, object):
                        continue
                    
                    neighbors.append(neighborNode)

        return neighbors    
    
    def pick(self, world, stack):
        if (self.getStackHeight(world, stack) > 0):
            return world[stack].pop()
        else:
            return None

    def drop(self, world, stack, object):
        rules = self.Rules(self.objects)


        if len (world[stack]) == 0:
            world[stack].append(object)
            return True
        else:
            stackObject = world[stack][-1]
        
            if (rules.applyRules(object, stackObject)):
                world[stack].append(object)
                return True
            else:
                return False

    # FIX HEURISTIC FOR TAKE AND DROP
    def heuristic_cost_estimate(self, world, goal):
        goalList = goal.split(",")
        command = goalList[0]
       
        
        if command == "take":
            object = goalList[1]
            if self.holding == object:
                return 0
    
            else:
                locObject = self.getLocation(world, object)
                stackHeight = self.getStackHeight(world, locObject[0])

                return stackHeight - locObject[1]

        elif command == "move":    
            objA = goalList[2]
            objB = goalList[3]

            locA = self.getLocation(world, objA)
            locB = self.getLocation(world, objB)
            
            return abs((locA[1] - self.getStackHeight(world, locA[0])) + (locB[1] - self.getStackHeight(world, locB[0]))) * (len(self.startWorld) / 5)

    def reconstructPath(self, node, commandString):
        if node.parent == None: # Base case
            return commandString
        else:
            parentNode, command = self.parseNode(node)
            return self.reconstructPath(parentNode, command + commandString)

    def parseNode(self, node):  
        parentNode = node.parent
        parentWorld = node.parent.world
        currentWorld = node.world
        worldLength = len (parentWorld)
        list = []

        parentWorldConcat = [value for sublist in parentWorld for value in sublist]
        currentWorldConcat = [value for sublist in currentWorld for value in sublist]
        pickString = ""
        dropString = ""

        if (len (parentWorldConcat) == len (currentWorldConcat)):
            for i in range(0,worldLength):
                if currentWorld[i] < parentWorld[i]:
                    pickString = "pick " + str(i)
                    
                if currentWorld[i] > parentWorld[i]:
                    dropString = "drop " + str(i)

            list.append(pickString)
            list.append(dropString) 
            return (parentNode, list)

        elif (len (parentWorldConcat) > len (currentWorldConcat)):
            # This loop gets run if the last command is pick, i.e. the arm ends up holding an object
            changedElement = (set(parentWorldConcat) - set(currentWorldConcat)).pop()
            theStack = getObjectStack(changedElement, parentWorld)
            newCommand = "pick " + str(theStack)
            list.append(newCommand)
            return (parentNode, list)
        else:
            # This loop gets run if the first command is a drop, i.e. if the arm was holding an object
            changedElement = (set(currentWorldConcat) - set(parentWorldConcat)).pop()
            theStack = getObjectStack(changedElement, currentWorld)
            newCommand = "drop " + str(theStack)
            list.append(newCommand)
            return (parentNode, list)

    def movementCost(self, fromNode, toNode):
        fromWorld = fromNode.world
        toWorld = toNode.world
        start = -1
        end = -1

        for column in range(self.getWorldLength(self.startWorld)):
            if (len(fromWorld[column]) != len(toWorld[column]) and start == -1):
                start = column
            elif (len(fromWorld[column]) != len(toWorld[column]) and end == -1):
                end = column

        return abs(end - start)


    # Checks whether the goal has been satisfied or not
    def isGoal(self, world, goal):
        goalList = goal.split(",")
        command = goalList[0]
        
        print "world"
        print  world
        print "holding"
        print self.holding

        if command == "take":
            sourceObject = goalList[1]
            sourceObjectLocation = self.getLocation(world, sourceObject)

            return not sourceObjectLocation
        elif command == "move":
            relation = goalList[1]
            sourceObject = goalList[2]
            targetObject = goalList[3]
            sourceObjectLocation = self.getLocation(world, sourceObject)
            targetObjectLocation = self.getLocation(world, targetObject)

            if relation == "onTop" or relation == "inside":
                return sourceObjectLocation[0] == targetObjectLocation[0] and sourceObjectLocation[1] == targetObjectLocation[1] + 1
            elif relation == "above":
                return sourceObjectLocation[0] == targetObjectLocation[0] and sourceObjectLocation[1] > targetObjectLocation[1]
            elif relation == "under":
                return sourceObjectLocation[0] == targetObjectLocation[0] and sourceObjectLocation[1] < targetObjectLocation[1]
            elif relation == "beside":
                return (sourceObjectLocation[0] == targetObjectLocation[0] + 1) or (sourceObjectLocation[0] == targetObjectLocation[0] - 1)
            elif relation == "leftOf":
                return sourceObjectLocation[0] < targetObjectLocation[0]
            elif relation == "rightOf":
                return sourceObjectLocation[0] > targetObjectLocation[0]

    # Utility functions, remove these functions
    def getWorldLength(self, world):
        return len(world)

    def getStackHeight(self, world, stack):
        return len(world[stack])

    def getObject(self, world, column, row):
        return world[column][row]

    def getObjectDescription(self, object):
        return self.objects[object]

    def getLocation(self, world, object): 
        for column in range(self.getWorldLength(world)):
            for row in range(self.getStackHeight(world, column)):
                if object == self.getObject(world, column, row):
                    return (column, row)

    # Gets all the empty stacks in the world
    def getEmptyStacks(self, world):
        x = []
        for stack, object in enumerate(world):
            if not object:
                x.append(stack)
        return x

    

if __name__ == '__main__':
    #print reconstructPath(node9, [])
        # medium = [["e"],["a","l"],[],[],["i","h","j"],[],[],["k","g","c","b"],[],["d","m","f"]
    world = [["e"],[],[],["k"]]
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
    "m": { "form":"box",     "size":"small",  "color":"blue"  }
    }

    goal = "take,k"
    planner = Planner(world, "", objects)
    #print planner.pick(world, 0)
   #print world[0]
#    print planner.heuristic_cost_estimate(world, goal)
    print planner.startPlanning(goal)
        #print planner.search(goal)
        #goal = "above,e,j" 
        #test = self.isGoal(medium,goal) 
