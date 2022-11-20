# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 22:57:52 2022

@author: Cristina GH

Takes list of forms (missing in ofrlex) that have been lemmatized by lgerm (or not, plain list of forms)
and aligns the annotations to multipleexternal lexical sources.
If missing lemmatized forms are passed, they are aligned to the BFMLEMGOLD inventory and Frolex
lexicon. If plain list of forms are passed, they are first aligned to the entries in lgerm lexicon.

Annotated forms are aligned based of matching on forms. Multiple POS can thus correspond to a single form,
so different POS may be associated to it.

A sorting is done based on POS (normalized in all sources**) given priority to BFM/FRO:
    
    - If all ressources agree on a POS for a form, the BFM lemma and POS is choosen. Priority goes to
    medieval sources to avoid spelling variation on lemmas.
    - If no matches:
        case 1) Lgerm A, BFM B, Frolex B ->> Candidate Lgerm + Candidate BFM (because each may propose a
                                                                              different category which is
                                                                              absent in the other source)
        Case 2) Lgerm A, BFM B, Frolex C ->> Three candidates
        Case 3) Missing Lgerm -> BFM if avaliable, if not Frolex (for same POS, otherwise add both)
        Case 4) Missing BFM or FRO -> Add both if different pos, otherwise, choose Frolex or BFM
        Case 5) No candidates -> Unknown (à générer des variants pour relancer un le matching)
                                                                              
                                                                                                                                            
** Each dataframe for each ressource posses a column with the main homogeneus cattex category, as lgerm
uses different annotation formatting (´subst.´ rather than ´NOMcom´)

This script uses the next files :
    - Manques.txt OU Manques annotés par LGERM
    - Lexique LGeRM*
    - Inventaire BFMGOLD
    - Lexique Frolex

And returns a file per POS and a file including remaining unknown forms

"""


import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import csv
import re

pd.set_option('display.max_rows', None)



def prep_lg(manques_lgerm, mode):
    """
    Load and preprocess annotated (or plain) missing forms and match them to lgerm lexicon
    if plain.

    Parameters
    ----------
    manques_lgerm : str
        Annotated (or plain) unknwon forms
    mode : str
        'lemmatise': already annotated missing forms
        'lexique': plain forms to be merged to lgerm lexicon

    Returns
    -------
    DataFrame

    """
    
    if mode == 'lemmatise':
        print('\n~ Loading lemmatized forms...\n')
        '''Prepare sortie lgerm3'''
        df_morph = pd.read_csv(manques_lgerm, sep='\t', encoding='utf-8', 
                               quoting=csv.QUOTE_NONE, names=['form','0','nb1','nb2','lemma_lgerm'])
    
        df_morph = df_morph[['form','lemma_lgerm']]
        
        # split multiple hypothesis into new rows
        df_morph['lemma_lgerm'] = df_morph['lemma_lgerm'].apply(lambda x: x.split('|') 
                                                        if '|' in x else x)
        df_morph = df_morph.explode('lemma_lgerm')
        df_morph = df_morph.drop_duplicates(keep='first')
       
        # normalize postags
        df_morph['pos_lg'] = ''
        
        df_morph['pos_lg'] = df_morph['lemma_lgerm'].apply(lambda x: x.split('@')[1] 
                                                    if '@' in x else 'NO_POS')
        
        df_morph['lemma_lgerm'] = df_morph['lemma_lgerm'].apply(lambda x: re.sub('\d+|µ','', x.split('@')[0]) 
                                                        if '@' in x else x)
        df_morph = df_morph.fillna('?')
        df_morph['pos_lg'] = df_morph['pos_lg'].apply(lambda x: x.split(' et ') 
                                                      if ' et ' in x else x)
    
        df_morph = df_morph.explode('pos_lg')
        df_morph['pos_lg'] = df_morph['pos_lg'].apply(lambda x: x.split(', ') 
                                                      if ', ' in x else x)
        df_morph = df_morph.explode('pos_lg')
        df_morph['pos_lg'] = df_morph['pos_lg'].apply(lambda x: x.split(' ou ')
                                                      if ' ou ' in x else x)
        df_morph = df_morph.explode('pos_lg')
        df_morph = df_morph.reset_index()
        df_morph.loc[df_morph['lemma_lgerm'] == '_NOM_PROPRE', 'lemma_lgerm'] = df_morph['form']
        df_morph.loc[df_morph['pos_lg'] == 'NOM_PROPRE', 'pos_lg'] = 'nom propre'
        
        df_morph['lemma_lgerm'] = df_morph['lemma_lgerm'].str.lower()
        df_morph.loc[df_morph['pos_lg'].str.contains('propre'), 'lemma_lgerm'] = df_morph['lemma_lgerm'].str.capitalize()
        df_morph['lemma_lgerm'] = df_morph['lemma_lgerm'].str.replace('œ', 'oe')
        df_morph['lemma_lgerm'] = df_morph['lemma_lgerm'].apply(lambda x: re.sub('^_', '', x))
        
        del df_morph['index']
        df_morph = df_morph[['form','lemma_lgerm','pos_lg']].drop_duplicates()
        
        return df_morph

    if mode == 'lexique':
        # Prepare lgerm lexicon
        print('\n~ Loading lexicon and matching unkown form to lex entries...\n')
        
        lex_lgerm = pd.read_csv(lexique_lgerm, sep=';', encoding='iso-8859-1', quoting=csv.QUOTE_NONE)
        
        
        ## Rename columns, select relevant cols
        lex_lgerm.columns = ['form', 'lemma_lgerm', 'pos_lg', 'src', 'in', 'id', '_'] # variants is 'formes' but done to merge on same dfs key
        lex_lgerm = lex_lgerm[['form','lemma_lgerm','pos_lg']]
        
        #######
        # Preprocess
        ########
        
        # Fix chars
        lex_lgerm['form'] = lex_lgerm['form'].apply(lambda x: re.sub('_|$|\]|\[|\s|µ', '', str(x)))
        lex_lgerm['form'] = lex_lgerm['form'].str.lower()
        lex_lgerm['lemma_lgerm'] = lex_lgerm['lemma_lgerm'].apply(lambda x: re.sub('_|$|\]|\[|\s|\d+|µ', '', str(x)))
        lex_lgerm['lemma_lgerm'] = lex_lgerm['lemma_lgerm'].str.lower()
        lex_lgerm = lex_lgerm.drop_duplicates(keep='first')
        lex_lgerm = lex_lgerm.fillna('')
        
        lex_lgerm = lex_lgerm.drop_duplicates(keep='first')

        df_morph = lex_lgerm
        
        # split multiple pos into new rows
        df_morph['pos_lg'] = df_morph['pos_lg'].apply(lambda x: x.split('|') 
                                                        if '|' in x else x)
        df_morph = df_morph.explode('lemma_lgerm')
        df_morph = df_morph.drop_duplicates(keep='first')
        
        df_morph['pos_lg'] = df_morph['pos_lg'].apply(lambda x: x.split(',') 
                                                        if ',' in x else x)
        df_morph = df_morph.explode('pos_lg')
        
        df_morph = df_morph.drop_duplicates(keep='first')

        # normalize postags

        df_morph['pos_lg'] = df_morph['pos_lg'].apply(lambda x: x.split('@')[1] 
                                                    if '@' in x else x)
        df_morph = df_morph.explode('pos_lg')
        
        df_morph['pos_lg'] = df_morph['pos_lg'].apply(lambda x: re.sub('\d+|µ','', x.split('@')[0]) 
                                                          if '@' in x else x)
        df_morph = df_morph.fillna('_')
        df_morph['pos_lg'] = df_morph['pos_lg'].apply(lambda x: x.split(' et ') 
                                                      if ' et ' in x else x)

        df_morph = df_morph.explode('pos_lg')
       
        df_morph['pos_lg'] = df_morph['pos_lg'].apply(lambda x: x.split(' ou ')
                                                      if ' ou ' in x else x)
        df_morph = df_morph.explode('pos_lg')
        df_morph = df_morph.reset_index()
        df_morph.loc[df_morph['lemma_lgerm'] == '_NOM_PROPRE', 'lemma_lgerm'] = df_morph['form']
        df_morph.loc[df_morph['pos_lg'] == 'NOM_PROPRE', 'pos_lg'] = 'nom propre'
        
        df_morph['lemma_lgerm'] = df_morph['lemma_lgerm'].str.lower()
        df_morph.loc[df_morph['pos_lg'].str.contains('propre'), 'lemma_lgerm'] = df_morph['lemma_lgerm'].str.capitalize()
        df_morph['lemma_lgerm'] = df_morph['lemma_lgerm'].str.replace('œ', 'oe')
        df_morph['lemma_lgerm'] = df_morph['lemma_lgerm'].apply(lambda x: re.sub('^_', '', x))
        
        df_morph['pos_lg'] = df_morph['pos_lg'].str.strip()

        df_morph = df_morph[['form','lemma_lgerm','pos_lg']].drop_duplicates()

        
        # merge lexique lgerm forms to manques
        
        manques_df = pd.read_csv(manques_file, sep='\t', encoding='utf-8', names=['form'], quoting=csv.QUOTE_NONE)
        aligned_manques_lgerm = manques_df.merge(df_morph, on='form', how='left')

        return aligned_manques_lgerm





def prep_bfm(inventaire_bfmgoldlem):
    print('\n~ Loading BFMGOLD inventory...\n')
    '''Prepare bfmgoldlem'''
    cols = 'flp','form','lemma','cattex','feats_bfm','lemma_src','file_src_bfm','occ_bfm','n'
    bfm = pd.read_csv(inventaire_bfmgoldlem, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, names=cols)
    bfm = bfm[['form','lemma','cattex']]
    bfm = bfm.fillna('_')
    bfm.loc[bfm['cattex'].str.contains(','), 'cattex'] = bfm['cattex'].str.split(', ')
    bfm = bfm.explode('cattex')
    bfm['lemma'] = bfm['lemma'].apply(lambda x: x.replace('*', ''))
    bfm['lemma'] = bfm['lemma'].str.replace('œ','oe')
    bfm = bfm[bfm.lemma != 'no_lem']
    bfm = bfm.reset_index()
    del bfm['index']
    bfm.loc[(bfm.cattex == 'NOMpro') & (bfm.lemma == '_'), 'lemma'] = bfm['form']
    bfm = bfm.drop_duplicates(keep='first')
    bfm = bfm[bfm.lemma != '_']
    bfm.set_index('form')
    
    return bfm
    



def merge_bfm_lgerm(manques_lgerm, inventaire_bfm):
    print('\n~ Merging unknown forms to BFMGOLD...\n')
    '''Merge lgerm with bfm on form'''

    mg = manques_lgerm.merge(inventaire_bfm, on='form', how='left')
    
    # Normalizations
    
    mg.loc[(mg['lemma_lgerm'] == 'nan')|(mg['lemma_lgerm'] == 'mot_inconnu'), 'lemma_lgerm'] = '_'
    mg.loc[(mg['lemma_lgerm'] == 'nan')|(mg['lemma_lgerm'] == 'mot_inconnu'), 'pos_lg'] = '_'
    mg['pos_lg'] = mg['pos_lg'].replace('NO_POS', '_')
    mg = mg.fillna('_')
    
    
    pos = {'@verb':'VER', 'verbe' : 'VER', 'part. prés.':'VER',
            'adj. fém.': 'ADJ',  'adj. masc.':'ADJ', 'adj. indéf.':'ADJ', 'adj.':'ADJ',
            'subst. masc.': 'Nco', 'NOMcom':'Nco', 'subst. fém.':'Nco', 'subst.':'Nco', 'masc.':'Nco', 'fém.':'Nco',
            'subst. fém. plur.':'Nco', 'subst. fém. (et masc.)':'Nco', 'subst. fém. (et masc.)':'Nco',
            'subst. masc. plur.':'Nco', 'subst. masc. (et fém.)': 'Nco', 'subst. plur.':'Nco',
            'adv. d\'intensité':'ADV', 'ADV':'ADV', 'adv. de nég.':'ADV', 'adv.':'ADV', 'adv. de temps':'ADV',
            'adv. de lieu':'ADV',
            'nom pro':'Npo', 'NOMpro':'Npo', 'nom de lieu':'Npo', 'nom lieu':'Npo', 'nom propre':'Npo',
            '@pron':'PRO', 'pron.':'PRO', 'pron. indéf.': 'PRO', 'pron. pers.': 'PRO', 'pron. adv.':'PRO',
            'interj.':'INTJ', '@INJ':'INTJ', 
            '@prép':'PRE', '@conj':'CONJ', '@PRO':'PRO',
            '@PRE':'PRE', '@DET':'DET', 'art. déf.':'DET', 'art.':'DET',
            '@CON':'CON', 'conj.':'CON', 'conj. de coord.':'CON',
            'prép. + pron. pers.':'PRE.PROper',  'prép.':'PRE',
            'art. contr.': 'DET',
            'loc. adv.':'LOC',
            'mot lat.':'LAT', 'mot latin':'LAT',
            'adv. conj.':'COMP',
            'adj. num.':'DET',
            '(?)':'AMBIGU_', '_':'INCONNU_', '':'AMBIGU_',
            'interr.':'AMBIGU_','num.':'AMBIGU_','quantif.':'AMBIGU_','poss.':'AMBIGU_','dém.':'AMBIGU_','indéf.':'AMBIGU_',
            'rel. interr.':'AMBIGU_'
            }
    
    mg['fixed_lg_pos'] = mg['pos_lg']
    
    for y, z in pos.items():
        mg.loc[mg.fixed_lg_pos == y, 'fixed_lg_pos'] = z
        
    # fix pos in cattex bfm (first 3 letters to match items in lgerm)
    mg['cattex'] = mg['cattex'].str.replace('NOMcom','Nco')
    mg['cattex'] = mg['cattex'].str.replace('NOMpro','Npo')
    mg['fixed_cattex_bfm'] = mg['cattex']
    mg['fixed_cattex_bfm'] = mg['fixed_cattex_bfm'].apply(lambda x: x[:3] if '.' not in x else x)
    
    
    return mg





def merge_frolex(merged_bfm_lg_df, frolex_file):
    print('\n~ Loading Frolex lexicon and merging to unknow forms...\n')
    ''' Add frolex to merged lg and bfm'''
    
    fro_df = pd.read_csv(frolex_f, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE)
    fro_df = fro_df[['form', 'msd_cattex_conv2', 'lemma']]
    fro_df = fro_df.rename(columns={'msd_cattex_conv2': 'cattex_fro', 'lemma': 'lemma_fro'})
    fro_df = fro_df[fro_df['lemma_fro'] != '<no_lemma>']
    fro_df['lemma_fro'] = fro_df['lemma_fro'].apply(lambda x: re.sub('\d+','', str(x)))
    
    merged_fro = merged_bfm_lg_df.merge(fro_df, on='form', how='left')
    merged_fro = merged_fro.fillna('_')
    
    # Adapt tags to fixed lg/bfm pos
    merged_fro['cattex_fro'] = merged_fro['cattex_fro'].str.strip().replace('NOMcom', 'Nco')
    merged_fro['cattex_fro'] = merged_fro['cattex_fro'].str.strip().replace('NOMpro', 'Npo')
    merged_fro['cattex_fro'] = merged_fro['cattex_fro'].apply(lambda x: x[:3] if '.' not in x else x)
    
    print('Frolex matches sur the merged_bfm_lg')
    print(len(merged_fro.loc[merged_fro.lemma_fro != '_'][['form', 'lemma_fro', 'cattex_fro']].drop_duplicates()))
    
    return merged_fro




'''TRIS '''

print('\n\nSelecting lemmas and POS')

def tri_manques(merged_dfs):
    print('\n~ Sorting lemmas and POS from lexical ressources for the unknown forms...\n')
    ## RULES
    # If aLL agree on poss, pas fro lem+pos
    # if fro + bfm agree pas fro pos
    # if lg and fro not agree pas fro
    # if lg and bfm not agree pass bfm
    # else pass bfm
    
    merges = merged_dfs
    merges['lem_pos'] = '_'
    
    # Formes pour lesquelles in n'y a eu aucune proposition 
    inconnus = merges[(merges.fixed_lg_pos.str.contains('_')) & (merges.fixed_cattex_bfm == '_') & (merges.cattex_fro == '_')]
    inconnus = inconnus['form'].drop_duplicates().to_list()
 
    print('Nombre de formes inconnues (no dupls, aucune proposition)', len(inconnus), 'sur', len(merges))
    # Formes porulesquelles il y a des propositions (soit legerm, bfm ou ofrlex)
    merges['inc'] = 0
    merges.loc[(merges.fixed_lg_pos.str.contains('_')) & (merges.fixed_cattex_bfm == '_') & (merges.cattex_fro == '_'), 'inc'] = 1
    merges = merges[merges.inc == 0]
    del merges['inc']
    
    print('Nombre de formes pour lesquelles il y a eu une proposition', len(merges))
    
    # If aLL agree on poss, pas fro lem+pos
    merges.loc[(merges.fixed_lg_pos == merges.fixed_cattex_bfm) & 
                (merges.fixed_cattex_bfm == merges.cattex_fro), 'lem_pos'] = merges['cattex_fro'] + '@' + merges['lemma_fro']
    merges['lem_pos'] = merges['lem_pos'].str.replace('_@_','_')
    
    # if no commons 3 at same time (3 same POS), juntalos y elimina los valores vacios ( aka '_@_)
    merges.loc[(merges.lem_pos == '_'), 'lem_pos'] = merges['fixed_lg_pos'] + '@' + merges['lemma_lgerm'] + '|' + merges['cattex_fro'] + '@' + merges['lemma_fro'] + '|' + merges['cattex'] + '@' + merges['lemma']
    merges['lem_pos'] = merges['lem_pos'].apply(lambda x: [w for w in x.split('|') if w != '_@_'])
    
    # is list with 2 items is the 2 same pos, select last item (= lema from fro or bfm)
    merges.loc[merges['lem_pos'].apply(lambda x: len(x) == 2), 'lem_pos'] = merges['lem_pos'].apply(lambda x: x[-1] if str(x[-1])[:3] == str(x[0])[:3] else x)
    
    merges.loc[merges['lem_pos'].apply(lambda x: len(x) == 2), 'lem_pos'] = merges['lem_pos'].apply(lambda x: '|'.join(x))
    
    # remove duplicates from lists
    merges.loc[merges['lem_pos'].apply(lambda x: len(x) == 3), 'lem_pos'] = merges['lem_pos'].apply(lambda x: list(set(x)))
    merges.loc[merges['lem_pos'].apply(lambda x: len(x) == 2), 'lem_pos'] = merges['lem_pos'].apply(lambda x: x[-1] if str(x[-1])[:3] == str(x[0])[:3] else x)
    merges.loc[merges['lem_pos'].apply(lambda x: len(x) == 2), 'lem_pos'] = merges['lem_pos'].apply(lambda x: '|'.join(x))
    
    
    # if frist item and second same POS, select second and add thir as JOINED
    merges.loc[merges['lem_pos'].apply(lambda x: len(x) == 3), 'lem_pos'] = merges['lem_pos'].apply(lambda x: x[1] if len(x) == 3 and str(x[0])[:3] == str(x[1])[:3] else x)
    merges.loc[merges['lem_pos'].apply(lambda x: len(x) == 3), 'lem_pos'] = merges['lem_pos'].apply(lambda x: x[2] if len(x) == 3 and str(x[0])[:3] == str(x[2])[:3] else x)
    merges.loc[merges['lem_pos'].apply(lambda x: len(x) == 3), 'lem_pos'] = merges['lem_pos'].apply(lambda x: x[1] if len(x) == 3 and str(x[1])[:3] == str(x[2])[:3] else x)
    
    merges.loc[merges['lem_pos'].apply(lambda x: len(x) == 3), 'lem_pos'] = merges['lem_pos'].apply(lambda x: '|'.join(x))
    merges.loc[merges['lem_pos'].apply(lambda x: len(x) == 1), 'lem_pos'] = merges['lem_pos'].apply(lambda x: ''.join(x))
    
    merges.loc[merges['lem_pos'].str.contains('|'), 'lem_pos'] = merges['lem_pos'].apply(lambda x: '|'.join([w for w in x.split('|') if 'INCONNU' not in w]))
    
    ## split pos_lem into new rows where 3 sources propose different pos and rest
    merges['lem_pos'] = merges['lem_pos'].str.split('|')
    
    merges = merges.explode(['lem_pos']).reset_index()
    merges['lemma_def'] = merges['lem_pos'].apply(lambda x: x.split('@')[-1])
    merges['pos_def'] = merges['lem_pos'].apply(lambda x: x.split('@')[0])
    del merges['lem_pos']
    
    merges.loc[merges['pos_def'] == 'NOM', 'pos_def'] = 'Nco'
    
    merges = merges[['form','lemma_def','pos_def']].drop_duplicates()
   
    # save inconnus
    inconnus_final = list(sorted(set(inconnus) - set(merges['form'].drop_duplicates().to_list())))
    inconnus = pd.DataFrame(inconnus)
    inconnus.to_csv(str(folder + '\\script_outputs\\inconnus_after11nov.txt'), sep='\t', encoding='utf-8', index=None, quoting=csv.QUOTE_NONE)
    
    return merges

def save_df_by_pos(df):
    df['p'] = df['pos_def'].apply(lambda x: x[:3] if '.' not in x else x)
    pos = df['p'].drop_duplicates().to_list()
    # save full df
    print('\n ~ Saving final annotated missing forms...\n')
    df.to_csv(str(folder + '\\script_outputs\\' + 'manques_annoté_full_tri_lemmat.txt'), sep='\t', encoding='utf-8', index=False)
    for p in pos:
        df_pos = df[df['p'] == p]
        nom = folder + '\\script_outputs\\manques_tri_pos\\' + f'_{p}_lemmat.tsv'
        df_pos.to_csv(nom, sep='\t', encoding='utf-8', index=False, quoting=csv.QUOTE_NONE)

    return df




######################
##      FILES       ##
######################


folder = 'scripts\\enrich_ofrlexdev\\'
manques_lemmatisees = folder + "manques\\lgerm_tagged_manques11nov_3.tsv" # Formes manquantes lemmatisées avec lgerm (no desamb.)
inventory_bfm = folder + 'ressources\\' + "inventaire_bfmgoldlem_nonorm.tsv" # Inventaire du corpus BFMGOLDLEM
frolex_f = folder + 'ressources\\frolex_lexique.tsv' # Lexique Frolex
lexique_lgerm = "lgerm\\lexiques\\graphies_MF.txt" # Lexique lgerm
manques_file = folder + "manques\\manques11nov.txt" # Manques



#########################
# PREPARE FILES        ##
#########################


manques_annotes_lgerm = prep_lg(manques_lemmatisees, mode='lemmatise')
# manques_annotes_lgerm = prep_lg(lexique_lgerm, mode='lexique') # applique sur les variantes graphiques generes

bfm_entries = prep_bfm(inventory_bfm)

## Merge entries on form (no tri yet)
merged_bfm_lg = merge_bfm_lgerm(manques_annotes_lgerm, bfm_entries)

merges = merge_frolex(merged_bfm_lg, frolex_f)

manques_final = tri_manques(merges)

print('Formes qui ont pu etre annotes (no dupls):')
print(len(manques_final['form'].drop_duplicates()))

save = save_df_by_pos(manques_final)


#################################
# CHIFFRES SUR LES ANNOTATIONS ##
#################################

print(f'\nSur ~32000 manques, LGeRM a trouvé {len(manques_annotes_lgerm)} possibilités.')
print('\n>> Distribution des catégories trouvés par LGeRM sur les manques annotées:')
pos_grouped_lgerm = merged_bfm_lg.groupby(['fixed_lg_pos'])['fixed_lg_pos'].size().sort_values(ascending=False)
print(pos_grouped_lgerm)

print(f'\n\nWith both sources merged, we found a total of {len(merged_bfm_lg)} possibilities')

bf = merged_bfm_lg[(merged_bfm_lg.cattex != '_') & (merged_bfm_lg.lemma != '_')]

bf['cattex'] = bf['cattex'].apply(lambda x: x[:3] if '.' not in x else x)
print(f"\nTrouvées dans l\'inventaire du corpus BFMGOLDLEM : {len(bf)}")
pos_grouped_bfm = bf.groupby(['cattex'])['cattex'].size().sort_values(ascending=False)
print(f"\nDistribution des catégories pour la BFM {pos_grouped_bfm}")
