# Enrichissement d'un lexique morphosyntaxique pour le français médiéval
This repository contains a set of ressources used to enrich a morphosyntactic lexicon for old French ([OFrLex](https://aclanthology.org/2020.lrec-1.393.pdf)) in order to improve the performance of a syntactic parser and improve its the lexical coverage. These ressources include lexicons, scripts and linguistic annotation tools for old French.

It is part of the [ANR PROFITEROLE](http://ihrim.ens-lyon.fr/recherche/contrats/article/anr-profiterole-processing-old-french-instrumented-texts-for-the-representation) projet. This work has been conducted by Cristina Garcia Holgado and Mathilde Reignault.  


## :black_square_button: Construction d'un inventaire de formes
**Description**  
Construction d'un inventaire de formes à partir du corpus gold BFMGOLDLEM et le lexique OFrLex (dev) afin d'augmenter la couverture du lexique (nouvelles entrées).  

#### :file_folder: Ressources
**- Corpus [BFMGOLDLEM](https://hal.archives-ouvertes.fr/hal-03265897/document) [source dans la Base de Français Médiéval](http://portal.textometrie.org/bfm/?command=metadata&path=/BFM2019](http://portal.textometrie.org/bfm/?command=metadata&path=/BFM2019)**: 21 textes (431 144 formes étiquetées et lemmatisées) en format CoNNL-U. Il inclut les informations suivantes: forme, lemme, étiquette UD, étiquette Cattex 2009, traits morphologiques (quelques formes) et source/idx.  Des nouveaux textes ont été ajoutés postérieurement. Accès au corpus: [corpus BFMGOLDLEM](https://sharedocs.huma-num.fr/wl/?id=ucuocmUCpdSxUJCgCliVlHCBEusoiIfk)  

**- Lexique [OFrLex](https://aclanthology.org/2020.lrec-1.393/)**: Lexique morpho-syntaxique annoté selon les conventions Alexina. Il est composé d'entrées lexicales de différentes sources complétées par leurs fonctions syntaxiques, leurs réalisations et leurs redistributions. Le lexique est composé d'entrées intensionnelles (.ilex) et extensionnelles (.lex) :  

*Intensional lexicon* 

||||
|---|---|---|
aamer___746696__1|v-er|100;Lemma;v;<Suj:cln\\sn,Obj:(cla\\sn)>;upos=VERB,cat=v;%actif

*Extensional lexicon* (lexique utilisé)

||||||||
|---|---|---|---|---|---|---|
aamer|100|v|\[pred="aamer___746696__1__1<Suj:cln\\sn,Obj:(cla|sn)>",@pers,cat=v,upos=VERB,@inf.std\]|aamer___746696__1__1|Default|inf.std|%actif|v-er  

Accès au lexique (dernière version) [OFrLex dev](https://gitlab.inria.fr/almanach/alexina/ofrlex/-/tree/86f157bb1c2d90c8fb58bb07398ae42d1c27dcc2). La version précédente utilisé dans ce travail est disponible dans [OFrLex old](https://gitlab.inria.fr/almanach/alexina/ofrlex)  

Informations plus détaillées à propos des ressources: [OFrLex](https://hal.inria.fr/inria-00521242/document), [Alexina](https://aclanthology.org/2020.lrec-1.393.pdf)  

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

On peut fusionner les entrées BFM-OFrLex par forme-lemme (fl), forme-pos(fp) et forme-lemme-pos(flp).  
```
merge_by_col = 'flp'
```

On obtient les formes en commun et/ou absentes (formes BFMGOLDLEM non renseignées dans OFrLex):  

|forme|lemme|UPOS|traits ofrlex|||||source ofrlex|
|---|---|---|---|---|---|---|---|---|
Abbeville*|Abeville*|_ | _ |Abeville|NOMpro | _ | _ | _ |
Abbeye___54353__1|Abbeye|PROPN  | \[pred="Abbeye___54353__1<Suj\:(sn)>",upos=PROPN,cat=np\] | _ | _ | _ |0.0 | ..\ofrlex-dev\PROPN.lex  
  
Formes BFMGOLD absentes dans OFrLex(*) triées par ordre alphabétique du lemme, ce qui permet de gérer (vérification manuelle) plus facilement les cas où l'on trouve des variants dans les lemmes:  
e.g. 
```
[...] Abbeville NOMpro  
[...] Abeville NOMpro  
[...] Abel NOMpro  
[...] Abels NOMpro  
[...] Abevile NOMpro  
...  
```


#### Fichiers en sortie
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

*Fusion d'entrées*


[Accès aux inventaires et formes BFMGOLDLEM absentes dans OFrLex](https://sharedocs.huma-num.fr/wl/?id=MZnR1ntysZNzpgTqJNlMuR69C04Ug8zY)
- - - -



## :black_square_button: Lemmatisation des formes non renseignés dans OFrLex
**Description**  

Après avoir constaté que de nombreuses formes du corpus PROFITEROLE (32.485 formes) étaient absentes dans le lexique OFrLex-dev, on leur a attribué des informations morphologiques en utilisant divers ressources et stratégies pour le tri des différentes informations.

Stratégies:  
**(1)** Lemmatisation avec divers outils et ressources (LGeRM, BFMGOLDLEM, FROLEX) et tri selon la priorité accordée à chaque ressource:  

1. BFMGOLDLEM (inventaire): priorité à un corpus gold pour le français médiéval  
2. LGeRM: puis, propositions de la lemmatisation par LGeRM, mais l'outil est notamment conçu pour le Moyen Français  
3. FROLEX: lexique qui fournit uniquement lemme/POS  

**(2)** Génération de variants graphiques possibles pour les formes qui n'ont pu être alignés (match)  
Cette strátegie permet de rapprocher les formes qui n'ont pas été trouvées pendant l'étape précedente.  
E.g.:
```
meyns (forme non trouvée)   meins(variant généré)   moins(forme trouvée)    ADV int_quantif quantif
````

**(3)** Requêtes automatiques dans un dictionnaire externe  
Pour les formes restantes qui n'ont pu être renseignées, on effectue des requêtes automatiques dans le dictionnaire ([dictionnaire anglo-normand](https://anglo-norman.net/entry/)) et on extrait les informations qui sont fournies pour cette forme.


#### :file_folder: Ressources
- [LGeRM](http://stella.atilf.fr/LGeRM/plateforme/): plateforme, lexique morphologique et outil de lemmatisation pour le moyen français et le français médieval. Il privilégie les lemmes du DMF ([Dictionnaire du Moyen Français](http://zeus.atilf.fr/dmf/)). Pour accèder à l'outil et au lexique en local, [contactez l'auteur](http://stella.atilf.fr/scripts/mep.exe?CRITERE=ACCUEIL_LGERM_CONTACT;ISIS=isis_mep_lgerm.txt;ONGLET=SiteLGeRM;OO1=1;OO2=1;s=s0f2729c4)  
- [BFMGOLDLEM](http://portal.textometrie.org/bfm/?command=metadata&path=/BFM2019)  
  
- [FROLEX](https://groupes.renater.fr/wiki/palafra/public/lexique_fro): lexique qui rassemble des formes en français médiéval provenant de diverses sources. Il fournit leur étiquette Cattex ([Cattex 2009](http://bfm.ens-lyon.fr/IMG/pdf/Cattex2009_manuel_2.0.pdf)). Ce lexique est disponible dans [frolex-03.tsv](https://github.com/sheiden/Medieval-French-Language-Toolkit/releases/download/v3.0/Medieval-French-Language-Toolkit.3.0.zip) dernière version (2020)

### :heavy_minus_sign: Instructions pour l'exécution du code
- **Lemmatisation et alignement d’entrées dans les différents resources**  
`[align_manques.py]`
Fichiers nécessaires

```
folder = 'scripts\\enrich_ofrlexdev\\' DOSSIER DE TRAVAIL
*manques_lemmatisees = folder + "MANQUES LEMMATISÉES" # Formes manquantes lemmatisées avec lgerm
inventory_bfm = folder + 'ressources\\' + INVENTAIRE BFMGOLDLEM # Inventaire du corpus BFMGOLDLEM
frolex_f = folder + LEXIQUE FROLEX # Lexique Frolex
lexique_lgerm = "lgerm\\lexiques\\graphies_MF.txt" # Lexique LGeRM
manques_file = folder + LISTE DE FORMES MANQUANTES # Manques

* optionnel
```

Mode d'annotation:  
Si "manques", on fournit des annotations pour les formes manquantes (première étape)  
Si "variants", on fournit des annotations pour les variants générés dans `[generate_variants.py]`

```
mode = MODE
```

Ce script retourne un fichier (un fichier par POS) structuré de la manière suivante:  

|form | def_pos | def_lemma | def_morph | source | UPOS | pos|
|---|---|---|---|---|---|---|
abiság | NCO | aviage | masc | LGERM | NCO | NCO
abitation | NCO | habitation | fem | FROLEX | NCO | NCO
abiteür | NCO | habiteur | _ | BFMGOLDLEM | NCO | NCO

Il inclut la source à partir de laquelle nous avons récupéré les informations morphologiques. L'ensemble de fichiers en sortie peuvent être consultés dans [FORMES MANQUANTES ANNOTES PAR POS](https://sharedocs.huma-num.fr/wl/?id=uOuu3n86J089lcBB0sk5qASUO4iChe4R)

Et un seul fichier avec la liste de formes qui n'ont pas été trouvées. Vous puvez le trouver dans [LISTE DE FORMES NON TROUVEES PREMIER ALIGNEMENT]()


- **Génération de variants pour les formes qui n'ont pu être alignés (aucune correspondance dans les ressources)**  

On génére les variants avec ` [generate_variants.py] `  en utilisant la liste de formes qui n'ont pas été trouvées à partir la commande:

```
-in LISTE_FORMES  -sep \t -out SAVE_TO_PATH
```
  
qui retourne:
  
|source_mot|variant|id|
|---|---|---|
malfaitúrs|malfaitúrs|461
malfaitúrs|malfaiturs|461
malvesyve|malvesyve|462
malvesyve|malvesive|462
marsopye|marsopye|463
marsopye|marsopie|463

Ensuite, on refait l'alignement avec le script précedent (`[mode = "variants"]`).  Pareillement, il retourne les formes annotées et une liste avec les formes qui n'ont pas été trouvées avec cette stratégie.


- **Requêtes automatiques dans des dictionnaires externes**
` [] `


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
