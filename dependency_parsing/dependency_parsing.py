from nltk.parse.stanford import StanfordDependencyParser

# Your path to CoreNLP jar
jar_path = '/home/szm/Downloads/stanford-corenlp-4.5.1/stanford-corenlp-4.5.1.jar'

# Path to CoreNLP model jar
models_jar_path = '/home/szm/Downloads/stanford-corenlp-4.5.1/stanford-corenlp-4.5.1-models.jar'

# sentence = 'Deemed universities charge huge fees'
sentence = "The tree has yellow and green leaves."

# Initialize StanfordDependency Parser from the path
parser = StanfordDependencyParser(path_to_jar = jar_path, path_to_models_jar = models_jar_path)

# Parse the sentence
result = parser.raw_parse(sentence)
dependency = result.__next__()


print ("{:<15} | {:<10} | {:<10} | {:<15} | {:<10}".format('Head', 'Head POS','Relation','Dependent', 'Dependent POS'))
print ("-" * 75)
  
# Use dependency.triples() to extract the dependency triples in the form
# ((head word, head POS), relation, (dependent word, dependent POS))  
for dep in list(dependency.triples()):
  print ("{:<15} | {:<10} | {:<10} | {:<15} | {:<10}"
         .format(str(dep[0][0]),str(dep[0][1]), str(dep[1]), str(dep[2][0]),str(dep[2][1])))

# dependency.nx_graph()         
import networkx as nx
import matplotlib.pyplot as plt
# Using reverse() to reverse the direction of edges as nx_graph() returns inverted edges
G = dependency.nx_graph().reverse()
print(G)
# nx_graph() returns numeric node labels starting from 1
# Create a dictionary to map numeric nodes and words in the sentence
words = sentence.split(" ")
labels = {index + 1: words[index] for index in range(len(words))}
print("Going to draw G")
nx.draw(G, with_labels=True, labels=labels, node_size=2500, node_color='#B5EAD7', font_size=10)
# nx.draw(G)
plt.show()