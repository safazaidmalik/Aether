from nltk.parse.stanford import StanfordDependencyParser
import networkx as nx
import matplotlib.pyplot as plt
import spacy
import numpy as np
import speech_recognition as sr
import sng_parser
import matplotlib.pyplot as plt
import networkx as nx
import time

flag = 1

while (flag):

    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print("Please say something")

        audio = r.listen(source)

        print("Recognizing Now .... ")

       # recognize speech using google

        try:
            print("\nYou have said: \n" + r.recognize_google(audio) + "\n")
            user_input = input("Press\n- 0, if this is incorrect:\n- 1, if this is correct ")
            if int(user_input) == 0:
                flag = 1
            elif int(user_input) == 1:
                    flag = 0

        except Exception as e:
            print("Error :  " + str(e))

    # write audio
    with open("recorded.wav", "wb") as f:
        f.write(audio.get_wav_data())

N_id = 1


jar_path = 'stanford-corenlp-4.5.1/stanford-corenlp-4.5.1.jar'
models_jar_path = 'stanford-corenlp-4.5.1/stanford-corenlp-4.5.1-models.jar'

#head
#modifiers
#relations

def scenegraphGraph(scenegraph):
    G = nx.DiGraph()
    objects = []
    similarity_input = {}

    # HEAD
    entities_list = scenegraph["entities"]
    for entity in entities_list:
        # print(entity["head"])
        val = entity["head"]
        similarity_input[val] = []
        objects.append(val)
        G.add_node(val)
    # print()

    # MODIFIERS
    for entity in entities_list:
        for modifier_dict in entity["modifiers"]:
            modifier = modifier_dict.get("span")
            G.add_node(modifier)
            object = entity["head"]
            G.add_edge(object, modifier)
            # if 'a' not in modifier and 'A' not in modifier and 'the' not in modifier and 'The' not in modifier:
            similarity_input[object].append(modifier)
            # print(modifier_dict.get("span"))
    # print()

    # RELATIONS
    relations_list = scenegraph["relations"]

    for relation in relations_list:
        G.add_edge(objects[relation.get("subject")], objects[relation.get("object")], label=relation.get("relation"))

    # print(relations_list)
    # print()

    pos = nx.spring_layout(G)
    node_size = 800
    nx.draw(G, with_labels=True, node_size=node_size)
    edge_labels = nx.get_edge_attributes(G, "label")
    label_pos = 0.5
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=label_pos)

    plt.show()

    print(similarity_input) # the output

def spanList(scenegraph):
    entities_list = scenegraph["entities"]
    for entity in entities_list:
        print(entity["lemma_span"])

def scenegraphTable(sentence):
    # print('Sentence:', sentence)
    # Here we just use the default parser.
    parserOutput = sng_parser.parse(sentence)
    # sng_parser.tprint(parserOutput)
    scenegraphGraph(parserOutput)
    # spanList(parserOutput)

    print()

# sentence = r.recognize_google(audio)

# scenegraphTable('A woman is playing the piano in the room.')
# scenegraphTable('A woman playing the piano in the room.')
# scenegraphTable('A piano is played by a woman in the room.')
# scenegraphTable('A woman is playing the space craft at NASA.')
# scenegraphTable('A woman is playing with a space craft at NASA.')
# scenegraphTable('A woman next to a piano.')
# scenegraphTable('A woman in front of a piano.')
sentence = 'A black woman standing next to a shiny red piano.'
# scenegraphTable('The woman is a pianist.')
# scenegraphTable('A giraffe grazing a tree in the wildness with other wildlife.')
# scenegraphTable('Fat brown cow standing on sidewalk in city area near shops.')
# scenegraphTable('A black horse is wearing a green saddle. A small girl sits on the horse. The horse is standing on the green hill.')
# scenegraphTable("a small and thin girl")

start_time = time.time()
scenegraphTable(sentence)
print("Total time taken = ", (time.time() - start_time), " seconds.")

