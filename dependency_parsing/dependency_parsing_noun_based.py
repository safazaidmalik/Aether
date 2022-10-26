from nltk.parse.stanford import StanfordDependencyParser
import networkx as nx
import matplotlib.pyplot as plt

# Change paths according to your own paths
jar_path = '/home/szm/Downloads/stanford-corenlp-4.5.1/stanford-corenlp-4.5.1.jar'
models_jar_path = '/home/szm/Downloads/stanford-corenlp-4.5.1/stanford-corenlp-4.5.1-models.jar'
sentence = "The girl has brown eyes and red hair."

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
counter = 1
nodes_list = []
relation_text = []
for dep in list(dependency.triples()):
    if dep[0][1] == 'VBZ':
        # store label verb in labels_list
        relation_text.append(dep[0][0])

# match dep[0][0] with labels_list
node_1 = ''
node_2 = ''
sbj_found = 0
obj_found = 0

nouns_list = ['NN', 'NNS', 'NNP', 'NNPS']

for dep in list(dependency.triples()):
    if dep[0][1] == 'VBZ' and dep[0][0] in relation_text:
        print("Dependent word with Common Head of ",
              dep[0][0], " is ", dep[2][0])
        if dep[2][1] in nouns_list:
            print("Dependent of common Head 'has' = ", dep[2][0])
            if dep[1] == 'nsubj':
                sbj_found = 1
                node_1 = dep[2][0]
                # print("Found subject!")
            elif dep[1] == 'obj':
                obj_found = 1
                node_2 = dep[2][0]
                # print("Found object!")

nodes = [node_1, node_2]
labels = {(node_1, node_2): relation_text[0]}
print("Labels = ", labels)
G.add_edge(node_1, node_2, label=relation_text[0])
pos = nx.spring_layout(G)
plt.figure()

nx.draw(G, pos, with_labels=True, node_size=2500,
        node_color='#B5EAD7', font_size=10)

plt.show()
