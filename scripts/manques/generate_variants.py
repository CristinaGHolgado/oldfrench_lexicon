# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 17:50:31 2022

@author: Cristina GH
"""

import pandas as pd
import csv
import re
import os
import unidecode
import argparse
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("-infile","--infile", type=str, help="<str> Fichier en entrée", required=True)
parser.add_argument("-sep","--sepchar", type=str, help="<str> Separateur", required=True)
parser.add_argument("-out", "--saveto", type=str, help="<str> Save to defined path. If path '' save to current folder", required=False)

args = parser.parse_args()



def make_variants(dataframe, source_col):
    '''Produit des variants graphiques possibles

    Parameters
    ----------
    source_col : src
        colonne sur laquelle generer des variantes graphiques

    Returns
    -------
    DataFrame

    '''
    
    df = dataframe
    
    # RULES
    # accents et consonnes/voyelles dupliques
    mod_any = {'á':'a', 'é': 'e', 'í':'i', 'ó':'o', 'ú':'u',
                'à':'a', 'è': 'e', 'ì':'i', 'ò':'o', 'ù':'u',
                'ÿ':'y',  'ÿ':'i',
                'ä':'a', 'ë':'e', 'ï':'i', 'ö':'o', 'ü':'u',
                'â':'a', 'ê':'e', 'î':'i', 'ô':'o', 'û':'u',
                'aa':'a', 'áa':'a', 'áá':'a', 'aá':'a',
                'ii':'i', 'íi':'i', 'íí':'i', 'ií':'i',
                'ée':'e', 'éé':'e', 'eé':'e', 'ee':'e',
                'óo':'o', 'óó':'o', 'oó':'o', 'oo':'o',
                'úu':'u', 'úú':'u', 'uú':'u', 'uu':'uu',
                'ss':'s', 'tt':'t', 'rr':'r', 'bb':'b',
                'll':'l', 'y':'i', 'nn':'n', 'mm':'m',
                'oy':'oi'}
    
    # mod debut de mot
    mod_init = {'y':'i', 'py':'pi', 'ry':'ri',
                'qa':'qua', 'qe':'que', 'quy':'qui',
                'aus':'aux',
                'ý':'y', 'î':'i', 'ÿ':'y',
                'á':'a', 'é': 'e', 'í':'i', 'ó':'o', 'ú':'u',
                'à':'a', 'è': 'e', 'ì':'i', 'ò':'o', 'ù':'u',
                'ä':'a', 'ë':'e', 'ï':'i', 'ö':'o', 'ü':'u',
                'â':'a', 'ê':'e', 'î':'i', 'ô':'o', 'û':'u',
                }
    
    # mod fin de mot
    mod_end = {'th':'t', 'lx':'ls', 'x':'s', 'uoy':'uoi', 'syf':'sif',
               'sy':'i', 'cy':'ci', 'uy':'ui', 'ly':'li', 'my':'mi',
               'ty':'ti'}
    
    
    # SUBST
    # replace accents at any position
    df[f'{source_col}_any'] = df[source_col].apply(lambda x: [re.sub(y, z, x) for y, z in mod_any.items() if y in x])
    df[f'{source_col}_any'] = df[f'{source_col}_any'].apply(lambda x: list(set(x)))
    
    # replace at init
    df[f'{source_col}_init'] = df[source_col].apply(lambda x: [re.sub(f'(^{y})', z, x) for y, z in mod_init.items() if x.startswith(y)])
    
    # replace at end
    df[f'{source_col}_end'] = df[source_col].apply(lambda x: [re.sub(f'({y})$', z, x) for y, z in mod_end.items() if x.endswith(y)])
    
    
        
def norm_gen_variants(in_formes, sepchar):
    ''' Normalisation de formes inconnues et generation de variants graphiques pour la detection de lemmes possibles
    dans les lexiques morphologiques
    
    Parameters
    ----------
    in_formes : str
        fichier liste de formes
    sepchar : str
        separateur

    '''
    df = pd.read_csv(in_formes, sep=sepchar, encoding="utf-8", quoting=csv.QUOTE_NONE, names=['source_mot'], engine='python')

    #################
    #   ETAPE 1     #
    #################
    
    # Creation de formes possibles (avec accents [source] > sans accents [col1] > sans doublons [col2], avec accents sans doublons [col 3], noms speciaux [col 4])
    
    # - col 0: forme source
    df['source_mot']
    
    # - col 1 : suppresion de tous les accents et normalisation de caracteres (´ et autres vers > ' ): c’ > c'
    df['full_norm'] = df['source_mot'].apply(lambda x: unidecode.unidecode(x))
    
    # - col 2: pas de doublons sur les mots normalises
        # full norm word with no duplicate letters (gurbaal > gurbal, illumee > ilume, mercurii > merciru)
    df['full_norm_dupl'] = df['full_norm'].apply(lambda x: re.sub(r'(\w)\1+', r'\1', x))
    
    # - col 3 : pas de doublons sur les formes sources
    df['src_no_dupl'] = df['source_mot'].apply(lambda x: re.sub(r'(\w)\1+', r'\1', x))
    
    # - col 4 :selection de formes spécifiques pour traitement manuel (principalement conjonctions prep adv pron composes et noms de villes) : 
        # boute-en-corroie, la-quelle, hault-vergier, eulx-mesmes, ·ddextris
    df['forms_spec'] = ''
    df.loc[df['full_norm'].apply(lambda x: bool(re.search(r'[^0-9a-zA-Z]+', x))), 'forms_spec'] = df['full_norm']


    

    #################
    #   ETAPE 2     #
    #################
    
    # GENERATION DE VARIANTS
    
    # creer variants pour chaque colonne (sauf col 4 avec n. lieux etc)
    
    # sur les formes source
    make_variants(df, 'source_mot')
    
    # sur les normmalises
    make_variants(df, 'full_norm')
    
    # sur les sans-doublons normalises
    make_variants(df, 'full_norm_dupl')
    
    # sur les sans-doublons source
    make_variants(df, 'src_no_dupl')
    
    #################
    #   ETAPE 3     #
    #################
        
    # Mise en forme
    for col in df.columns[5:]:
        df[col] = df[col].apply(lambda x: ','.join(x)) # convert columns to list
    
    df['variants'] = df[df.columns[1:]].apply(lambda x: ','.join(x.astype(str)), axis=1) # expect forms, pass all variants to common list in a single column
    df['variants'] = df['variants'].apply(lambda x: [w for w in list(set(x.split(','))) if w != ''])
    
    df = df[['source_mot', 'variants']] # keep relevant columns (forme + variants candidats generes)
    
    manques_var = df.explode(['variants']).reset_index()    # explode the list, 1 variant per row (forme source + 1 variant)
    # manques_var = manques_var[manques_var.variants != manques_var.source_mot]          # ignore where forme source and variant are the same (it's a copy of the form generated during preprocessing, so useless)
    # keep the original forms lacking in the variants col in case they could be matched in others lexicons or dicts.
    manques_var['id'] = manques_var['index']
    del manques_var['index']
    
    print('>> Nombre de variants générés:', len(manques_var), 'sur', len(df), 'formes')
    
    #####
    # Save
    ####
    if args.saveto and Path(args.saveto).is_dir():
        # variants sans mise en forme (forme + liste de variants candidats)
        df.to_csv(str(args.saveto + "\\formes_variants.csv"), encoding='utf-8', sep='\t')
        
        # variants avec explode sur la liste de variants candidats (forme_source1 + var1, forme_source1 + var2, etc.)
        manques_var.to_csv(str(args.saveto + "\\formes_variants_explode.csv"), encoding='utf-8', sep='\t', index=None)
        
        print(f"\nFiles saved to '{args.saveto}'")
    
    elif not args.saveto:
        df.to_csv("manques_variants_generes(liste).csv", encoding='utf-8', sep='\t', quoting=csv.QUOTE_NONE)
        manques_var.to_csv("manques_variants_generes(explode).csv", encoding='utf-8', sep='\t', quoting=csv.QUOTE_NONE, index=None)
        
        print(f"\nFiles saved into current folder {os.getcwd()}")
        
    else:
        print("Saving path not found")
        
    #return manques_var

data = norm_gen_variants(args.infile, args.sepchar)

