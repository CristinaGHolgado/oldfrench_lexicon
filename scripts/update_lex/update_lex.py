# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 12:03:22 2022

@author: Cristina GH
"""


import pandas as pd
import csv
import re
import os
import warnings
warnings.filterwarnings('ignore')


save_to = "enrich_ofrlexdev\data"

folder_manques_annotes_par_pos = "enrich_ofrlexdev\data\\scripts_data\\annotations_by_pos"

# Missing forms (from merging)
last_manques = "scripts_data\\annotated_missing_forms_manques.tsv"

# Missing forms (from variants)
folder_manques_annotes = "scripts_data\\annotated_missing_forms_variants.tsv"


lm_df = pd.read_csv(last_manques, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE)

for file in os.listdir(folder_manques_annotes):
    df = pd.read_csv(str(folder_manques_annotes + file), sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE)
    df['pos'] = df['pos'].str.strip()
    
    if 'nompro' in file.lower():
        def cap(x):
            return '-'.join([y.capitalize() for y in x.split('-')]) if '-' in x else x.capitalize()
        
        npro_add = lm_df.loc[lm_df.pos == 'NOMpro']
        df_npro = df.append(pd.DataFrame({'src_mot': npro_add['source_mot'],
                                          'form': npro_add['variants'],
                                          'lemma_def': npro_add['lemme'],
                                          'pos': npro_add['pos']}), ignore_index=True)
        
        df_npro = df_npro.drop_duplicates(keep='first')
        df_npro.loc[df_npro.lemma_def.str.lower() == 'nompropre', 'lemma_def'] = df['form']
        
        df_npro = df_npro.fillna('__')
        
        for col in df_npro.columns:
            if col != 'pos':
                df_npro[col] = df_npro[col].apply(lambda x: cap(x))
        
        df_npro['src_mot'] = df_npro['src_mot'].str.replace('__','')
        
        df_npro.to_csv(str(save_to + 'v2_' + file), sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, index=None)
    
    
    if 'nomcom' in file.lower():
        ncom_add = lm_df.loc[lm_df.pos == 'NOMcom']
        df_ncom = df.append(pd.DataFrame({'src_mot': ncom_add['source_mot'],
                                          'form': ncom_add['variants'],
                                          'lemma_def': ncom_add['lemme'],
                                          'pos': ncom_add['pos'],
                                          'genre': ncom_add['morph'],
                                          'nombre': ncom_add['morph2']}), ignore_index=True)
        # split rows with '|' into new rows
        df_ncom['genre'] = df_ncom['genre'].str.split('\|')
        df_ncom = df_ncom.explode(['genre']).reset_index().fillna('')
        del df_ncom['index']
        
        # NOMS tous les masc son sing et plu
        df_ncom.loc[(df_ncom['genre'].str.contains('masc')) & (df_ncom['nombre'] == ''), 'nombre'] = 'sg|pl'
        # # # si nom fem termine pas s, plusiel sinon singulier
        df_ncom.loc[(df_ncom['genre'].str.contains('fem')) & (df_ncom['form'].str.endswith('s'))
                      & (df_ncom['nombre'] == ''), 'nombre'] = 'pl'
        df_ncom.loc[df_ncom['genre'].str.contains('fem') & (df_ncom['nombre'] == ''), 'nombre'] = 'sg'
        
        df_ncom['genre'] = df_ncom['genre'].str.replace('_','')
        
        ## si formes ne finissent par -s, -z ou -x c'est sg fem|masc or pl masc
        df_ncom.loc[(df_ncom['genre'] == '') & (df_ncom['form'].apply(lambda x: x.endswith(tuple(['s','z','x'])))), 'nombre'] = 'pl-fem|sg-masc|pl-masc'
        
        
        ### Remove duplicates (lema A with info vs lema A without info)
        """ e.g.
                  form lemma_def     pos genre nombre  has_morph
        112  ácuintez  accointe  NOMcom                       0  <-- del this
        113  ácuintez  accointe  NOMcom   fem     sg          1
        114  ácuintez   acompte  NOMcom  masc  sg|pl          1
        115  ácuintez   aceinte  NOMcom   fem     sg          1
        """
        df_ncom['has_morph'] = 0
        df_ncom.loc[df_ncom.genre != '', 'has_morph'] = 1
        df_ncom = df_ncom.groupby(['form','lemma_def','pos'], group_keys=False).apply(lambda x: x.loc[x.has_morph.idxmax()]).reset_index(drop=True)
        del df_ncom['has_morph']
        
        df_ncom.to_csv(str(save_to + 'v2_' + file), sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, index=None)
        
    if 'adv' in file.lower():
        adv_add = lm_df.loc[lm_df.pos.str.contains('ADV')]
        df_adv = df.append(pd.DataFrame({'src_mot': adv_add['source_mot'],
                                          'form': adv_add['variants'],
                                                'lemma_def': adv_add['lemme'],
                                                'pos': adv_add['pos'],
                                                'type': adv_add['morph']}), ignore_index=True).fillna('_')
        df_adv.loc[(df_adv.pos.str.endswith('neg')), 'type'] = 'negation'
        
        # remove dupls
        df_adv['has_morph'] = 0
        df_adv.loc[df_adv['type'] != '_', 'has_morph'] = 1
        df_adv.groupby(['form','lemma_def','pos'], group_keys=False).apply(lambda x: x.loc[x.has_morph.idxmax()]).reset_index(drop=True)
        del df_adv['has_morph']

        df_adv.to_csv(str(save_to + 'v2_' + file), sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, index=None)
        
    if 'adj' in file.lower():
        adj_add = lm_df.loc[lm_df.pos.str.contains('ADJ')]
        df_adj = df.append(pd.DataFrame({'src_mot': adj_add['source_mot'],
                                          'form': adj_add['variants'],
                                                'lemma_def': adj_add['lemme'],
                                                'pos': adj_add['pos'],
                                                'type': adj_add['morph']}), ignore_index=True)
        
        adjs = {'qua':'qualificatif', 'car':'cardinal', 'ind':'indefini', 'ord':'ordinal'}
        df_adj['type'] = df_adj['type'].apply(lambda x: [x.replace(y, z) for y, z in adjs.items() if x == y])
        df_adj['type'] = df_adj['type'].apply(lambda x: "".join(x))
        
        df_adj['pos'] = 'adjectif'
        
        df_adj = df_adj.drop_duplicates(keep='first')
        
        df_adj.to_csv(str(save_to + 'v2_' + file), sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, index=None)
        
    if 'ver' in file.lower():
        ver_add = lm_df.loc[lm_df.pos.str.contains('VER')]
        df_ver = df.append(pd.DataFrame({'src_mot': ver_add['source_mot'],
                                          'form': ver_add['variants'],
                                                'lemma_def': ver_add['lemme'],
                                                'pos': ver_add['pos'],
                                                'type': ver_add['morph']}), ignore_index=True).fillna('')
        df_ver['has_morph'] = 0
        df_ver.loc[df_ver['type'] != '_', 'has_morph'] = 1
        df_ver.groupby(['form','lemma_def','pos'], group_keys=False).apply(lambda x: x.loc[x.has_morph.idxmax()]).reset_index(drop=True)
        
        df_ver.loc[df_ver.pos.str.contains(','), 'pos'] = df_ver['pos'].apply(lambda x: x.split(', ')[0:2])
        df_ver = df_ver.explode(['pos'])
        df_ver = df_ver.fillna('')
        df_ver['pos'] = df_ver['pos'].str.strip()
        df_ver.loc[df_ver['feats'].str.contains(','), 'feats'] = ''
        df_ver['type'] = df_ver['pos'].apply(lambda x: x[-3:])
        conjs = {'inf':'infinitif', 'cjg':'conjugue', 'ppe':'participe passe', 'ppa':'ppa'}
        df_ver['type'] = df_ver['type'].apply(lambda x: [x.replace(y, z) for y, z in conjs.items() if x == y])
        df_ver['type'] = df_ver['type'].apply(lambda x: "".join(x))
        df_ver = df_ver.drop_duplicates(keep= 'first')
        
        del df_ver['has_morph']
        
        df_ver.to_csv(str(save_to + 'v2_' + file), sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, index=None)
    
    if 'pro' in file.lower():
        pro_add = lm_df.loc[lm_df.pos.str.startswith('PRO')]
        
        df_pro = df.append(pd.DataFrame({'src_mot': pro_add['source_mot'],
                                          'form': pro_add['variants'],
                                                'lemma_def': pro_add['lemme'],
                                                'pos': pro_add['pos'],
                                                'type': pro_add['morph']}), ignore_index=True)
        df_pro.loc[df_pro.pos.str.endswith('ind'), 'type'] = 'indefini'
        df_pro.loc[df_pro.pos.str.endswith('per'), 'type'] = 'personnel'
        df_pro.loc[df_pro.pos.str.endswith('rel'), 'type'] = 'relatif'
        df_pro.loc[df_pro.pos.str.contains('\.'), 'type'] = ''
        
        df_pro.to_csv(str(save_to + 'v2_' + file), sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, index=None)
    
    if 'pré' in file.lower():
        pre_add = lm_df.loc[lm_df.pos.str.startswith('PRE')]
        df_pre = df.append(pd.DataFrame({'src_mot': pre_add['source_mot'],
                                          'form': pre_add['variants'],
                                                'lemma_def': pre_add['lemme'],
                                                'pos': pre_add['pos'],
                                                'type': pre_add['morph']}), ignore_index=True)
        df_pre.to_csv(str(save_to + 'v2_' + file), sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, index=None)
    
    if 'con' in file.lower():
        con_add = lm_df.loc[lm_df.pos.str.startswith('CON')]
        df_con = df.append(pd.DataFrame({'src_mot': con_add['source_mot'],
                                          'form': con_add['variants'],
                                                  'lemma_def': con_add['lemme'],
                                                  'pos': con_add['pos'],
                                                  'type': con_add['morph']}), ignore_index=True)

        df_con['pos'] = df_con['pos'].apply(lambda x: str(x)[:3].upper() + str(x)[3:])
        df_con.loc[df_con.pos.str.endswith('coo'), 'type'] = 'coordination'
        
        df_con.to_csv(str(save_to + 'v2_' + file), sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, index=None)
        
    if 'det_' in file.lower():
        det_add = lm_df.loc[lm_df.pos.str.startswith('DET')]
        df_det = df.append(pd.DataFrame({'src_mot': det_add['source_mot'],
                                          'form': det_add['variants'],
                                                'lemma_def': det_add['lemme'],
                                                'pos': det_add['pos'],
                                                'type': det_add['morph']}), ignore_index=True)
        df_det.loc[(df_det.pos.str.endswith('def')), 'type'] = 'defini'
        df_det.loc[df_det.pos.str.endswith('ind')|(df_det.pos.str.endswith('ndf')), 'type'] = 'indefini'
        
        df_det.to_csv(str(save_to + 'v2_' + file), sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, index=None)
        