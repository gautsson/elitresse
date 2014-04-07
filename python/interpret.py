class Interpreter:
    
                   
    def __init__(self):
        None
        
    def interpret(self, parse_trees):
        goals = list()
        
        for eachParseTree in parse_trees:
            command = eachParseTree[0]
        
            if command == "take":
                print "take"
                entity = eachParseTree[1]
                
                #entity = interpretEntity(entity)
            
            elif command == "put":
                print 'put'
                location = eachParseTree[1]
                
                location = interpretLocation(location)
            
            elif command == "move":
                print "move"
                entity   = eachParseTree[1]
                location = eachParseTree[2]
                
                entity   = interpretEntity(entity)
                location = interpretLocation(location)
        
            
    def interpretEntity(self, entity):
        print entity
        
    def interpretLocation(self, location):  
        print location  
 
    """ Quantifiers
       the
       a | an | any
       every
       all
       
       Relations
       beside
       leftOf
       rightOf
       above
       onTop
       under
       inside
    """