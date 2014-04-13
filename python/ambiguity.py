import math

class AmbiguityResolver:
    
    def __init__(self, goals, world):
        self.world = world
        self.objectsInWorld = world.worldObjects
        self.worldPopulation = world.population
        
    def filterElements(self, objectList, relation, otherObjectList):
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
        
        quantifiers = {
                       "any": "a",
                       "the": "t",
                       "all": "al"
                       }
            ## Reverse the list
        parsedList[::-1]
            ## Save the first object in the reversed list, which is the last object of reference for the main object
        relObj = parsedList.pop()
        print relObj
        print len(parsedList)
        while len(parsedList) > 1:
            if parsedList[len(parsedList)-1] in quantifiers:
                #manage the ambiguity later using the quantifier
                quantifier = parsedList.pop()
                print "quantifiers"
            relation = parsedList.pop()
            print "relation"
            mainObj = parsedList.pop()
            relObj = self.filterElements(mainObj, relation, relObj)
        return relObj
        
        
    def onTop(self, topObject, botObject):   
        return (botObject == "floor" and topObject[1] == 0) or (topObject[0] == botObject[0] and topObject[1]-1 == botObject[1])
            
    def inside(self, object, container):
        return onTop(object, container)
    
    def rightOf(self, right, left):
        return right[0] > left[0]
    
    def leftOf(self, left, right):
        return left[0] < right[0]
    
    def above(self, topObject, botObject):
        return topObject[1] > botObject[1]
    
    def under(self, botObject, topObject):
        return botObject < topObject
    def beside(self, object, nextObject):
        return math.fabs(object[0]-nextObject[0]) == 1

    def convertToPDDL(self, sourceList, rel, targetList):
            pddl = []
            relation = rel
           
            if len(sourceList) > 1 and len(targetList) > 1:
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
            return pddl


    
    def getObjectCoordinates(self, object):
        wIndex = 0
        for worldIndex in self.worldPopulation:
            sIndex = 0
            for stackIndex in worldIndex:
                if stackIndex == object:
                    return [wIndex,sIndex]
                sIndex = sIndex + 1
            wIndex = wIndex + 1
                
    def findPlacesOnTheFloor(self):
        wIndex = 0
        freeFloorPlaces = []
        for worldIndex in self.worldPopulation:
            if not worldIndex:
                freeFloorPlaces.append((wIndex,0))
            wIndex = wIndex + 1
        return freeFloorPlaces    
    def getMatchingObjects(self, objectToBeChecked):
        '''Finds matching world objects.
            it takes an object and compares it attribute by attribute
            to world objects. Upon finding a match, it calls getObjectCoordinates.
            Returns a tuple of tuples 
        '''
        matchingObjects = []
        #matches = []
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
        #matches.append(list(matchingObjects))
        return matchTuple
    
    def handleInput(self, inputList):
        sourceList = []
        targetList = []
        source = True
        for bigList in inputList[0]:
            if source:
                sourceList = self.parse(bigList)
                source = False
            else:
                targetList = self.parse(bigList)
        action = targetList.pop(0)
        print "Source"
        print sourceList
        sourceResult = self.resolve(sourceList)
        print "source result"
        print sourceResult
        print targetList
        print "target result"
        targResult = self.resolve(targetList)
        print targResult
          ## If the target is the floor, find all the places available on the floor
        if targResult == "floor":
            targResult = self.findPlacesOnTheFloor()
        pddl = self.convertToPDDL(sourceResult, action, targResult)
        print "PDDL = "
        print pddl
        
        
    def parse(self, inputList):
        
        dummyList = []
        if self.isDone(inputList):
            #print inputList
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
        for something in parentList:
            if isinstance(something, list):
                return True
        return False
    
    def isDone(self, testList):
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
            
class Tester:
    
    def __init__(self, testAtt):
        pass
        #self.oneAtt = testAtt
        #print "made a class and its attribute is ", self.oneAtt
    
        
if __name__ == '__main__':
    
    myMediumWorld = World("medium")
    ambMediumSolver = AmbiguityResolver("someGoal", myMediumWorld)
    #ambMediumSolver.resolve(((1,1),(0,0)), "leftOf", ((0,0),(7,0)))
    ambMediumSolver.handleInput([[[['the', ['plank', '', '']], [['ontop', [['the', ['table', '', '']], [['rightof', ['the', ['box', '', 'red']]]]]]]], ['ontop', [['the', ['ball', '', 'white']], [['ontop', 'floor']]]]]])
    #ambMediumSolver.handleInput([[['the', ['ball', '', 'white']], ['ontop', 'floor']]])

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