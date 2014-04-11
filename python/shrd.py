import shrdlite
import interpret
import ambiguity

def getInput():	
    input = raw_input("\nEnter a command for SHRDLITE:")
    return input.split()
    
if __name__ == '__main__':
    utterance = getInput()
    parse_trees = shrdlite.parse(utterance)
    print parse_trees
    
    x = interpret.Interpreter()
    
    goals = x.interpret(parse_trees)
    
    