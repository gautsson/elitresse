import shrdlite
import interpret
import ambiguity

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
    utterance = getInput()
    parse_trees = shrdlite.parse(utterance)
    
    print parse_trees
    
    x = interpret.Interpreter()
    goals = x.interpret(parse_trees)
        
    for goal in goals:
        src, dst = goal
        object, relations = src
        
        parseRelation(relations)   