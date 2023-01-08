#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# This file contains a part of SceneGraphParser from demo.py.
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 08/22/2018
# Distributed under terms of the MIT license.
# https://github.com/vacancy/SceneGraphParser

import speech_recognition as sr

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

import sng_parser
import matplotlib.pyplot as plt
import networkx as nx

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
    return similarity_input

def spanList(scenegraph):
    entities_list = scenegraph["entities"]
    for entity in entities_list:
        print(entity["lemma_span"])

def scenegraphTable(sentence):
    # print('Sentence:', sentence)
    # Here we just use the default parser.
    parserOutput = sng_parser.parse(sentence)
    # sng_parser.tprint(parserOutput)
    print()

    return scenegraphGraph(parserOutput)
    # spanList(parserOutput)

    # print()

#Scene graph parsing completed here

#########################################################
from rdflib import Graph, URIRef, Literal, BNode, Namespace
import rdflib.plugins.sparql as sparql
from rdflib.namespace import FOAF, XMLNS, XSD, RDF, RDFS, OWL
import torch
import json, os, re
# import tensorflow as tf
from sentence_transformers import SentenceTransformer, util
print("Loading model")
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Loaded model")
g = Graph()
g.parse('Populated_Assets_KG.ttl', format = "ttl")
n = Namespace("http://www.semanticweb.org/szm/megascan-assets-ontology#")

#######################################################################
# util functions

def create_embedding_tensor(text):
  embedding_tensor = sentence_model.encode(text)
  print()
  return embedding_tensor

def str_to_tensor(string):
  str_list = string.split(',')

  float_list = [float(x) for x in str_list]
  tenser_res = torch.tensor(float_list)
  return tenser_res

def tensor_to_str(tensor):
  tensor_list = tensor.tolist()
  tensor_list_string = ""
  for l in tensor_list:
    tensor_list_string += str(l) + ','
  tensor_list_string = tensor_list_string[:-1]  # remove last ','
  return tensor_list_string

def find_similar_asset(input_string,KG_info):
    cosine_scores = []
    KG_tensor_dict = KG_info[0]
    KG_tensors_values = list(KG_tensor_dict.values())
    for val in KG_tensors_values:
        cosine_scores.append(util.cos_sim(input_string, val))

    # cosine_scores =  util.cos_sim(input_string, list(KG_tensor_dict.values()))
    #Find the pair with the highest cosine similarity score
    pair = []
    max_score = -1
    max_index = -1
    for i in range(len(cosine_scores)):
        if cosine_scores[i]>max_score:
            max_score = cosine_scores[i]
            max_index = i
            # print('new max score = ', max_score)

    closest_asset_ID = ""

    for id, tensor in KG_tensor_dict.items():
        # print(type(tensor), type(KG_tensors_values[max_index]))
        if torch.equal(tensor,KG_tensors_values[max_index]):
            print("found id: ", id)
            closest_asset_ID = id
            break
    print("Closest matching asst ID = ", closest_asset_ID)

    print("Matching ID info:\n")
    # print(KG_info[0][closest_asset_ID])
    # print(KG_info[1][closest_asset_ID])
    # print(KG_info[2][closest_asset_ID])

    return KG_info[0][closest_asset_ID], KG_info[1][closest_asset_ID], KG_info[2][closest_asset_ID]
    


    # return closest_asset_ID

    # closest_asset_ID_lit = Literal(closest_asset_ID, datatype=XSD.string)
# return asset path for closest_asset_ID found

# http://www.semanticweb.org/szm/megascan-assets-ontology#Asset_wdvlditia
    # q = sparql.prepareQuery(
    #     '''PREFIX mega:<http://www.semanticweb.org/szm/megascan-assets-ontology#>
    #         SELECT ?s ?assetID
    #         WHERE { ?s mega:assetID ?assetID.}
    # ''')

    
    # qres = graph.query(q, initBindings = {'p' : p, 'o' : o})
    # qres = g.query(
    # """
    #     PREFIX mega:<http://www.semanticweb.org/szm/megascan-assets-ontology#>
    #     SELECT ?s ?o1 ?o2
    #     WHERE
    #     {
    #         ?s mega:assetID ?o1
    #         ?s mega:assetName ?o2
    #     }
    # """, initBindings = {'o1': closest_asset_ID_lit})



#######################################################################
# form embeddings for entities mentioned in input

def scene_graph_tensors(sceneGraph_dict):
    # assume input of the sort:
    # The giraffe was grazing on a large isolated wasteland -> 
    # {'giraffe': ['The'], 'wasteland': ['a', 'large', 'isolated']}

    all_spawning_asset_desc = []
    for key,value in sceneGraph_dict.items():
        desc = ""
        for modifier in value:
            desc+= modifier + ' '
        all_spawning_asset_desc.append(key + desc)
    
    all_spawning_asset_tensor =[]   #list of all tensors for all nouns and their modifiers - later for matching with assets
    for str_desc in all_spawning_asset_desc:
        all_spawning_asset_tensor.append(create_embedding_tensor(str_desc))
    
    return all_spawning_asset_tensor

def get_KG_asset_tensors():
    # def get_asset_embeddings():
    # g = Graph()
    # g.parse('Populated_Assets_KG.ttl', format = "ttl")
    # n = Namespace("http://www.semanticweb.org/szm/megascan-assets-ontology#")
    qres = g.query(
    """
        PREFIX mega:<http://www.semanticweb.org/szm/megascan-assets-ontology#>
        SELECT ?s ?aID ?aName ?aTensor
        WHERE
        {
            {?s mega:assetTensor ?aTensor}
            UNION
            {?s mega:assetID ?aID}
            UNION
            {?s mega:assetName ?aName}
            
        }
    """)

    asset_Tensor_dict = {}
    asset_ID_dict = {}
    asset_Name_dict = {}
    count = 0
    for row in qres:
        try:
            asset_Tensor_dict[row.s.toPython()] = str_to_tensor(row.aTensor.toPython())
        except Exception as e:
            # print("No tensor found")
            count+=1
        try:
            asset_ID_dict[row.s.toPython()] = row.aID.toPython()
        except Exception as e:
            # print("No ID found")
            count+=1

        try:
            asset_Name_dict[row.s.toPython()] = row.aName.toPython()
        except Exception as e:
            # print("No name found")
            count+=1


    # sentences = []
    # for key,value in asset_ID_Tensor_dict.items():
    #     sentences.append(str_to_tensor(value))
    # print("Asset ID dict = ", asset_ID_dict)

    return asset_Tensor_dict, asset_ID_dict, asset_Name_dict

# print(get_KG_asset_tensors())

def write_to_file(chosen_asset):
    print("Chosen Asset ID: ", chosen_asset[1])
    print("Chosen Asset Name: ", chosen_asset[2], type(chosen_asset[2]))
    print("\n\n")
    line  = re.sub(" ", "_",chosen_asset[2])
    # print(line)
    #name_processed = re.sub("[^a-zA-Z0-9]", "_", data["id"])

    line+="_"+chosen_asset[1]
    
    # Append-adds at last
    # append mode
    fil = open("asset_info.txt", "a")
    fil.write(line)
    # writing newline character
    fil.write("\n\n\n")
    fil.close()    


def match_KG_input(KG_info, input_tensors):
# res_dict = scenegraphTable('A black woman standing next to a shiny red piano.')
# res_tensors = scene_graph_tensors(res_dict)
    for in_tensor in input_tensors:
        # for each input entity, find closest assetID and path+append to file: 'assetName_assetID'
        chosen_asset = find_similar_asset(in_tensor, KG_info)
        write_to_file(chosen_asset)
        
# KG_info = get_KG_asset_tensors()
# # KG_tensors = KG_info()[0]

# res_dict = scenegraphTable('A black woman standing next to a shiny red piano.')
# res_tensors = scene_graph_tensors(res_dict)

# input_tensors = match_KG_input(KG_info, res_tensors)

def main():
#     # scenegraphTable('A woman is playing the piano in the room.')
#     # scenegraphTable('A woman playing the piano in the room.')
#     # scenegraphTable('A piano is played by a woman in the room.')
#     # scenegraphTable('A woman is playing the space craft at NASA.')
#     # scenegraphTable('A woman is playing with a space craft at NASA.')
#     # scenegraphTable('A woman next to a piano.')
#     # scenegraphTable('A woman in front of a piano.')
#     res_dict = scenegraphTable('A black woman standing next to a shiny red piano.')
#     # scenegraphTable('The woman is a pianist.')
#     # scenegraphTable('A giraffe grazing a tree in the wildness with other wildlife.')
#     # scenegraphTable('Fat brown cow standing on sidewalk in city area near shops.')
#     # scenegraphTable('A black horse is wearing a green saddle. A small girl sits on the horse. The horse is standing on the green hill.')
#     # scenegraphTable("a small and thin girl")
#     res_tensors = scene_graph_tensors(res_dict)
#     print(res_tensors)

    sentence = r.recognize_google(audio)
    # sentence = 'There is a small gray rock and a big green leaf.'

    KG_info = get_KG_asset_tensors()
    # print('Input your own sentence. Type q to quit.')
    # while True:
    #     sentence = input('> ')
    #     if sent.strip() == 'q':
    #         break
    
        # KG_tensors = KG_info()[0]

        # res_dict = scenegraphTable('A black woman standing next to a shiny red piano.')
        # res_tensors = scene_graph_tensors(res_dict)

        # input_tensors = match_KG_input(KG_info, res_tensors)        
    fil = open("asset_info.txt", "w")
    fil.close()
    res_dict = scenegraphTable(sentence)
    res_tensors = scene_graph_tensors(res_dict)
    match_KG_input(KG_info, res_tensors)

    # start_time = time.time()
    # print("Total time taken = ", (time.time() - start_time), " seconds.")

if __name__ == '__main__':
    main()

