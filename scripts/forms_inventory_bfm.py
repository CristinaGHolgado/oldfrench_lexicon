import pandas as pd
import csv
import glob
import os
import re
import numpy as np
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', None)
np.set_printoptions(linewidth=160)
import warnings
warnings.filterwarnings('ignore')
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-in","--input_dir", type=str, help="<str> Path to directory with corpus files (.conllu)", required=True)
parser.add_argument("-out", "--outputname", type=str, help="<str> Output file name", required=True)
parser.add_argument("-ignore", "--ignore_files", type=str, help="<str> File(s) to ignore in (sub)directory")
args = parser.parse_args()


def prep_file(file):
	''' Preprocess BFMGOLDLEM corpus

	Parameters
	----------
	file : str
		Input .conllu file
	Returns
	-------
	DataFrame
	'''
	print(file)

	columns = ["id","form","lemma","upos","cattex","feats","head","deprel","deps","misc", "extra_col"]
	df = pd.read_csv(file, encoding="utf-8", sep="\t", quoting=csv.QUOTE_NONE, names=columns, index_col=False)
	
	if df.iloc[0][0] == 1:
		pass
	else:
		df = df.reset_index()

	# relevant columns
	df = df[["form","lemma","upos","cattex","feats","misc"]]
	
    # column: insert text sources
	df['file_src'] = file.split("\\")[-1].replace(".conllu","")

	# fix punctuation & fill empty rows
	df = df.fillna("_")
	df = df[~df.upos.str.contains("PUNCT")]

	# convert _ to - in forma & remove spaces
	df['form'] = df['form'].str.replace("_","-")
	df['form'] = df['form'].str.replace(" ","-")

	# column form lemma pos: concat values
	df['flp'] = df['form'] + "_" + df['lemma'] + "_" + df['upos']
	df['flp'] = df['flp'].str.lower()

	# lowercase lemmas/forms that are not proper nouns
	df = df.reset_index()
	df.loc[~df['upos'].str.contains("NOMpro"), 'lemma'] = df['lemma'].str.lower()
	df.loc[~df['upos'].str.contains("NOMpro"), 'form'] = df['form'].str.lower()

	# delete asterisc from forms & lowercase
	df['form'] = df['form'].str.replace("*","")
	df['form'] = df['form'].str.lower()

	df['lemma_src'] = 'no_source'
	df.loc[df['misc'].str.contains("LemmaSrc="), 'lemma_src'] = df['misc'].apply(lambda x: str(x.split("LemmaSrc=")[-1]).split("|")[0])
	
	# pass numbers from lemmas to new col
	df['n'] = "_"
	df.loc[df.lemma.str.contains(r'(\d+)'), 'n'] = df['lemma'].apply(lambda x: re.sub(r'(\d+)', '\__\\1', x).split("__")[-1])
	
	# remove numbers from forms/lemmas/flp if exist
	df['form'] = df['form'].apply(lambda x: re.sub(r"\d+","", x))
	df['lemma'] = df['lemma'].apply(lambda x: re.sub(r"\d+","", x))
	df['flp'] = df['flp'].apply(lambda x: re.sub(r"\d+","", x))
    
    # exclude rows where no lemma/cattex
	df = df[(df['lemma'] != '_')|(df['lemma'] == 'no_source')]
	df = df[df['cattex'] != '_']

	del df['misc']
	del df['index']

	return df



def make_inventory(folder_corpus, **ignore):
 	''' Merge BFMGOLDLEM files and build and inventory of forms and lemmas

 	Parameters
 	----------
 	folder_corpus : str
		Path to the corpus
 	ignore : str
		List of files to be ignored. It can be passed as a single item or multiple, separated by a comma

 	'''
 	print()

 	# files to be ignored in target dir
 	ignore_files = []

 	if args.ignore_files == True:
         ignore_files.append(str(ignore))
 	else:
         pass

 	# find .conllu files in folder_corpus (including .conllu files in subdirectories)
 	folder = [os.path.join(path, name) for path, subdirs, files in os.walk(folder_corpus) for name in files if ".conllu" in name]

 	# Prepare & concat .conllu files
 	df = [prep_file(file) for file in folder if file not in ignore_files]
 	concat_df = pd.concat(df, axis=0)

 	print("-- Input files:", len([file for file in folder if file not in ignore_files]))
 	print("-- Number of forms (PUNCT ignored):", len(concat_df))
 	
 	# add col: frequence form-lemma-pos
 	concat_df['freq'] = 1

 	inv = concat_df.groupby(['flp','form','lemma']).agg({'freq': [lambda x: x.sum()],
 											'lemma_src': [lambda x: ', '.join(x.unique())],
 											'file_src': [lambda x: ', '.join(x.unique())],
 											'cattex': [lambda x: ', '.join(x.unique())],
 											'feats': [lambda x: ', '.join(x.unique())],
 											'n': [lambda x: ', '.join(x.unique())]})
 	inv = inv.reset_index()
 	inv = inv.droplevel(1, axis=1) 
 	inv = inv.sort_values(by=['flp']) # sort entries by alphabetical order based of flp column (form-lemma-pos)
 	inv = inv[['flp','form','lemma','cattex','feats','lemma_src','file_src','freq','n']] # reorder columns
 	inv.rename(columns = {'feats':'feats_bfm', 'file_src':'file_src_bfm','freq':'occ_bfm'}, inplace = True)
     
 	
 	# Remove eventual duplicates (rare) and empty rows (lemma or pos)
 	inv = inv.drop_duplicates(keep='first')

 	print(f"-- Number of types (inventory size): {len(inv)} forms")
 	print(f"-- POS distribution \n {concat_df.groupby('cattex')['cattex'].count().sort_values(ascending=False)}")

 	inv.to_csv(f"{args.outputname}.tsv", sep='\t', encoding='utf-8', index=None, quoting=csv.QUOTE_NONE)

 	print(f"\n-- File saved at {args.outputname}")


make_inventory(args.input_dir)



