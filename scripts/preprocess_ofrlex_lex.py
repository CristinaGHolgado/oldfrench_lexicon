import pandas as pd
import csv
import os
import chardet
import re
import numpy as np
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 300)
pd.set_option('max_colwidth', None)
np.set_printoptions(linewidth=160)
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-in","--input_dir", type=str, help="<str> Path to directory with .lex files. It will use all .lex files including subdirectories", required=True)
parser.add_argument("-out", "--outputname", type=str, help="<str> Output file name", required=True)
parser.add_argument("-ignore", "--ignore_files", type=str, help="<str> File(s) to ignore in (sub)directory")
parser.add_argument("-cattex", "--cattex_pos", type=bool, help="<bool> Add Cattex pos tags to the lexicon", required=False)
args = parser.parse_args()


def ofrlex_inventory(file):
	''' Preprocess OFrLex lexicon (.lex): retrieve lemmas, insert upos, detect empty entries & unknown forms.
	
	It allows to build and aligned lexicon with the BFMGOLDLEM annotated corpus.
	
	Parameters
	----------
	file : str
		Input .lex file
	Returns
	-------
	DataFrame
	'''

# Detect file encoding & pass encoding to pandas csv
	check_encoding = "file --mime-encoding " + file
	file_encoding = str(os.popen(check_encoding).read().split()[1])
	
# read file, select first 9 cols, fill nans & add col names
	df = pd.read_csv(file, encoding=file_encoding, sep="\t", quoting=csv.QUOTE_NONE,
		names=list(range(20)))
	df = df.iloc[:,:9]
	df = df.fillna("_")
	df.columns = ['form','poids','pos','traits','lemme','morph1','morph2','indic','i']

	# delete not useful cols
	del df['poids']
	del df['i']

# New col: add file source
	df['file_src'] = str(file)

# New col: add lemmas (get lemmas without id)
	df['raw_lemme'] = df['lemme'].apply(lambda x: str(x).split("_")[0])


	def add_cattex():
	### USE IF CATTEX POS EVER NEEDED :
	# New col: Try to add cattex POS (contractions not avaliable)
		# Create cattex pos from lex info if upos & type in `traits` col
		df['cattex'] = ''
		# Insert Category (VER)
		df.loc[df.traits.str.contains('upos=') , 'cattex'] = df.traits.apply(lambda x: x.split('upos=')[1][:3] if "upos" in x else None)
		# Insert Type (inf)
		df.loc[df.traits.str.contains('type=') , 'cattex'] = df.cattex + df.traits.apply(lambda x: x.split('type=')[1][:3] if len(x.split('type=')) > 1 else None)

		# Tag forms/lemmas entries with cattex for some entries

		# VERBS
			# if "pl.1.ind.prs" in verb -> return VERind (verb + second to last morph2. info)
			# if only single morph. info (e.g.: "inf") -> return VERinf (verb + morph2. info)
		df.loc[df['pos'] == 'v', 'cattex'] = 'VER'+ df.morph2.apply(lambda x: 
			str(str(''.join(str(x).split(".")[-2])) if 
				len(str(x).split('.')) > 1 else x))
		
		df.cattex = df.cattex.str[:6] # cattex POS is 6 chars
		
		# PROPER NOUNS
		df.loc[df.traits.str.contains("upos=PROPN"), 'cattex'] = "NOMpro"
		# NOMcom
		df.loc[df.traits.str.contains("upos=NOUN"), 'cattex'] = 'NOMcom'
		# CONJS
		df.loc[df.pos == 'csu', 'cattex'] = "CONsub"
		df.loc[df.traits.str.contains("upos=CCONJ"), 'cattex'] = 'CONcoo'
		# ADJS
		df.loc[df.pos == 'adj', 'cattex'] = "ADJ" + df.indic.apply(lambda x: str(str(''.join(str(x).split("\%adj_")))[:3] if len(str(x).split('.')) >= 1 else ''))
		df.loc[df.cattex.str.contains("%") , 'cattex'] = df['cattex'].str[:3]+"xx"
		df.loc[df.cattex.str.contains("ADJxx"), 'cattex'] = "VERpp"
		df.loc[df.cattex.str.contains("SCO"), 'cattex'] = "CONsub"
	

# New col: unknown
	df['inconnu'] = 0
	df.loc[df['traits'].str.contains('99999'), 'inconnu'] = 1

# New col: UPOS 
	df['upos'] = ''
	df.loc[df['traits'].str.contains("upos="), 'upos'] = df['traits'].apply(lambda x: "".join([info for info in x.split(",") if "upos=" in info]))
	df['upos'] = df.upos.apply(lambda x: re.sub(r"\]|\[","",str(x)).replace("'",""))
	df.loc[df['upos'].str.contains("upos="), 'upos'] = df['upos'].apply(lambda x: "".join(x.split("=")[-1]))
	# insert column to note forms where upos missing in traits col for the forms
	df['no_upos'] = 0
	df.loc[df['upos'].isna(), 'no_upos'] = 1
	# or
	df.loc[df['upos'].str.isalpha() == False, 'no_upos'] = 1
	
	# Now we can fill empty upos (no upos info in `traits` col) with the upos of the df
	df['upos'] = df['upos'].fillna(method='ffill')
	# if no upos (it happens with some verb lex files) fill with default pos
	df.loc[df['upos'].isna(), 'upos'] = df['pos']
	# it seems empty rows are not detected as nan so we use .isalpha()
	df.loc[df['upos'].str.isalpha() == False, 'upos'] = df['pos']

	# convert the pos to upos (all forms lacking of upos in `traits` are verbs)
	df.loc[df['upos'].apply(lambda x: x == 'v'), 'upos'] = 'VERB'

	# For future queries: return rows where no upos avaliable for the source form
	show_missing_upos = df.loc[df.upos.str.len() < 3]
	if len(show_missing_upos) >= 1:
		print("UPOS missing in {file} at:")
		print(show_missing_upos)
	else:
		pass

# Insert cattex tags to dataframe
	if args.cattex_pos == True:
		add_cattex()
	else:
		pass

# Fill the rest of empty rows in the dataframe
	df = df.fillna("_")

# delete not used colums (to reduce output file size)
	del df['morph1']
	del df['morph2']
	del df['indic']

	return df



if  os.listdir(args.input_dir) == []:
	print(args.input_dir)
	print("No files found in specifies folder.")

else:
	files_dir = args.input_dir
	print(f"Selecting files in: {Path(files_dir).absolute()}")
	print(f"Ignored files: {args.ignore_files}")
	
	# files to be ignored in target dir (with extension)
	list_ignore_files = []
	list_ignore_files.append(str(args.ignore_files))

	# find .lex files in files_dir (including .lex files in subdirectories)
	folder = [os.path.join(path, name) for path, subdirs, files in os.walk(files_dir) for name in files if ".lex" in name]
	
	folder = [f for f in folder if f.split("\\")[-1] not in list_ignore_files]
	
	# Prepare & concat .lex files
	df = [ofrlex_inventory(file) for file in folder if file not in list_ignore_files]
	inventory_ofrlex = pd.concat(df, axis=0)

	# save merged lexicon
	inventory_ofrlex.to_csv(str(args.outputname + ".tsv"), sep='\t', encoding='utf-8', index=None, quoting=csv.QUOTE_NONE)

