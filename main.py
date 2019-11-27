#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:37:37 2019

@author: thibo
"""

import spacy
import get_relations
import primitives
import dottize_test
import det_rules

#=====================PREPARATION==============================================

nlp = spacy.load('fr_core_news_sm')

def spot_nouns(doc):
    return list(filter(lambda word: word.pos_ == "NOUN", doc))

def epicenize(word, base_noun):
    """
    Takes a word object from the doc returns its dottized epicene form
    """
    if word.pos_ == 'ADJ':
        #pdb.set_trace()
        return dottize_test.dottize_adjective(word, base_noun)
    elif word.pos_ == 'NOUN':
        #pdb.set_trace()
        return dottize_test.dottize_noun(word, base_noun)
    elif word.pos_ == 'DET':
        return det_rules.epicenize_det(word.text)
    elif word.pos_ == 'VERB':
        return dottize_test.dottize_verb(word, base_noun)
    else:
        return word.text

#=====================MAIN=====================================================

def main():
    doc = nlp("""les jardiniers qui ont été embauché sont très compétent.""")
    print(doc)
    nouns_index = list(map(lambda word: word.i, spot_nouns(doc)))

    lists_index_to_epicenize = list()
    for i in nouns_index:
        #pdb.set_trace()
        try:
            if primitives.is_human_from_noun(doc[i].lemma_):
                lists_index_to_epicenize.append([i])
        except:
            None
    #pdb.set_trace()
    for j in lists_index_to_epicenize:
        j += get_relations.get_index_of_all_related_element(doc, j[0])
    print('\nIndexes of words to epicenize: {}'.format(lists_index_to_epicenize))
    
    output_list = [word.text for word in doc]
    
    for u in range(len(doc)):
        for l in lists_index_to_epicenize:
            if u in l:
                print('currently processed: {}'.format(doc[u].text))
                output_list[u] = epicenize(doc[u], base_noun = doc[l[0]])
                break
    print('\n\n')
    print(' '.join(output_list))



if __name__ == '__main__':
    main()
