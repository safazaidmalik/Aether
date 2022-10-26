from nltk.parse.stanford import StanfordDependencyParser
import networkx as nx
import matplotlib.pyplot as plt

# Add your own paths here
jar_path = '/home/szm/Downloads/stanford-corenlp-4.5.1/stanford-corenlp-4.5.1.jar'
models_jar_path = '/home/szm/Downloads/stanford-corenlp-4.5.1/stanford-corenlp-4.5.1-models.jar'
# sentence = "The horse wears a saddle. Two girls own the saddle. They wear brown dresses."
# without coreference resolution - 'A girl' and 'Another girl' are shown as the same entity


sentence = "The horse wears a saddle. A girl owns the saddle. The girl wears a brown dress."
print("Input sentence = ", sentence)

# intitialize parser
parser = StanfordDependencyParser(
    path_to_jar=jar_path, path_to_models_jar=models_jar_path)

# Parse the sentence
result = parser.raw_parse(sentence)
dependency = result.__next__()
print("{:<15} | {:<10} | {:<10} | {:<15} | {:<10}".format(
    'Head', 'Head POS', 'Relation', 'Dependent', 'Dependent POS'))
print("-" * 75)
for dep in list(dependency.triples()):
    print("{:<15} | {:<10} | {:<10} | {:<15} | {:<10}"
          .format(str(dep[0][0]), str(dep[0][1]), str(dep[1]), str(dep[2][0]), str(dep[2][1])))

count = 0

# 'Head'      'Head POS'   'Relation'   'Dependent'    'Dependent POS'
# dep[0][0]    dep[0][1]    dep[1]       dep[2][0]      dep[2][1]

G = nx.MultiDiGraph()
# Traverse dep in dependency.triples. If both dep[0][1] == 'VBZ' and are equal,
#  ie dep[1][0]=='NN' or 'NNS' (entity), and one of them is a subject (ie dep[1] == 'nsubj')
#  while the other is an object (ie dep[1] == 'obj'),
#  add nodes to the graph and connect them with label = dep[0][0]
nouns_list = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$']
verbs_list = ['VB', 'VBG', 'VBN', 'VBP', 'VBZ', 'VBD']
relations_list = {'subject': ['nsubj', 'det:poss', 'nmod', 'nmod:poss', 'nmod:tmod', 'nsubj:move', 'nummod',
                              'nummod:gov'], 'object': ['obj', 'obl', 'iobj', 'dobj', 'obl:agent', 'obl:arg', 'obl:lmod', 'obl:tmod']}
triples = {}
relations = []
for dep in list(dependency.triples()):
    if dep[0][1] in verbs_list:
        relations.append(dep[0][0])

for rel in relations:
    # append relevant subject,object tuples to triples[rel] later
    triples[rel] = []
relations = list(set(triples))
print("Relations = ", relations)
tmp_sbj = ''
sbj_found = 0
obj_found = 0
tmp_obj = ''
for dep in list(dependency.triples()):
    if dep[0][1] in verbs_list:
        if dep[0][0] in relations:
            if dep[2][1] in nouns_list:
                if dep[1] in relations_list['subject']:
                    tmp_sbj = dep[2][0]
                    sbj_found = 1
                elif dep[1] in relations_list['object']:
                    tmp_obj = dep[2][0]
                    obj_found = 1
                    # sbj_found = 0
    if sbj_found == 1 and obj_found == 1:
        triples[dep[0][0]].append((tmp_sbj, tmp_obj))
        sbj_found = 0
        obj_found = 0
print(triples)

for rel in relations:
    for edges in triples[rel]:
        print("edges = ", edges)
        G.add_edge(edges[0], edges[1], label=rel)
        print("Added to graph: ", edges[0], edges[1], rel)
pos = nx.spring_layout(G)
plt.figure()

nx.draw(G, pos, with_labels=True, node_size=2500,
        node_color='#B5EAD7', font_size=5)
plt.show()
