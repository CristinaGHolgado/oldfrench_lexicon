# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 18:47:11 2022

@author: Cristina GH
"""

import pandas as pd
import csv
import enchant
from datetime import datetime


"""
Quick script to calculate Levenshtein distance among a list of lemmas to match potential variants
"""

    
def levenshtein_dist(li, approx_dist):
    '''
    Calculate Levenshtein distance from couples of lemme + pos    

    Parameters
    ----------
    lem_pos : list
        list of lemmas and joined POS
    distance : int
        Edit distance
        
    Returns
    -------
    DataFrame

    '''
    import itertools
    
    lemma_dic = {}

    for a, b in itertools.combinations(li, 2):
        for first in a:
            for second in b:
                # si tokenA has N distance to tokenB and lenght of both words are > 3, append to lemma dic
                if enchant.utils.levenshtein(first, second) == approx_dist and len(first.split('_')[0]) > 3 and len(second.split('_')[0]) > 3:
                    add_lemmas = {first: second}
                    lemma_dic.update(add_lemmas)

    return lemma_dic


def remove_inverted_dupl(li):
    ''' Remove duplicates from comparison, keep first.
    e.g.
        tokenA isclose to tokenB
        tokenB isclose to tokenA
    '''
    reverse = []
    
    for y, z in list(li.items())[:1]:
        reverse.append(str(y + '@' + z))
    
    for y, z in li.items():
        if str(z + '@' + y) not in reverse:
            reverse.append(str(y + '@' + z))
    
    return set(reverse)


def calc_distance_format(folder, file, cols=[]):
    
    lem = cols[0]
    pos = cols[1]
    
    df = pd.read_csv(str(folder + file), encoding='utf-8', sep='\t', quoting=csv.QUOTE_NONE)
    
    liste_lemmes = df[lem] + '_' + df[pos] # liste avec lemme+pos pour trouver des variants possibles de lemmes
    liste_lemmes = liste_lemmes.to_list()
    lists = [liste_lemmes, liste_lemmes]


    liste_lemmes = levenshtein_dist(lists, 1)  # calc lev distance
    liste_lemmes_simplifie = remove_inverted_dupl(liste_lemmes) # remove duplicates from output list

    # pass to df and format table
    varlem = pd.DataFrame(liste_lemmes_simplifie, columns=['lemme']).drop_duplicates(keep='first')
    varlem['prox_lemme'] = varlem['lemme'].apply(lambda x: x.split('@')[1:])
    varlem['lemme'] = varlem['lemme'].apply(lambda x: x.split('@')[0])
    varlem = varlem.sort_values(by=['lemme'])
    varlem['var?'] = ''

    varlem.to_csv(str(folder + f'{str(datetime.now().strftime("%d%m%Y%H%M%S"))}_{file}_var.tsv'), sep='\t', encoding='utf-8', index=False)


folder = 'scripts\\normalisation_relematisation_manques\\files\\updated_manques\\'
file = 'v2_conj_manques_annote.tsv'

vars_possibles = calc_distance_format(folder, file, cols=['lemma_def','pos'])
