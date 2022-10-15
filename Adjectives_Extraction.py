'''

If adjective following article or number, it describes the next appearing noun/pronoun
e.g. That is a strong dog.



If adjective is following verb to be, it describes last appearing noun/pronoun. 
e.g. The dog is strong.

'''

import spacy
import numpy as np

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
        print(sen[i],sen[i].pos_)
        
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

    # print('lis_nouns = ', lis_nouns)            
    # print('lis_verbs_to_be = ', lis_verbs_to_be)
    
    #Github Desktop

    for noun in lis_nouns:
        intra_obj_relation[sen[noun]] = {'adj':[],'article':[]}
        

# Start adj from left to right
# Can have one or more than one adjectives per noun
    for adj_index in lis_adj:
        adj_list_adjuster_back = 0  # count of how many adjectives and/or conjunctions are between the noun and the current adjective
        adj_list_adjuster_for = 0 # count of how adjectives between curr adj and next coming noun

        while adj_index-1-adj_list_adjuster_back in lis_adj or adj_index-1-adj_list_adjuster_back in lis_con:
            adj_list_adjuster_back += 1

        while adj_index+1+adj_list_adjuster_for in lis_adj or adj_index+1+adj_list_adjuster_for in lis_con:
            adj_list_adjuster_for += 1

#           If adjective following article or number, it describes the next appearing noun/pronoun e.g.I saw a big red dog.            
        if (adj_index - 1 - adj_list_adjuster_back) in lis_articles:
            dummy = np.array(lis_nouns)     #[0,5]  -> Indices of the nouns that follow the adjective
            noun = sen[min(dummy[dummy > adj_index])]  # Index of first noun after adj
            
          #[dummy > adj_index] = [False, True]
            # dummy[dummy > adj_index] = 5 -> array that slices off False instances
            # immediately following noun -> the first noun, hence min()
            
            intra_obj_relation[noun]['adj'].append(sen[adj_index])
            intra_obj_relation[noun]['article'].append(sen[adj_index - 1 - adj_list_adjuster_back])            

        elif (adj_index - 1 - adj_list_adjuster_back) in lis_verbs_to_be:
            dummy = np.array(lis_nouns)
            noun = sen[max(dummy[dummy < adj_index])]
            # [dummy < adj_index] => boolean list for all nouns that some before the first appearing adjective
            intra_obj_relation[noun]['adj'].append(sen[adj_index])
            intra_obj_relation[noun]['article'].append(sen[adj_index - 1 - adj_list_adjuster_back])    
            
        elif (adj_index + 1 + adj_list_adjuster_for) in lis_nouns:
            noun = sen[adj_index+1+adj_list_adjuster_for]  # first noun after adj
            intra_obj_relation[noun]['adj'].append(sen[adj_index])

    return intra_obj_relation



text = input('Input query here :')

print(set_pos(text))
