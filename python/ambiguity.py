import math
import random

class AmbiguityResolver:
    
    def __init__(self, world, objects):
        ''' Takes a world object.
        '''
        self.objectsInWorld = objects
        self.worldPopulation = world
        
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
        ''' This is the main function that deals with solving the ambiguity, calling for clarification questions 
            and differentiating between quantifiers. It is used for both the source list of elements and target list of elements
            and calls the filterElements() function, to get rid of the elements that don't match the spatial description.
            The next step is interpreting the quantifiers. In case of "any" and "all", if the list of candidate objects has more than one
            object, it will pick one of them randomly.
            In case of "the" quantifier, if the filtered list of candidate objects has more than one candidate, the clarification questions will
            be used.
            First it will start searching for differences in attributes by calling the function getObjectDifferences and ask questions about 
            those attributes to narrow down the list. After this, if the resulting list of candidates (unformattedResult) still has more than one
            element, it will start checking the neighbours and ask questions about the candidates' positions according to their neighbours.
        '''
        quantifiers = ["any", "the", "all"]
            ## Save the first object in the reversed list, which is the last object of reference for the main object
        quantifier = ""
        relObj = parsedList.pop()
        if len(parsedList) == 1:
            quantifier = parsedList.pop()
        while len(parsedList) > 1:
            if parsedList[len(parsedList)-1] in quantifiers:
                quantifier = parsedList.pop()
            relation = parsedList.pop()
            mainObj = parsedList.pop()
            relObj = self.filterElements(mainObj, relation, relObj)
        if len(parsedList) == 1:
            quantifier = parsedList.pop()
        if relObj == 'floor':
                return relObj
        if quantifier == "the":
            if len(relObj) > 1:
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
            if len(relObj) == 1:
                return relObj[0]
            elif len(relObj) < 1:
                return -1
            else:
                return relObj[random.randrange(0, len(relObj)-1, 1)]
        if len(relObj) < 1:
            return -1
        else:
            return relObj[0]
    
    def selectByNeighbour(self, neighbourObjects, duplicateObject):
        '''This is the function that actually compares the neighbours on one direction for each object,
            and asks questions to eliminate or select objects according to the user's answer.
        '''
        direction = ["to the right of a", "below a", "to the left of a", "above a"]
        dir = 0
        while dir < len(neighbourObjects[0]):
            neighb = 0
            while neighb < len(neighbourObjects[dir]):
                if neighbourObjects[dir].count(neighbourObjects[dir][neighb]) == 1 and not neighbourObjects[dir][neighb] == "-":
                    while True:
                        answer = raw_input("Do you mean the "+ duplicateObject[1]+ " "+ duplicateObject[2]+ " "+ duplicateObject[0]+ " that is the closest "+
                            direction[dir]+ " "+ neighbourObjects[dir][neighb][1]+ " "+ neighbourObjects[dir][neighb][2]+
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
        '''This function saves in separate lists the neighbours to the left of all object candidates, those on top,
            to the right and under each candidate. Returns a list of 4 lists, left ontop right under, where each list position is the neighbour of a different object. 
            The goal is to be able to compare neighbours on one direction
            for all the candidates, in order to differentiate them and narrow down the list of candidate objects.
        '''
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
        '''
            Takes as input the answer, the index of the attribute difference (0=form, 1=size, 2=colour)
            and the actual value of the attribute that differs. If the answer is yes, it will select all elements that have
            as attribute the value given, otherwise it will eliminate from the list those objects sharing that value attribute.
        '''
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
        '''
            Function that asks questions based on the attribute differences. It takes a difference, and if that difference is in "form"
            it will ask about the form of the described object, narrowing down the list by calling the function cleanCandidates and returning it.
            If the difference is in colour or shape, the questions slightly differs, but the selection (cleanCandidates) is the same, according to the answer.
        '''
        while True:
            value = objCandidates[0][objDifference]
            if objDifference == 0:
                answer = raw_input("Did you mean a " + objCandidates[0][objDifference] +"? (Y/N)").upper()
            else:
                answer = raw_input("Did you mean the " + objCandidates[0][objDifference] +" "+ objCandidates[0][0] + "? (Y/N)").upper()
            if answer == 'Y' or answer == 'N':
                break
        objCandidates = self.cleanCandidates(objCandidates, answer, objDifference, value)
        return objCandidates
    
    def getObjectAttributes(self, objects):
        '''
            Function that takes as input a list of objects in terms of their coordinates
            and interacting with the objects' descriptions in the world it returns the list of
            same objects, but described by their attributes.
        '''
        objList = []
        oneObject = []
        for obj in objects:
            if not obj == "-":
                object = self.worldPopulation[obj[0]][obj[1]]
                attr = self.objectsInWorld[object]['form']
                oneObject.append(attr)
                attr = self.objectsInWorld[object]['size']
                oneObject.append(attr)
                attr = self.objectsInWorld[object]['color']
                oneObject.append(attr)
                objList.append(list(oneObject))
                del oneObject[:]
            else:
                objList.append("-")
        return objList
    
    def getObjectDifferences(self, objects):
        '''It creates a list for each attribute, containing each object's value for that attribute.
           So it will create a list of forms, a list of sizes and one of colours.
           In order to check for differences it transforms the list in a set and if there's more than
           one element in the list, there are one or more differences so it calls the function ask question
           to select objects by the first difference.
           This recursively calls itself taking as argument the result of asking the question and selecting objects.
           At the end it will return a list of candidates narrowed down (to preferably one element).
        '''
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
        return self.onTop(object, container)
    
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
        return None
       
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
                    if not objectToBeChecked[0] == 'anyform':
                        match = False
            if (objectToBeChecked[1] and 
                    self.objectsInWorld[object]['size'] != objectToBeChecked[1]):
                    match = False
            if (objectToBeChecked[2] and
                    self.objectsInWorld[object]['color'] != objectToBeChecked[2]):
                    match = False
            if match:
                location = self.getObjectCoordinates(object)
                if not location == None:
                    coords = tuple(self.getObjectCoordinates(object))
                    matchingObjects.append(coords)
        matchTuple = tuple(matchingObjects)
        return matchTuple
    
    def handleInput(self, inputList):
        ''' Separates the list received as parameter into action, source list, relation and a target list.
            The lists are parsed separately by calling the parse function, and then they are processed with the resolve function
            to resolve ambiguity and return a single goal.
        '''
        sourceList = []
        targetList = []
        source = True
        command = inputList.pop(0)
        sourceResult = 0
        targResult = 0
        if command == "move":
            for bigList in inputList[0]:
                if source:
                    sourceList = self.parse(bigList)
                    source = False
                else:
                    targetList = self.parse(bigList)
        elif command == "put" or command == "take":
            targetList = self.parse(inputList[0])
        if not command == 'take':
            relation = targetList.pop(0)
        if not len(sourceList) == 0:
            sourceResult = self.resolve(sourceList)
        targResult = self.resolve(targetList)
        if sourceResult == -1 or targResult == -1:
            return []
        if command == 'take':
            if targResult == 'floor':
                return command + "," + targResult
            else:
                return command + "," + self.worldPopulation[targResult[0]][targResult[1]]
        elif command == 'put':
            if targResult == 'floor':
                return command + "," + relation + "," + targResult
            else:
                return command + "," + relation + "," + self.worldPopulation[targResult[0]][targResult[1]]
        else:
            if sourceResult == 'floor':
                return command + "," + relation + "," + sourceResult + "," + self.worldPopulation[targResult[0]][targResult[1]]
            elif targResult == 'floor':
                return command + "," + relation + "," + self.worldPopulation[sourceResult[0]][sourceResult[1]] + "," + targResult
            else:
                return command + "," + relation + "," + self.worldPopulation[sourceResult[0]][sourceResult[1]] + "," + self.worldPopulation[targResult[0]][targResult[1]]

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
