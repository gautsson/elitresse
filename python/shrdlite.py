#!/usr/bin/env python

# Test from the command line:
# python shrdlite.py < ../examples/medium.json

from __future__ import print_function

import sys
import json
import interpreting
import planning
import ambiguity


GRAMMAR_FILE = "shrdlite_grammar.fcfg"

# IMPORTANT NOTE:
# 
# If you are using NLTK 2.0b9 (which is the one that is installed 
# by the standard Ubuntu repository), then nltk.FeatureChartParser
# (in the parse function) fails to parse some sentences! In this 
# case you can use nltk.FeatureTopDownChartParser instead.
# You can check if it is working by calling this:
# 
#   python shrdlite.py < ../examples/small.json
# 
# The program should return "Ambiguity error!". If it instead
# returns "Parse error!", then the NLTK parser is not correct, 
# and you should change to nltk.FeatureTopDownChartParser instead.

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


def interpret(tree, world, holding, objects):
    
    return ["put,onTop,floor"]


def solve(goal, world, holding, objects):
    planner = planning.Planner(world, holding, objects)
    pickAndDrop = planner.startPlanning(goal)
    return pickAndDrop

def main(utterance, world, holding, objects, **_):
    result = {}
    result['utterance'] = utterance
    trees = parse(utterance)

    result['trees'] = [str(t) for t in trees]
    if not trees:
        result['output'] = "Parse error!"
        return result
    result['goals'] = goals = [goal for tree in trees
                               for goal in interpret(tree, world, holding, objects)]
    if not goals:
        result['output'] = "Interpretation error!"
        return result
    if len(goals) > 1:
        result['output'] = "Ambiguity error!"
        return result
    goal = goals[0]
    result['plan'] = plan = solve(goal, world, holding, objects)
    if not plan:
        result['output'] = "Planning error!"
        return result
    result['output'] = "Success!"
    return result


if __name__ == '__main__':
    #utterance1 = "put the large white ball in the red box"
    #utterance = utterance1.split()
    
    #goals1 = interpreter.interpret(tree)
    
    #world = [["e"],["g","l"],[],["k","m","f"],[]]
    #objects = {
    #"a": { "form":"brick",   "size":"large",  "color":"green" },
    #"b": { "form":"brick",   "size":"small",  "color":"white" },
    #"c": { "form":"plank",   "size":"large",  "color":"red"   },
    #"d": { "form":"plank",   "size":"small",  "color":"green" },
    #"e": { "form":"ball",    "size":"large",  "color":"white" },
    #"f": { "form":"ball",    "size":"small",  "color":"black" },
    #"g": { "form":"table",   "size":"large",  "color":"blue"  },
    #"h": { "form":"table",   "size":"small",  "color":"red"   },
    #"i": { "form":"pyramid", "size":"large",  "color":"yellow"},
    #"j": { "form":"pyramid", "size":"small",  "color":"red"   },
    #"k": { "form":"box",     "size":"large",  "color":"yellow"},
    #"l": { "form":"box",     "size":"large",  "color":"red"   },
    #"m": { "form":"box",     "size":"small",  "color":"blue"  }
    #}
    #holding = ""

    #)
    #result = (main(utterance, world, holding, objects))
    
    #print (result['trees'])

    #for tree in result ['trees']:
    #    print (type(tree))       
    #    print (tree)
    input = json.load(sys.stdin)
    output = main(**input)
    # json.dump(output, sys.stdout)
    # json.dump(output, sys.stdout, sort_keys=True, indent=4)
    print("{", ",\n  ".join('%s: %s' % (json.dumps(k), json.dumps(v))
                           for (k, v) in output.items()), "}")
