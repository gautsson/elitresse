import interpreting
import ambiguity
import planning
from copy import deepcopy
import json

GRAMMAR_FILE = "shrdlite_grammar.fcfg"

def get_tree_label(result):
    """Returns the label of a NLTK Tree"""
    try:
        # First we try with NLTKv3, the .label() method:
        return result.label()
    except AttributeError, TypeError:
        # If that doesn't work we try with NLTKv2, the .node attribute:
        return result.node

def get_all_parses(parser, utterance):
    """Returns a sequence of all parse trees of an utterance"""
    try:
        # First we try with NLTKv2, the .nbest_parse() method:
        return parser.nbest_parse(utterance)
    except AttributeError, TypeError:
        try:
            # Then we try with NLTKv3, the .parse_all() method:
            return parser.parse_all(utterance)
        except AttributeError, TypeError:
            # Finally we try with NLTKv3, the .parse() method:
            return parser.parse(utterance)

def parse(utterance):
    import nltk
    grammar = nltk.data.load("file:" + GRAMMAR_FILE, cache=False)
    parser = nltk.FeatureChartParser(grammar)
    try:
        return [get_tree_label(result)['sem'] 
                for result in get_all_parses(parser, utterance)]
    except ValueError:
        return []

def getStartingState():
    while True:
        worldSize = raw_input ('Enter the size of the world (small/medium/complex/impossible): ')

        if worldSize    == "small":
            return json.load(open('../examples/small.json'))
        elif worldSize  == "medium":
            return json.load(open('../examples/medium.json'))
        elif worldSize  == "complex":
            return json.load(open('../examples/complex.json'))
        elif worldSize  == "impossible":
            return json.load(open('../examples/impossible.json'))
        else:
            print "Not a valid world size\n"

def getUtterance(examples):
    utterance = raw_input ('\nEnter a command to Shrdlite: ')       
    return utterance.split()

def interpret(trees, world, objects):
    interpreter = interpreting.Interpreter()
    ambiguityResolver = ambiguity.AmbiguityResolver(world, objects)
    
    preGoal = interpreter.interpret(trees)

    goal = ambiguityResolver.handleInput(preGoal)
    
    return goal

def solve(goal, world, holding, objects):
    planner = planning.Planner(world, holding, objects)
    pickAndDrop = planner.startPlanning(goal)

    return pickAndDrop

def doPlan(world, holding, plan):
    for action in plan:
        splitAction = action.split()
        
        if splitAction[0] == "pick":
            holding = world[int(splitAction[1])].pop()
        elif splitAction[0] == "drop":
            world[int(splitAction[1])].append(holding)
            holding = None

    return holding

def main():
    print "Welcome to Shrdlite!\n"

    startingState = getStartingState()
    world    = startingState['world']
    objects  = startingState['objects']
    examples = startingState['examples']
    holding  = startingState['holding']
   
    while True:
        print "\nCURRENT WORLD STATE"
        print world
        print "Currently holding: " + str(holding) + "\n"
        
        utterance = getUtterance(examples)

        parseTrees = parse(utterance)
        if not parseTrees:
            print "Parse error!"
            continue
        
        goals = interpret(parseTrees, world, objects)
        if not goals:
            print "Interpretation error!"
            continue

        goal = goals[0]

        worldCopy = deepcopy(world)
        plan = solve(goal, worldCopy, holding, objects)
        if not plan:
            print "Planning error!"
            continue
        
        print "Plan: " str(plan)

        holding = doPlan(world, holding, plan)

if __name__ == '__main__':    
    main()
