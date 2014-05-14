import math
import random

class AmbiguityResolver:
    
    def __init__(self, world):
        ''' Takes a world object.
        '''
        self.world = world
        self.objectsInWorld = world.worldObjects
        self.worldPopulation = world.population
        
    def filterElements(self, objectList, relation, otherObjectList):
        ''' Takes 2 lists of possible marching objects for 2 object description and 
            the spatial relation between them and returns just those coordinates that
            match the spatial relation
        '''
        selectedList = []
        functions = {
                "above": self.above,
                "ontop": self.onTop,
                "inside": self.inside,
                "rightof": self.rightOf,
                "leftof": self.leftOf,
                "under": self.under,
                "beside": self.beside }
        for item in objectList:
            if otherObjectList == "floor":
                if functions[relation](item, otherObjectList):
                    selectedList.append(item)
            else:
                for otherItem in otherObjectList:
                    if functions[relation](item,otherItem):
                        selectedList.append(item)
        return list(set(selectedList))
        
    def resolve(self, parsedList):
        ''' This is used for both the source list of elements and target list of elements
            and calls the filterElements() function, to get rid of the elements that don't
            match with the spatial description
        '''
        quantifiers = ["any", "the", "all"]
            ## Reverse the list
        parsedList[::-1]
            ## Save the first object in the reversed list, which is the last object of reference for the main object
        quantifier = ""
        relObj = parsedList.pop()
        if len(parsedList) < 2:
            quantifier = parsedList.pop()
        while len(parsedList) > 1:
            if parsedList[len(parsedList)-1] in quantifiers:
                quantifier = parsedList.pop()
            relation = parsedList.pop()
            mainObj = parsedList.pop()
            relObj = self.filterElements(mainObj, relation, relObj)
        if quantifier == "the":
            if len(relObj) > 1 and not relObj == 'floor' :
                objectAttributes = self.getObjectAttributes(relObj)
                unformattedResult = self.getObjectDifferences(objectAttributes)
                result = self.getMatchingObjects(unformattedResult[0])
                if len(unformattedResult) > 1:
                    range = 1
                    while (range < len(self.worldPopulation)):
                        attributeList = []
                        neighbours = self.getNeighbours(result, range)
                        for neigh in neighbours:
                            attributes = self.getObjectAttributes(neigh)
                            attributeList.append(list(attributes))
                        rawResult = self.selectByNeighbour(attributeList, unformattedResult[0])
                        if not rawResult == -1:
                            return result[rawResult]
                        range = range + 1 
                else:
                    return result[0]
                       
        elif quantifier == "any" or quantifier == "all":
            return relObj[random.randrange(0, len(relObj)-1, 1)]
        return relObj[0]
    
    def selectByNeighbour(self, neighbourObjects, duplicateObject):
        direction = ["to the right of a", "below a", "to the left of a", "above a"]
        dir = 0
        while dir < len(neighbourObjects[0]):
            neighb = 0
            while neighb < len(neighbourObjects[dir]):
                if neighbourObjects[dir].count(neighbourObjects[dir][neighb]) == 1 and not neighbourObjects[dir][neighb] == "-":
                    while True:
                        answer = raw_input("Do you mean the "+ duplicateObject[2]+ " "+ duplicateObject[1]+ " "+ duplicateObject[0]
                            + " that is the closest "+
                            direction[dir]+ " "+ neighbourObjects[dir][neighb][2]+ " "+ neighbourObjects[dir][neighb][1]+
                                                     " "+ neighbourObjects[dir][neighb][0]+ " ? (Y/N)").upper()
                        if answer == "Y":
                            return neighb
                        if answer == "N":
                            if (len(neighbourObjects[dir]) - neighb) == 2:
                                return neighb + 1
                            elif (len(neighbourObjects[dir]) - neighb) == 1 and len(neighbourObjects[dir]) == 2:
                                return neighb - 1
                            else:
                                neighb = neighb + 1
                                break
                else:
                    neighb = neighb + 1
            dir = dir + 1
        return -1

    def getNeighbours(self, objCandidates, range):
        candidatesNeighb = []
        leftNeighbours = []
        topNeighbours = []
        rightNeighbours = []
        bottomNeighbours = []
        for obj in objCandidates:
            if obj[0]-range > -1 and len(self.worldPopulation[obj[0]-range]) >= 1:
                leftNeighbours.append((obj[0]-range, len(self.worldPopulation[obj[0]-range]) - 1))
            else:
                leftNeighbours.append('-')
                
            if len(self.worldPopulation[obj[0]]) > obj[1]+range:
                topNeighbours.append((obj[0], obj[1]+range))
            else:
                topNeighbours.append('-')
                
            if obj[0]+range < len(self.worldPopulation) and len(self.worldPopulation[obj[0]+range]) >= 1:
                rightNeighbours.append((obj[0]+range, len(self.worldPopulation[obj[0]+range]) - 1))
            else:
                rightNeighbours.append('-')
                
            if obj[1]-range > -1:
                bottomNeighbours.append((obj[0], obj[1]-range))
            else:
                bottomNeighbours.append('-')
        candidatesNeighb.append(leftNeighbours)
        candidatesNeighb.append(topNeighbours)
        candidatesNeighb.append(rightNeighbours)
        candidatesNeighb.append(bottomNeighbours)
        return candidatesNeighb
            
        
    def cleanCandidates(self, objCandidates, answer, difference, value):
        newCandidates = []
        if answer == 'Y':
            for obj in objCandidates:
                if obj[difference] == value:
                    newCandidates.append(obj)
        else:
            for obj in objCandidates:
                if not obj[difference] == value:
                    newCandidates.append(obj)
        return newCandidates
    
    def askQuestion(self, objDifference, objCandidates):
        while True:
            value = objCandidates[0][objDifference]
            answer = raw_input("Did you mean the " + value +" "+ objCandidates[0][0] + "? (Y/N)").upper()
            if answer == 'Y' or answer == 'N':
                break
        objCandidates = self.cleanCandidates(objCandidates, answer, objDifference, value)
        return objCandidates
        #if len(objCandidates) == 1:
         #   return objCandidates
        #else:
         #   self.getObjectDifferences(objCandidates)
    
    def getObjectAttributes(self, objects):
        objList = []
        oneObject = []
        for obj in objects:
            if not obj == "-":
                object = self.worldPopulation[obj[0]][obj[1]]
                attr = self.objectsInWorld[object]['form']
                oneObject.append(attr)
                object = self.worldPopulation[obj[0]][obj[1]]
                attr = self.objectsInWorld[object]['size']
                oneObject.append(attr)
                object = self.worldPopulation[obj[0]][obj[1]]
                attr = self.objectsInWorld[object]['color']
                oneObject.append(attr)
                objList.append(list(oneObject))
                del oneObject[:]
            else:
                objList.append("-")
        return objList
    
    def getObjectDifferences(self, objects):
        attributes = ['form', 'size', 'color']
        i = 0
        while i < 3:
            attrList = []
            for obj in objects:
                attrList.append(obj[i]);
            attrList = set(attrList);
            if len(attrList) > 1:
                return self.getObjectDifferences(self.askQuestion(i, objects))
            i = i + 1
        return objects
        
    def onTop(self, topObject, botObject): 
        ''' Returns true if a given object is on top of another given object.
        '''  
        return (botObject == "floor" and topObject[1] == 0) or (topObject[0] == botObject[0] and topObject[1]-1 == botObject[1])
            
    def inside(self, object, container):
        ''' Returns true if a given object is inside of another given object.
        '''
        return onTop(object, container)
    
    def rightOf(self, right, left):
        '''Returns true if a given object is right of another given object.
        '''
        return right[0] > left[0]
    
    def leftOf(self, left, right):
        '''Returns true if a given object is left of another given object.
        '''
        return left[0] < right[0]
    
    def above(self, topObject, botObject):
        ''' Returns true if a given object is above another given object.
        '''
        return topObject[1] > botObject[1]
    
    def under(self, botObject, topObject):
        ''' Returns true if a given object is under another given object. 
        '''
        return botObject < topObject
    
    def beside(self, object, nextObject):
        ''' Returns true if a given object is beside another given object.
        '''
        return math.fabs(object[0]-nextObject[0]) == 1

    def convertToPDDL(self, source, relation, target):
            ''' Takes a source object, a relation and a target object
            and converts it into PDDL in order to allow processing by the planner.
            Returns a PDDL goal.
            '''
            return ((relation,source, target))
            '''if len(sourceList) > 1 and len(targetList) > 1:
                pddl.append("or")
                for item in sourceList:
                    for otherItem in targetList:
                        pddl.append((relation,item,otherItem))
                       
            elif len(sourceList) > 1:
                pddl.append("or")
                for item in sourceList:    
                    pddl.append((relation,item,targetList[0]))
            elif len(targetList) > 1:
                pddl.append("or")
                for item in targetList:
                    pddl.append((relation,sourceList[0],item))
            else:
                pddl.append((relation, sourceList[0], targetList[0]))
            return pddl'''


    
    def getObjectCoordinates(self, object):
        ''' Searches the world for a given object and returns its coordinates.
        '''
        wIndex = 0
        for worldIndex in self.worldPopulation:
            sIndex = 0
            for stackIndex in worldIndex:
                if stackIndex == object:
                    return [wIndex,sIndex]
                sIndex = sIndex + 1
            wIndex = wIndex + 1
       
    def findPlacesOnTheFloor(self):
        ''' Searches for all places that are available on the floor
        '''
        wIndex = 0
        freeFloorPlaces = []
        for worldIndex in self.worldPopulation:
            if not worldIndex:
                freeFloorPlaces.append((wIndex,0))
            wIndex = wIndex + 1
        return freeFloorPlaces    
    def getMatchingObjects(self, objectToBeChecked):
        '''Finds matching world objects.
            Takes an object and compares it attribute by attribute
            to world objects. Upon finding a match, it calls getObjectCoordinates.
            Returns a tuple of tuples with coordinates for the matches found.
        '''
        matchingObjects = []
        for object in self.objectsInWorld:
            match = True
            if (objectToBeChecked[0] and 
                    self.objectsInWorld[object]['form'] != objectToBeChecked[0]):
                    match = False
            if (objectToBeChecked[1] and 
                    self.objectsInWorld[object]['size'] != objectToBeChecked[1]):
                    match = False
            if (objectToBeChecked[2] and
                    self.objectsInWorld[object]['color'] != objectToBeChecked[2]):
                    match = False
            if match:
                coords = tuple(self.getObjectCoordinates(object))
                matchingObjects.append(coords)
        matchTuple = tuple(matchingObjects)
        return matchTuple
    
    def handleInput(self, inputList):
        ''' Separates the list received as parameter into a source list and a target list,
            which are parsed separately by calling the parse function.
        '''
        sourceList = []
        targetList = []
        source = True
        for bigList in inputList[0]:
            if source:
                sourceList = self.parse(bigList)
                source = False
            else:
                targetList = self.parse(bigList)
        relation = targetList.pop(0)
        sourceResult = self.resolve(sourceList)
        targResult = self.resolve(targetList)
          ## If the target is the floor, find all the places available on the floor
        if targResult == "floor":
            targResult = self.findPlacesOnTheFloor()
        print (relation, self.worldPopulation[sourceResult[0]][sourceResult[1]], self.worldPopulation[targResult[0]][targResult[1]])
        #pddl = self.convertToPDDL(sourceResult, relation, targResult)
        return (relation, self.worldPopulation[sourceResult[0]][sourceResult[1]], self.worldPopulation[targResult[0]][targResult[1]])
        
    def parse(self, inputList):
        ''' Takes a list from the interpreter and parses it to a format
            which will allow processing through disambiguation methods.
            Works recursively by eliminating sublists from the parameter inputList.
            Returns a list without sublists.
        '''
        dummyList = []
        if self.isDone(inputList):
            return inputList
        else:
            for innerList in inputList:
                if self.hasSubList(innerList):
                    for item in innerList:
                        dummyList.append(item)
                elif isinstance(innerList,list) and len(innerList)==3:
                    dummyList.append(self.getMatchingObjects(innerList))
                elif isinstance(innerList, list):
                    for i in innerList:
                        dummyList.append(i)
                else:
                    dummyList.append(innerList)
                        
            return self.parse(dummyList)
        
    def hasSubList(self, parentList):
        '''Simple method for checking whether a list contains any sublists.
        '''
        for something in parentList:
            if isinstance(something, list):
                return True
        return False
    
    def isDone(self, testList):
        ''' Simple method for checking whether or not there are
            unparsed elements in a list.
            Returns true if no unparsed elements are detected.
        
        '''
        for item in testList:
            if isinstance(item,list):
                for subItem in item:
                    if isinstance(subItem,list):
                        return False
                    elif len(item)==3:
                        return False
        return True
            
    
class World:
    
    def __init__(self, size):
        ''' Represents the world.
            size can be either small, medium, complex or impossible.
            Creates a world population and keeps a dictionary of objects in the world.
            This class is likely to be moved later but has been created here
            to facilitate testing.
            
        '''

        if size == "small":
            self.population = [["e"],["g","l"],[],["k","m","f"],[]]
            self.worldObjects = {
        "e": { "form":"ball",    "size":"large",  "color":"white" },
        "f": { "form":"ball",    "size":"small",  "color":"black" },
        "g": { "form":"table",   "size":"large",  "color":"blue"  },
        "k": { "form":"box",     "size":"large",  "color":"yellow"},
        "l": { "form":"box",     "size":"large",  "color":"red"   },
        "m": { "form":"box",     "size":"small",  "color":"blue"} }
            
        elif size == "medium":
            self.population = [["e"],["a","l"],[],[],["i","h","j"],[],[],
                                        ["k","g","c","b"],[],["d","m","f"]]
            self.worldObjects = {
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
        
        elif size == "complex":
            self.population = [["e"],["a","l"],["i","h","j"],
                                    ["c","k","g","b"],["d","m","f"]]
            
            self.worldObjects = {
        "a": { "form":"brick",   "size":"large",  "color":"yellow" },
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
            
        elif size == "impossible":
            self.population = [["lbrick1","lball1","sbrick1"], [],
                               ["lpyr1","lbox1","lplank2","sball2"], [],
                               ["sbrick2","sbox1","spyr1","ltable1","sball1"]]
            self.worldObjects = {
        "lbrick1": { "form":"brick",   "size":"large",  "color":"green" },
        "sbrick1": { "form":"brick",   "size":"small",  "color":"yellow" },
        "sbrick2": { "form":"brick",   "size":"small",  "color":"blue" },
        "lplank1": { "form":"plank",   "size":"large",  "color":"red"   },
        "lplank2": { "form":"plank",   "size":"large",  "color":"black"   },
        "splank1": { "form":"plank",   "size":"small",  "color":"green" },
        "lball1":  { "form":"ball",    "size":"large",  "color":"white" },
        "sball1":  { "form":"ball",    "size":"small",  "color":"black" },
        "sball2":  { "form":"ball",    "size":"small",  "color":"red" },
        "ltable1": { "form":"table",   "size":"large",  "color":"green"  },
        "stable1": { "form":"table",   "size":"small",  "color":"red"   },
        "lpyr1":   { "form":"pyramid", "size":"large",  "color":"white"},
        "spyr1":   { "form":"pyramid", "size":"small",  "color":"blue"   },
        "lbox1":   { "form":"box",     "size":"large",  "color":"yellow"},
        "sbox1":   { "form":"box",     "size":"small",  "color":"red"   },
        "sbox2":   { "form":"box",     "size":"small",  "color":"blue"} }
            
if __name__ == '__main__':
    '''
        This method is purely for testing purposes of the above functions. 
    '''
    #myMediumWorld = World("medium")
    #ambMediumSolver = AmbiguityResolver("someGoal", myMediumWorld)
    #ambMediumSolver.resolve(((1,1),(0,0)), "leftOf", ((0,0),(7,0)))
    #ambMediumSolver.handleInput([[['the', ['ball', '', 'white']], ['inside', [['the', ['box', '', '']], [['above', ['the', ['plank', '', '']]]]]]]])
    #ambMediumSolver.handleInput([[['the', ['ball', '', 'black']], ['beside', [['any', ['pyramid', '', '']], [['ontop', 'floor']]]]]])

    '''f = ambSmallSolver.getObjectCoordinates("f")
    m = ambSmallSolver.getObjectCoordinates("m")
    print "----Should be True, False all the time-----"
    print ambSmallSolver.onTop(f, m)
    print ambSmallSolver.onTop(m, f)
    e = ambSmallSolver.getObjectCoordinates("e")
    print ambSmallSolver.rightOf(f, e)
    print ambSmallSolver.rightOf(m, f)
    print ambSmallSolver.leftOf(e, f)
    print ambSmallSolver.leftOf(m, e)
    print ambSmallSolver.above(f, e)
    l = ambSmallSolver.getObjectCoordinates("l")
    print ambSmallSolver.above(l, m)
    print ambSmallSolver.under(e, f)
    print ambSmallSolver.under(f, l)
    print ambSmallSolver.beside(e, l)
    print ambSmallSolver.beside(l, e)
    print ambSmallSolver.beside(m, l)
    '''
