#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : demo.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 08/22/2018
#
# This file is part of SceneGraphParser.
# Distributed under terms of the MIT license.
# https://github.com/vacancy/SceneGraphParser

"""
A small demo for the scene graph parser.
"""

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


def main():
    # scenegraphTable('A woman is playing the piano in the room.')
    # scenegraphTable('A woman playing the piano in the room.')
    # scenegraphTable('A piano is played by a woman in the room.')
    # scenegraphTable('A woman is playing the space craft at NASA.')
    # scenegraphTable('A woman is playing with a space craft at NASA.')
    # scenegraphTable('A woman next to a piano.')
    # scenegraphTable('A woman in front of a piano.')
    scenegraphTable('A black woman standing next to a shiny red piano.')
    # scenegraphTable('The woman is a pianist.')
    # scenegraphTable('A giraffe grazing a tree in the wildness with other wildlife.')
    # scenegraphTable('Fat brown cow standing on sidewalk in city area near shops.')
    # scenegraphTable('A black horse is wearing a green saddle. A small girl sits on the horse. The horse is standing on the green hill.')
    # scenegraphTable("a small and thin girl")

    print('Input your own sentence. Type q to quit.')
    while True:
        sent = input('> ')
        if sent.strip() == 'q':
            break
        scenegraphTable(sent)


if __name__ == '__main__':
    main()

