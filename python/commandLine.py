import shrdlite
import interpret
import ambiguity
import planning

def getInput():
    input = raw_input ('Enter a command to Shrdlite: ')
    return input.split()

def parseRelation(relations):
    if (len(relations) == 1):
        relations = relations.pop()        
    
    relation, rest = relations

    print relation
    print rest
    
    if (len(rest) > 1):
        parseRelation(rest)

    
if __name__ == '__main__':
    world = [["e"],["g","l"],[],["k","m","f"],[]]
    worldSize = "small"

    utterance = getInput()
    parse_trees = shrdlite.parse(utterance)
    
    interpreter = interpret.Interpreter()
    goals = x.interpret(parse_trees)
    
    ambiguityResolver = AmbiguityResolver(worldSize)

    x = Interpreter()
    print x.printOut()
    
    
    #planner = Planner()
    
    #utterance = (raw_input ('Enter a command to Shrdlite: ')).split()
    #trees = self.parse(utterance) 
    
    #print trees
    #print interpreter.interpret(trees)
        
    #for goal in goals:
    #    src, dst = goal
    #    object, relations = src
        
    #    parseRelation(relations)   
