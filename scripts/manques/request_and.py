# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 22:57:52 2022

@author: Cristina GH

Script pour faire des requÊtes sur le AND pour les formes manquantes que n'ont pas été trouvées dans autres ressources lexicales
"""

from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import re
import enchant
import unicodedata


    
def and_entries(url, form):
    ''' Scrap entries from the Anglo-Normand Dictionnary to return POS and lemma(s) for unnanotated forms

    Parameters
    ----------
    url : str
        Website adress on search query
    form : str
        Form to be requested on dictionnary

    Returns
    -------
    dict

    '''
    # data = {}
    # entries = pd.DataFrame(data, columns=['form', 'pos', 'cognates'])
    

    site_link = url + form
    page = requests.get(site_link)
    soup_ = BeautifulSoup(page.content, 'html.parser')

    texte = soup_.text
    
    print(f"Requested form : {form.upper()}")
    
    if bool(re.search('Your search matched 0 entries', texte)):
        print(f"No entries for the form {form}")
        forms_no_matches.append(form)
    
    elif bool(re.search('search matched \d+ entries', texte)):
        print(f"Matching entries for {form}")
        
        data = [a for a in soup_.find_all("div", id='searchResults') if a.text]
        entries = [entry.find_all("h4") for entry in data]
        
        for entry in entries:
            # as this returns multiple entries for a form, we
            # need to get the href of the entry and acces it
            #so we can have acces to the cognates
            href_entries = []
            for href_item in entry: # get href in a
                hrefs = href_item.find_all('a', href=True)
                for a in hrefs:
                    if a.text:
                        href_entries.append(a['href'])
                    else:
                        pass
            for ref in href_entries: # request each entry
                # egt distance between form and lemmas to avoid requesting too many
                # forms and that could not be useful
                ref_entry = re.sub('\d+&_', '', str(ref.split('/')[-1]))
                dist = enchant.utils.levenshtein(form, ref.split('/')[-1])
                
                if dist <= 3:
                    print(ref_entry.upper(), dist)
                    page = requests.get(str("https://anglo-norman.net/" + ref))
                    soup = BeautifulSoup(page.content, 'html.parser')

                    
                    if soup.find("span", class_="summaryPos") is None:
                        print(f'Matching entries for {form}')
                        refs = soup.find(id="cognateRefs").text
                        lemma = soup.find(id="entryTitle").text
                        pos = soup.find("h4", class_="entryPos")
                        pl = lemma + '__' + pos.text 
                        
                        pos_lem['form'].append(str(form))
                        pos_lem['cognates'].append(str(refs))
                        pos_lem['lemma_pos'].append(str(pl))
                        print()
                        
                    else:
                        print(f'Matching entry for {form}')
                        lemma = soup.find(id="entryTitle").text
                        refs = soup.find(id="cognateRefs").text
                        pos = soup.find("span", class_="summaryPos")
                        pl = lemma + '__' + pos.text 
                        
                        pos_lem['form'].append(str(form))
                        pos_lem['cognates'].append(str(refs))
                        pos_lem['lemma_pos'].append(str(pl))
                else:
                    print(f"Entry {ref_entry.upper()} ignored (distance > 3)")
                    print()

    
    else:
        # cases where only 1 entry is matched
        if soup_.find("span", class_="summaryPos") is None:
            print(f'Matching entry for {form}')
            refs = soup_.find(id="cognateRefs").text
            lemma = soup_.find(id="entryTitle").text
            pos = soup_.find("h4", class_="entryPos")
            pl = lemma + '__' + pos.text 
            
            pos_lem['form'].append(str(form))
            pos_lem['cognates'].append(str(refs))
            pos_lem['lemma_pos'].append(str(pl))
            
        else:
            print(f'Matching entry for {form}')
            lemma = soup_.find(id="entryTitle").text
            refs = soup_.find(id="cognateRefs").text
            pos = soup_.find("span", class_="summaryPos")
            pl = lemma + '__' + pos.text 
            
            pos_lem['form'].append(str(form))
            pos_lem['cognates'].append(str(refs))
            pos_lem['lemma_pos'].append(str(pl))
            
    return pos_lem


def format_entries(df):
    '''
    Format dictionnary into dataframe

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    '''

    df = pd.DataFrame(df)
    dics = ['TL:','DMF:', 'FEW:', 'Gdf:']
    df['cognates'] = df['cognates'].apply(lambda x: re.sub('\n','', x))
    df['cognates'] = df['cognates'].apply(lambda x: unicodedata.normalize("NFKD", x).split(';'))
    df['cognates'] = df['cognates'].apply(lambda x: [re.sub('\[|\]','', y.strip()) for y in x if '∅' not in y])
    df['cognates'] = df['cognates'].apply(lambda x: [w for w in x if re.match('TL:|DMF:|FEW:|Gdf:', w)])
    
    def insert_ref(ref):
        df[ref] = df['cognates'].apply(lambda x: ''.join([w for w in x if ref in w]))
        df[ref] = df[ref].apply(lambda x: str(re.sub('\d+|,|DMF|FEW|TL|Gdf|:', '', x)).strip())
        return df
    
    for item in dics:
        insert_ref(item)
    
    return df



########3 FILES
folder = "scripts\\enrich_ofrlexdev\\script_outputs\\"
manques_file = folder + "list_inconnus_et_ambigus.tsv"


forms_no_matches = []
pos_lem = {'form':[], 'lemma_pos':[], 'cognates':[]}

from_ = 63 ## testing a nb of forms
up_to = 80


manques_list = pd.read_csv(manques_file, sep='\t', encoding='utf-8', names=['forms'])
    
for word in manques_list['forms'][from_:up_to]:
    print(word)
    url = 'https://anglo-norman.net/search/'
    entries = and_entries(url, word)
    print()
    
print(f'No matches for {len(forms_no_matches)} forms (sur {len(manques_list)})')
        # save missing

fname = folder + "formes_and_{}_{}.txt".format(from_, up_to)
with open(fname, 'w+', encoding='utf-8') as f:
   for w in forms_no_matches:
       f.write(str(w+'\n')) 
       

df = pd.DataFrame(pos_lem)
formatted_entries = format_entries(df)

# formated_entries.to_csv(str(folder + ""))


    
    
