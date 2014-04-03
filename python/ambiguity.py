class AmbiguityResolver:
    
    def __init__(self, goals, world):
        self.world = world
        self.objectsInWorld = world.worldObjects
        self.worldPopulation = world.population
        
    def resolve(self, operation):
        #dostuff
        #firstObject = getObjectIndex(something)
        #secondObject = getObjectIndex(somethingElse)
        pass
    def onTop(self, topObject, botObject):
        if top[0] == bot[0] and top[1] < bot[1]:
            return true
        return false
    def inside(self, object, container):
        pass
    def rightOf(self, leftObject, rightObject):
        pass
    def leftOf(self, leftObject, rightObject):
        pass
    def above(self, topObject, botObject):
        pass
    def under(self, topObject, botObject):
        pass
    def beside(self, object, nextObject):
        pass
    def getObjectIndex(self, object):
        for worldIndex in self.population:
            for stackIndex in worldIndex:
                if stackIndex == object:
                    return [worldIndex,stackIndex]
                
    
    def getMatchingObjects(self, objectsToBeChecked):
        '''Finds matching world objects.
            It takes a list of objects and a list of world objects,
             then searches for matches for each object,
            Returns a list of matches for each object, in the same order as in the list
            sent to the function.
        '''
        matchingObjects = []
        matches = []
        for objectBeingChecked in objectsToBeChecked:
            del matchingObjects[:]
            for object in self.objectsInWorld:
                match = True
                if (objectBeingChecked[0] and 
                        self.objectsInWorld[object]['form'] != objectBeingChecked[0]):
                        match = False
                if (objectBeingChecked[1] and 
                        self.objectsInWorld[object]['size'] != objectBeingChecked[1]):
                        match = False
                if (objectBeingChecked[2] and
                        self.objectsInWorld[object]['color'] != objectBeingChecked[2]):
                        match = False
                if match:
                    matchingObjects.extend(object)
            matches.append(list(matchingObjects))
        return matches
    
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
            
class Tester:
    
    def __init__(self, testAtt):
        self.oneAtt = testAtt
        print "made a class and its attribute is ", self.oneAtt
    
        
if __name__ == '__main__':
    mySmallWorld = World("small")
    myMediumWorld = World("medium")
    ambSmallSolver = AmbiguityResolver("someGoal", mySmallWorld)
    ambMediumSolver = AmbiguityResolver("someOtherGoal", myMediumWorld)
    smallListOfObjects = [["ball","",""],["","","black"],["plank", "small", "green"],
                        ["table", "large", "blue"]]
    mediumListOfObjects = [["table", "large", "red"],["box","",""],
                           ["plank", "small", "green"],["","","white"]]
    smallMatches = ambSmallSolver.getMatchingObjects(smallListOfObjects)
    mediumMatches = ambMediumSolver.getMatchingObjects(mediumListOfObjects)
    
    
    print "------------------------------"
    print "Testing small-sized world"
    print "It should print: [[e,f],[f],[],[g]]"
    print "Matches found: ", smallMatches
    
    
    print "------------------------------"
    print "Testing medium-sized world"
    print "It should print: [[],[k,lm,l],[d],[b,e]]"
    print "Matches found: ", mediumMatches
    
        
        