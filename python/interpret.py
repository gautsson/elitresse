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
        
    def interpret(self, parse_trees):
        """
        Takes a set of parse_trees and returns a set of goals in
        PDDL-like format
        
        Arguments: parse_trees
        Returns:   goals in PDDL-like format
        """
        
        goals = list()
        
        for eachParseTree in parse_trees:
            command = eachParseTree[0]
        
            if command == "take":
                entity = eachParseTree[1]
                
                goals.append[self.interpretEntity(entity)]
            
            elif command == "put":
                location = eachParseTree[1]
                
                goals.append[self.interpretLocation(location)]
                
            elif command == "move":
                entity   = eachParseTree[1]
                location = eachParseTree[2]
                
                goals.append([self.interpretEntity(entity), self.interpretLocation(location)])   
            
        print goals
        return goals
        
    def interpretEntity(self, entity):
        """
        Interprets a part of the grammar called entity
        
        Arguments: An entity
        Returns:   A semantic representation of the entity
        """
        
        print entity
        
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