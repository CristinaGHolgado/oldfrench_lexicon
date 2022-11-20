# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 13:20:37 2022

@author: Cristina GH
"""

import pandas as pd
import csv
import glob

folder_lemmatized = glob.glob('Lemmatization models\corpus pos lemma\*')
folder_pos = glob.glob('Lemmatization models\corpus tagged UPOS\*')
manques = 'Lemmatization models\\manques11nov_v2.txt'


manques_df = pd.read_csv(manques, sep='\n', names=['form'])
manques_list = manques_df['form'].to_list()

dict_ = {}
def merge_files():
    for file_pos, file_lemma in zip(folder_pos, folder_lemmatized):
        lemma_fname, pos_fname = file_lemma.split('\\')[-1], file_pos.split('\\')[-1]
        # print(lemma_fname, pos_fname)
        df = pd.concat([pd.read_csv(f, sep='\t', quoting=csv.QUOTE_NONE, encoding='utf-8', names=[0,1]) for f in [file_pos, file_lemma]], axis=1)
        df.columns = ['form','pos','t','lemma']
        del df['t']
        df = df[df.form != 'token']
        name = 'Lemmatization models\\Corpus tagged lemmatized\\' + lemma_fname.split('_')[0] + '_nlppie.tsv'
        df.to_csv(name, sep='\t', index=None, header=False, quoting=csv.QUOTE_NONE)
        df_dict = df.set_index('form').T.to_dict('list')
        dict_.update(df_dict)

merge_files()

corpus_dict = pd.DataFrame.from_dict(dict_).T
corpus_dict = corpus_dict.reset_index()
corpus_dict.columns = ['form','upos','lemma']
corpus_dict['form'] = corpus_dict['form'].str.lower()
corpus_dict = corpus_dict.drop_duplicates()

# merge corpus dict to manques
merged_manques = manques_df.merge(corpus_dict, on='form', how='left')
merged_manques.to_csv('Lemmatization models\\manques_lemmatized_pie.tsv', sep='\t', index=None)