''' simple script to manage lgerm issues with encoding
'''

import os
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-in","--infolder", type=str, help="<str> Path to directory with corpus files. It will use all .conllu files including subdirectories", required=True)
parser.add_argument("-ext", "--extension", type=str, help="<str> file extension of input file (e.g.: '.txt', '.tsv', ...)", required=True)
parser.add_argument("-out", "--outfolder", type=str, help="<str> directory to save encoded files", required=True)
parser.add_argument("-source_enc", "--source_encoding", type=str, help="<str> source encoding of input files", required=True)
parser.add_argument("-target_enc", "--target_encoding", type=str, help="<str> target encoding", required=True)

args = parser.parse_args()


def convert(input_folder, file_extension, output_folder, from_encoding, to_encoding):
	''' Change encoding from files in a directory. 

	Parameters
	----------
	input_folder : str
		source folder
	file_extension : str
		file extension of input file (e.g.: '.txt', '.tsv', ...)
	output_folder : str
		directory to save encoded files
	from_encoding : str
		source encoding of input files
	to_encoding : str
		target encoding
	'''
	list_input_files = [os.path.join(path, name) for path, subdirs, files in os.walk(input_folder) for name in files if file_extension in name]

	for file in list_input_files:
		output_filename = file.split("\\")[-1].replace("iso_5","").replace(file_extension,f"_{to_encoding}.tsv")
		dir_output = os.path.join(output_folder, output_filename)

		commande = f"iconv -f {from_encoding} -t {to_encoding}//TRANSLIT " +f'"{file}" > "{dir_output}"; exit'
		conv = ["bash", "-c", commande]
		subprocess.call(conv)

		display_name = file.split('\\')[-1]
		print(f"Connverting {display_name} from {from_encoding} to {to_encoding} at {dir_output}")
		print()

# convert("..\\profiterole_lgerm\\lemmatise_iso", ".txt", "..\\profiterole_lgerm\\lemmatise_utf8", "iso-8859-1", "utf-8")

convert(args.infolder, args.extension, args.outfolder, args.source_encoding, args.target_encoding)