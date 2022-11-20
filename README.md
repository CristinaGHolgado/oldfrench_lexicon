# Enrichissement d'un lexique morphosyntaxique pour le français médiéval
This repository contains a set of ressources used to enrich a morphosyntactic lexicon for old French ([OFrLex](https://aclanthology.org/2020.lrec-1.393.pdf)) in order to improve the performance of a syntactic parser and improve its the lexical coverage. These ressources include lexicons, scripts and linguistic annotation tools for old French.

It is part of the [ANR PROFITEROLE](http://ihrim.ens-lyon.fr/recherche/contrats/article/anr-profiterole-processing-old-french-instrumented-texts-for-the-representation) projet. This work has been conducted by Cristina Garcia Holgado and Mathilde Reignault.  


## :black_square_button: Construction d'un inventaire de formes
**Description**  
Construction d'un inventaire de formes à partir du corpus gold BFMGOLDLEM et le lexique OFrLex (dev) afin d'augmenter la couverture du lexique (nouvelles entrées).  

#### :file_folder: Ressources
Corpus [BFMGOLDLEM](https://hal.archives-ouvertes.fr/hal-03265897/document): 21 textes (431 144 formes étiquetées et lemmatisées) en format CoNNL-U. Il inclut les informations suivantes: forme, lemme, étiquette UD, étiquette Cattex 2009, traits morphologiques (quelques formes) et source/idx.
Lexique [OFrLex](https://aclanthology.org/2020.lrec-1.393/): Lexique morpho-syntaxique annoté selon les conventions Alexina. Il est composé d'entrées lexicales de différentes sources complétées par leurs fonctions syntaxiques, leurs réalisations et leurs redistributions. Le lexique est composé d'entrées intensionnelles (.ilex) et extensionnelles (.lex) :

*Intensional lexicon* 

||||
|---|---|---|
aamer___746696__1|v-er|100;Lemma;v;<Suj:cln\\sn,Obj:(cla\\sn)>;upos=VERB,cat=v;%actif

*Extensional lexicon* (lexique utilisé)

||||||||
|---|---|---|---|---|---|---|
aamer|100|v|\[pred="aamer___746696__1__1<Suj:cln\\sn,Obj:(cla|sn)>",@pers,cat=v,upos=VERB,@inf.std\]|aamer___746696__1__1|Default|inf.std|%actif|v-er  

[OfrLex](https://hal.inria.fr/inria-00521242/document), [Alexina](https://aclanthology.org/2020.lrec-1.393.pdf)  

### :heavy_minus_sign: Instructions pour l'exécution du code
**Inventoire**
*inventory_builder_bfm.py*  
` [-in CORPUS -out FILENAME -ignore IGNORE FILES] `

*inventory_builder_ofr.py*  
` [-in CORPUS -out FILENAME -ignore IGNORE FILES -cattex CATTEX IF AVALIABLE -fiter_pos IGNORE POS] `

**Fusion d'entrées**  
*scripts/map_ofrlex_bfmgoldlem.ipynb*  

```
bfm_inventory = "data\\profiterole_bfmgold_inventoire.tsv"
ofrlex_inventory = "data\\ofrlexdev_inventory.tsv
```

#### Fichier en sortie
*BFMGOLDLEM*

|  fpl | forme  | lemme  |  pos (cattex) | feats_bfm  |  lemma_src |  file_src_bfm | occ_bfm |  n |
|---|---|---|---|---|---|---|---|---|
 confondemant_confondement_noun | confondemant | confondement | NOMcom | _ | DECT | CligesKu | 1 | _ 
 confondent_confondre_verb | confondent | confondre | VERcjg | VerbForm=Fin | DECT | CligesKu | 2 | _ 
 confondoit_confondre_verb | confondoit | confondre | VERcjg | VerbForm=Fin | DMF | SGenPr1 | 1 | _ 

*OFrLex* (.lex)

|form|pos|traits|lemme|file_src|raw_lemme|inconnu|upos|no_upos|
|---|---|---|---|---|---|---|---|---|
 aates | adj | [pred="aate___203__1<Suj:cln|sn>",@pers,cat=adj,upos=ADJ,@sg.nom.masc] | aate___203__1 | ..\ofrlex-dev\ADJ.lex | aate | 0 | ADJ | 0 
 abaant | adj | [pred="abeant___211__1<Suj:cln|sn>",@pers,cat=adj,upos=ADJ] | abeant___211__1 | ..\ofrlex-dev\ADJ.lex | abeant | 0 | ADJ | 0 
 abaeux | adj | [pred="abaeuz___204__1<Suj:cln|sn>",@pers,cat=adj,upos=ADJ] | abaeuz___204__1 | ..\ofrlex-dev\ADJ.lex | abaeuz | 0 | ADJ | 0 

- - - -



## :black_square_button: Lemmatisation des formes non renseignés dans OFrLex
**Description**  
Ajout de lemmes et d'informations morphosyntaxiques pour les entrées manquantes du lexique

#### :file_folder: Ressources
LGeRM [desc, src, utilisation]  
BFMGOLDLEM []  
FROLEX [descr, src]  
[frolex-03.tsv](https://github.com/sheiden/Medieval-French-Language-Toolkit/releases/download/v3.0/Medieval-French-Language-Toolkit.3.0.zip) dernière version (2020)

### :heavy_minus_sign: Instructions pour l'exécution du code
- Lemmatisation et alignement d’entrées
` [] `
- Génération de variants pour les formes qui n'ont pu être alignés (graphie)
` [] `
- Requêtes automatiques dans des dictionnaires externes
` [] `

#### Fichiers en sortie
[]

- - - -

## :black_square_button: Recherche et extraction de préfixes
**Description**  
### :heavy_minus_sign: Instructions pour l'exécution du code
` [] `

- - - -

## :black_square_button: Recherche de variants graphiques dans les lemmes OFrLex
**Description**  
Réduire le nombre de lemmes permettrait, d’une part, de réduire le nombre d’entrées (ce qui aurait pour effet de réduire l’ambiguïté lexicale et représenterait une diminution du temps de calcul de l’analyse syntaxique), et, d’autre part, de proposer une meilleure lemmatisation au terme de l’analyse syntaxique avec MetaMOF.
#### :file_folder: Ressources
[]

### :heavy_minus_sign: Instructions pour l'exécution du code
` [] `

### Résultats 
[]


- - - -

## :white_square_button: Statistiques sur les nouvelles entrées ajoutées dans OFrLex
[]
#### Fichiers en sortie
[]
