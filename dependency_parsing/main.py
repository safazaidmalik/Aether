from nltk.parse.stanford import StanfordDependencyParser
import networkx as nx
import matplotlib.pyplot as plt
import spacy
import numpy as np
import speech_recognition as sr

# flag = 1
#
# while (flag):
#
#     r = sr.Recognizer()
#
#     with sr.Microphone() as source:
#         r.adjust_for_ambient_noise(source)
#
#         print("Please say something")
#
#         audio = r.listen(source)
#
#         print("Recognizing Now .... ")
#
#         # recognize speech using google
#
#         try:
#             print("\nYou have said: \n" + r.recognize_google(audio) + "\n")
#             user_input = input("Press\n- 0, if this is incorrect:\n- any key, if this is correct ")
#             if int(user_input) == 0:
#                 flag = 1
#             else:
#                 flag = 0
#
#         except Exception as e:
#             print("Error :  " + str(e))
#
#     # write audio
#     with open("recorded.wav", "wb") as f:
#         f.write(audio.get_wav_data())

N_id = 1


class Node:
    node_id = -1
    noun_labels = []
    adj_list = []

    def __init__(self, N_id):
        self.node_id = N_id
        N_id += 1

    # def addNounLabel()


jar_path = 'stanford-corenlp-4.5.1/stanford-corenlp-4.5.1.jar'
models_jar_path = 'stanford-corenlp-4.5.1/stanford-corenlp-4.5.1-models.jar'
# sentence = "The horse wears a saddle. Two girls own the saddle. They wear brown dresses."
# without coreference resolution - 'A girl' and 'Another girl' are shown as the same entity


verbs_to_be = ['are', 'am', 'is', 'was', 'were', 'been', 'being']


def set_pos(chunk):
    intra_obj_relation = {}
    sp = spacy.load('en_core_web_sm')
    sen = sp(chunk)
    adj_pos = -1
    article_pos = -1
    obj_pos = -1
    verb_to_be_pos = -1
    article = ''
    adj = ''
    obj = ''
    verb_to_be = ''

    lis_nouns = []
    lis_propn = []
    lis_articles = []
    lis_verbs = []
    lis_adj = []
    lis_prep = []
    lis_adv = []
    lis_con = []
    lis_verbs_to_be = []

    print(sen.text)
    for i in range(len(sen)):
        print(sen[i], sen[i].pos_)

        if sen[i].pos_ == 'DET' or sen[i].pos_ == 'NUM':  # DET: determiner (for article) or num
            lis_articles.append(i)

        # if article position (art_pos) is smaller than adjective pos (adj_pos), it is related to noun/pronoun that has noun_pos > adj_pos
        # assume only one adjective per chunk (one attibute for one object)
        elif sen[i].pos_ == 'ADJ':
            lis_adj.append(i)
        elif sen[i].pos_ == 'NOUN' or sen[i].pos_ == 'PRON':
            lis_nouns.append(i)
        elif sen[i].pos_ == 'PROPN':
            lis_propn.append(i)
        elif sen[i].pos_ == 'AUX':
            lis_verbs_to_be.append(i)
        elif sen[i].pos_ == 'CCONJ':
            lis_con.append(i)

    for noun in lis_nouns:
        intra_obj_relation[sen[noun]] = {'adj': [], 'article': []}

    # Start adj from left to right
    # Can have one or more than one adjectives per noun
    for adj_index in lis_adj:
        # if (adj_index - 1 - adj_list_adjuster_back) in lis_adj or (adj_index - 1 - adj_list_adjuster_back) in lis_con:
        #     adj_list_adjuster_back += 1
        # else:
        #     adj_list_adjuster_back = 0
        adj_list_adjuster_back = 0  # count of how many adjectives and/or conjunctions are between the noun and the current adjective
        adj_list_adjuster_for = 0  # count of how adjectives between curr adj and next coming noun

        while adj_index - 1 - adj_list_adjuster_back in lis_adj or adj_index - 1 - adj_list_adjuster_back in lis_con:
            adj_list_adjuster_back += 1
        # if adj_index-1-adj_list_adjuster_back not in lis_:
        #     adj_list_adjuster_for = 0

        while adj_index + 1 + adj_list_adjuster_for in lis_adj or adj_index + 1 + adj_list_adjuster_for in lis_con:
            adj_list_adjuster_for += 1
        # if adj_index+1+adj_list_adjuster_for not in lis_nouns:
        #     adj_list_adjuster_for = 0

        # print(adj_list_adjuster_back)

        if (adj_index - 1 - adj_list_adjuster_back) in lis_articles:
            print('If 1')
            dummy = np.array(lis_nouns)
            # e.g. I saw a big red dog.
            # [0,5]

            # Indices of the nouns that follow the adjective
            noun = sen[min(dummy[dummy > adj_index])]  # first noun after adj
            # [dummy > adj_index] = [False, True]
            # dummy[dummy > adj_index] = 5 -> array that slices off False instances
            # immediately following noun -> the first noun, hence min()
            # actual word -> sen[everything]
            intra_obj_relation[noun]['adj'].append(sen[adj_index])
            intra_obj_relation[noun]['article'].append(sen[adj_index - 1 - adj_list_adjuster_back])

        elif (adj_index - 1 - adj_list_adjuster_back) in lis_verbs_to_be:
            print('If 2')
            dummy = np.array(lis_nouns)
            noun = sen[max(dummy[dummy < adj_index])]
            # [dummy < adj_index] => boolean list for all nouns that some before the first appearing adjective
            intra_obj_relation[noun]['adj'].append(sen[adj_index])
            intra_obj_relation[noun]['article'].append(sen[adj_index - 1 - adj_list_adjuster_back])

        elif (adj_index + 1 + adj_list_adjuster_for) in lis_nouns:
            print('If 3')
            noun = sen[adj_index + 1 + adj_list_adjuster_for]  # first noun after adj
            intra_obj_relation[noun]['adj'].append(sen[adj_index])

        # if adj immediately following
        # blu birds -> blue must describe the birds, just before

    return intra_obj_relation


def dependecyParsing(sentence):
    noun_adj_dict = set_pos(sentence)
    print("Identified Nouns with adjectives:\n", noun_adj_dict)

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
                                  'nummod:gov'],
                      'object': ['obj', 'obl', 'iobj', 'dobj', 'obl:agent', 'obl:arg', 'obl:lmod', 'obl:tmod']}
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
    pos_higher = {}
    plt.figure(figsize=(8, 8))

    for rel in relations:
        for edges in triples[rel]:
            nx.draw_networkx_edge_labels(G, pos, edge_labels={edges: rel})

    for k, v in pos.items():
        if (v[1] > 0):
            pos_higher[k] = (v[0], v[1] + 0.15)
        else:
            pos_higher[k] = (v[0], v[1] - 0.15)

    nx.draw_networkx(G, pos, with_labels=True, font_size=9, node_size=1000)
    nx.draw_networkx_labels(G, pos_higher, font_color="maroon", font_size=8, font_family="Arial")

    plt.margins(0.25)
    plt.show()

sentence = "The black horse wears a green saddle. A girl owns the saddle and has green eyes "
print("Input sentence = ", sentence)
dependecyParsing(sentence)

