"""
Module containing all the classes and related functions to the 
interpretation and semantic analysis of the parse_trees. 
"""



class Interpreter:
    
    """
    Main component of this module. Does semantic analysis of the
    parse_trees that can be used to resolve which objects are
    referred to.
    """
        
    def __init__(self):
        pass     

    def printOut():
        return "hello"

    def interpret(self, parseTree):
        """
        Takes a set of parse_trees and returns a set of goals in
        PDDL-like format
        
        Arguments: parse_trees
        Returns:   goals in PDDL-like format
        """
        
        goal = list()
        
        command = parseTree[0]
        
        if command == "take":
            entity = parseTree[1]
            goals.append([self.interpretEntity(entity)])
            
        elif command == "put":
            location = parseTree[1]
            goals.append([self.interpretLocation(location)])
                
        elif command == "move":
            entity   = parseTree[1]
            location = parseTree[2]
                
            goals.append([self.interpretEntity(entity), self.interpretLocation(location)])   
        return goal
        
    def interpretEntity(self, entity):
        """
        Interprets a part of the grammar called entity
        
        Arguments: An entity
        Returns:   A semantic representation of the entity
        """
        
        typeOfEntity = entity[0]
        
        if (typeOfEntity == "basic_entity"):
            typeOfEntity, quantifier, object = entity
            return [quantifier, self.modifyObject(object)]
            
        elif (typeOfEntity == "relative_entity"):
            typeOfEntity, quantifier, object, location = entity
            return [[quantifier, self.modifyObject(object)], [self.interpretLocation(location)]]
        
        else:
            return entity
            
    def interpretLocation(self, location): 
        """
        Interprets the part of the grammar called Location
        
        Arguments: A location
        Returns:   A semantic representation of the location
        """ 
        
        relative, relation, entity = location
        
        return [relation, self.interpretEntity(entity)]
    
    def modifyObject(self, object):
        """
        Modifies the object
        
        Arguments: An object
        Returns:   A modified object
        """  
        
        object = list(object)
        
        del object[0]
        
        for i in range (len(object)):
            if (object[i] == "-"):
                object[i] = ""
                
        return object
