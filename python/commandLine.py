import interpreting
import ambiguity
import planning
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

def determineState():
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

def getUtterance(examples):
    utterance = raw_input ('Enter a command to Shrdlite: ')       
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
    holding = ""
    for action in plan:
        splitAction = action.split()
        
        if splitAction[0] == "pick":
            holding = world[int(splitAction[1])].pop()
        elif splitAction[0] == "drop":
            world[int(splitAction[1])].append(holding)
            holding = ""

    return holding

def main():
    state   = determineState()
    world   = state['world']
    objects = state['objects']
    examples = state['examples']
    holding = state['holding']

    while True:
        print "Current world state"
        print world
        
        utterance = getUtterance(examples)
        print utterance
        parseTrees = parse(utterance)
        print parseTrees

        #goal = interpret(parseTrees, world, objects)
        #print goal
        
        goals = interpret(parseTrees, world, objects)
        goal = goals[0]
        
        #goal = 'put,onTop,k'

        plan = solve(goal, world, holding, objects)
        print "Plan"
        print plan
        holding = doPlan(world, holding, plan)
        print "Holding: " + holding + "\n\n"

if __name__ == '__main__':    
    main()


