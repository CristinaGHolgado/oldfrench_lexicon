# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 16:44:34 2022

@author: Cristina GH

detect potential prefixes in ofrelex and annotated missing forms

How it works
------------
list of missing forms are compared to entries in ofrlex to see if forme1 in ofrlex is in missing form,
as words are composes by a root to which preffixes are attaches
"""
folder = "enrich_ofrlexdev\\data\\source_data\\"
manques_f = folder + "manques11nov.txt"
ofrlex = folder + "inventaire_ofrlex.tsv"
prefixes = folder + "prefixes.txt"

import pandas as pd
import csv
import re
import numpy as np
import nltk
from nltk import word_tokenize
from nltk.stem import SnowballStemmer



manques_df = pd.read_csv(manques_f, sep='\t', encoding='utf-8', names=['forms'], quoting=csv.QUOTE_NONE)
manques_li = manques_df['forms'].to_list()

ofr_df =  pd.read_csv(ofrlex, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE)
ofr_li = ofr_df['form'].astype(str).to_list()
manques_li = ofr_df['form'].drop_duplicates().to_list()


pre_df = pd.read_csv(prefixes, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE)
prefs_li = pre_df['prefixes'].to_list()




def split_prefixs():
    ''' Identification simple de prefixes:
        A partir d'une liste de prefixes, recherche dans les manques les formes commençant
        par prefixe et dont la base (root >2 chars min) existe dans le lexique. 
        + pass POS
    '''
    # dict to append candidates (prefixed forms)
    possible_prefs = {'prefixe':[], 'word':[], 'root': []}
    
    ignore_prefs = ['a-']
    
    ## In ofrlex, pick categories that can be/contain a prefix (ddv, adj, ver, nouns)
    ## ignore lemmas len <2
    cats = 'adj', 'v', 'verb', 'adv', 'nc', 'aux'
    ofr_items = ofr_df[ofr_df['pos'].apply(lambda x: x in cats)]
    ofr_items = ofr_items[ofr_items['raw_lemme'].str.len() > 2]
    
    for pref in prefs_li: # for each prefix in prefix list
        if pref not in ignore_prefs:
            pref = pref[:-1]    # if prefix without last char '-'
            for w in manques_li[:50]: # if word in missing words starts with prefix
                if w.startswith(pref):  
                    root = w[len(pref):]    # extract root based on prefix length
                    if len(root) > 2:   # append root if len > 2, else ignore
                        possible_prefs['prefixe'].append(pref)
                        possible_prefs['word'].append(w)
                        possible_prefs['root'].append(root)
                
    df = pd.DataFrame(possible_prefs) # pass dict to df
    


        # check if exctracted roots exist in ofrlex forms and pass its lemma
    ofr = ofr_items[['form', 'pos', 'lemme']].dropna()
    ofr_form_pos_lemme = ofr['form'] + '@' + ofr['pos'] + '@' + ofr['lemme']

    for item in ofr_form_pos_lemme.drop_duplicates():
          # if root = ofrlex forms, pass ofr form, them its lemma and pos
          item = str(item)
          ofr_form = item.split('@')[0]
          ofr_pos = item.split('@')[1]
          ofr_lemma = item.split('@')[-1]
          df.loc[df.root == ofr_form, ['ofr_root_form',
                                       'ofr_root_lemma',
                                       'ofr_root_pos']] = [ofr_form, ofr_lemma, ofr_pos]
    

    df = df.fillna('').drop_duplicates()
    # df = df.groupby(['prefixe', 'word', 'ofr_root_lemma', 'ofr_root_pos']).size()
    df.to_csv('prefixes_stemmer1_ofrlex.csv', sep='\t', encoding='utf-8')
    
    return df
    

find_prefixes = split_prefixs()




def process_missingWords_prefixes():
    prefixes_found = 'prefixes_stemmer1.csv'
    annotated_missingWords = 'enrich_ofrlexdev\\data\\scripts_data\\annotated_missing_forms_manques.tsv'
    
    prefixated_words = pd.read_csv(prefixes_found, sep='\t')
    prefixated_words = prefixated_words[~prefixated_words.ofr_root_lemma.isna()]
    
    annotated_words = pd.read_csv(annotated_missingWords, sep='\t')
    annotated_words['pos_def'] = annotated_words['pos_def'].str.replace('ADJ','adj').replace('Nco','nc').replace('VER','v').replace('ADV', 'adv')
    annotated_words['word'], annotated_words['ofr_root_pos'] = annotated_words['form'], annotated_words['pos_def']
    
    merged_form_upos = prefixated_words.merge(annotated_words, on=['ofr_root_pos', 'word'], how='left')
    merged_form_upos = merged_form_upos.fillna('_')
    merged_form_upos = merged_form_upos.iloc[: , 1:]
    
    del merged_form_upos['form']
    del merged_form_upos['pos_def']
    del merged_form_upos['pos_list']
    
    print(merged_form_upos.groupby('prefixe')['prefixe'].count().sort_values(ascending=False))
    
    merged_form_upos.to_csv('prefixes_stemmer1_clean.csv', sep='\t', encoding='utf-8')

    return merged_form_upos

# processed_found_prefixes = process_missingWords_prefixes()


