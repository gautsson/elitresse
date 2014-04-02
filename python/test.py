import nltk
grammar = nltk.data.load("file:shrdlite_grammar.fcfg", cache=False)
parser = nltk.FeatureTopDownChartParser(grammar)
sentence = "put the white ball in a box on the floor".split()
for tree in parser.nbest_parse(sentence): 
    print tree.label()['sem']