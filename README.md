# Enrichissement d'un lexique morphosyntaxique pour le français médiéval
This repository contains a set of ressources used to enrich a morphosyntactic lexicon for old French ([OFrLex](https://aclanthology.org/2020.lrec-1.393.pdf)) in order to improve the performance of a syntactic parser and improve its the lexical coverage. These ressources include lexicons, scripts and linguistic annotation tools for old French.

It is part of the [ANR PROFITEROLE](http://ihrim.ens-lyon.fr/recherche/contrats/article/anr-profiterole-processing-old-french-instrumented-texts-for-the-representation) projet. This work has been conducted by Cristina Garcia Holgado and Mathilde Reignault.  


## :black_square_button: 1. Construction d'un inventaire de formes
### Description  
Construction d'un inventaire de formes à partir du corpus gold BFMGOLDLEM et le lexique OFrLex (dev) afin d'augmenter la couverture du lexique (nouvelles entrées).  

### :file_folder: Ressources

`/scripts/inventaires`  

**- Corpus [BFMGOLDLEM](https://hal.archives-ouvertes.fr/hal-03265897/document) [source dans la Base de Français Médiéval](http://portal.textometrie.org/bfm/?command=metadata&path=/BFM2019)**: 21 textes (431 144 formes étiquetées et lemmatisées) en format CoNNL-U. Il inclut les informations suivantes: forme, lemme, étiquette UD, étiquette Cattex 2009, traits morphologiques (quelques formes) et source/idx.  Des nouveaux textes ont été ajoutés postérieurement. Accès au corpus: [corpus BFMGOLDLEM](https://sharedocs.huma-num.fr/wl/?id=ucuocmUCpdSxUJCgCliVlHCBEusoiIfk)  

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

Structure du fichier en sortie:  

|  fpl | forme  | lemme  |  pos (cattex) | feats_bfm  |  lemma_src |  file_src_bfm | occ_bfm |  n |
|---|---|---|---|---|---|---|---|---|
 confondemant_confondement_noun | confondemant | confondement | NOMcom | _ | DECT | CligesKu | 1 | _ 
 confondent_confondre_verb | confondent | confondre | VERcjg | VerbForm=Fin | DECT | CligesKu | 2 | _ 
 confondoit_confondre_verb | confondoit | confondre | VERcjg | VerbForm=Fin | DMF | SGenPr1 | 1 | _ 

*inventory_builder_ofr.py*  
` [-in CORPUS -out FILENAME -ignore IGNORE FILES -cattex CATTEX IF AVALIABLE -fiter_pos IGNORE POS] `  

Structure du fichier en sortie:  

|form|pos|traits|lemme|file_src|raw_lemme|inconnu|upos|no_upos|
|---|---|---|---|---|---|---|---|---|
 aates | adj | [pred="aate___203__1<Suj:cln|sn>",@pers,cat=adj,upos=ADJ,@sg.nom.masc] | aate___203__1 | ..\ofrlex-dev\ADJ.lex | aate | 0 | ADJ | 0 
 abaant | adj | [pred="abeant___211__1<Suj:cln|sn>",@pers,cat=adj,upos=ADJ] | abeant___211__1 | ..\ofrlex-dev\ADJ.lex | abeant | 0 | ADJ | 0 
 abaeux | adj | [pred="abaeuz___204__1<Suj:cln|sn>",@pers,cat=adj,upos=ADJ] | abaeuz___204__1 | ..\ofrlex-dev\ADJ.lex | abaeuz | 0 | ADJ | 0 

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

[Accès aux inventaires et formes BFMGOLDLEM absentes dans OFrLex](https://sharedocs.huma-num.fr/wl/?id=MZnR1ntysZNzpgTqJNlMuR69C04Ug8zY)




- - - -
- - - -




## :black_square_button: 2. Lemmatisation des formes non renseignés dans OFrLex
### **Description**  

Après avoir constaté que de nombreuses formes du corpus PROFITEROLE (32.485 formes) étaient absentes dans le lexique OFrLex-dev, on leur a attribué des informations morphologiques en utilisant divers ressources et stratégies pour le tri des différentes informations.

** Dans une étape postérieure, ces formes ont été lematisées en contexte (voir [section 5](#5.-Annotation-de-formes-manquantes-en-contexte))

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


### :file_folder: Ressources  

`scripts/manques`  

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

Il inclut la source à partir de laquelle nous avons récupéré les informations morphologiques. L'ensemble de fichiers en sortie peuvent être consultés dans [FORMES MANQUANTES ANNOTES PAR POS](https://github.com/CristinaGHolgado/oldfrench_lexicon/tree/master/scripts/manques/fichiers/premier_alignement)

Et un seul fichier avec la liste de formes qui n'ont pas été trouvées. Vous puvez le trouver dans [LISTE DE FORMES NON TROUVEES PREMIER ALIGNEMENT](https://github.com/CristinaGHolgado/oldfrench_lexicon/blob/master/scripts/manques/fichiers/premier_alignement/formes%20manquantes%20premier%20alignement.csv)


- **Génération de variants pour les formes qui n'ont pu être alignés (aucune correspondance dans les ressources)**  

On génére les variants avec ` [generate_variants.py] `  en utilisant la liste de formes qui n'ont pas été trouvées à partir la commande suivante:

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

Ensuite, on refait l'alignement avec le script précedent (`[mode = "variants"]`).  Pareillement, il retourne les formes annotées et une liste avec les formes qui n'ont pas été trouvées avec cette stratégie. [LISTE DE FORMES NON TROUVEES DEUXIEME ALIGNEMENT](https://github.com/CristinaGHolgado/oldfrench_lexicon/blob/master/scripts/manques/fichiers/deuxieme_alignement/missing_forms_from_variants.csv), [FORMES MANQUANTES ANNOTES PAR POS DEUXIEME ALIGNEMENT](https://github.com/CristinaGHolgado/oldfrench_lexicon/tree/master/scripts/manques/fichiers/deuxieme_alignement)


- **Requêtes automatiques dans des dictionnaires externes**  
  
` [request_and.py] `  
  
Avec ce script, nous récupérons les entrées du dictionnaire correspondant au reste des formes manquantes en précisant le chemin vers les dernières formes manquantes. Pour éviter les limites de requête, nous pouvons extraire les entrées par chunks de 100 formes `[from_="0"]`, `[up_to= "500"]`. Structure des fichiers en sortie:

|form|lemma_pos|cognates|TL:|DMF:|FEW:|Gdf:|
|---|---|---|---|---|---|---|
chaitivíer|chaitivier \(s.xii2\)\__s.|\['FEW: 2/i,330a captivus', 'Gdf: 2,38b chaitivier', 'TL: 2,173 chaitivier'\]|chaitivier| captivus|chaitivier
chelidonius|celidoine \(s.xii1/3\)\__s.|\['FEW: 2/i,634a chelidonia', 'DMF: chélidoine'\]||chélidoine|chelidonia|
clamíve|clamif \(s.xii\)\__s.|\['FEW: 2/i,730a clamare', 'TL: 2,460 clamif', 'DMF: clamif'\]|clamif|clamif|clamare||




- - - -
- - - -

## :black_square_button: 3. Recherche et extraction de préfixes
### **Description**  

Recherche de formes préfixées dans les formes manquantes à partir d’une liste de préfixes de départ. Nous avons sélectionné les formes dans les catégories ADV, ADJ, VER et NOM. Seulement les formes avec une longueur supérieure à 3 caractères (et 3 également pour le radical) ont été retenues. Pour chaque préfixe dans la liste, nous avons collecté toutes les formes possibles commençant par ces préfixes et ensuite, nous avons cherché, à partir d'une segmentation sur le préfixe, si le radical est attesté dans le lexique. Par exemple: 

[prefixe] sor - [forme trouvé] sorcroissant - [radical attesté] - croissant - [lemme associé] - croissir___750428_… - [POS] v  

### **Ressources**  
- [Liste prédéfinie de préfixes](https://github.com/CristinaGHolgado/oldfrench_lexicon/blob/master/scripts/prefixes/fichiers/prefixes.txt)  
- [Liste de formes manquantes](https://github.com/CristinaGHolgado/oldfrench_lexicon/blob/master/scripts/manques/fichiers/liste_manques.txt)  
- [Inventaire d'entrées OFrLex](https://sharedocs.huma-num.fr/wl/?id=MZnR1ntysZNzpgTqJNlMuR69C04Ug8zY)  

### :heavy_minus_sign: Instructions pour l'exécution du code  
` [find_prefixes.py] `  

Préiser les fichiers dans:  

```
folder = "enrich_ofrlexdev\\data\\source_data\\"
manques_f = folder + "liste_manques.txt"
ofrlex = folder + "inventaire_ofrlex.tsv"
prefixes = folder + "prefixes.txt"
```

|prefixe|word|root|ofr_root_form|ofr_root_lemma|ofr_root_pos|lemma_def|
|---|---|---|---|---|---|---|
contre|contredeïst|deïst|deïst|dire___751970__1__1|v|_
contre|contrediroient|diroient|diroient|dire___751970__1__1|v|contredire
des|deshonnestement|honnestement|honnestement|onestement___9076__1|adv|déshonnêtement
des|deshonneur|honneur|honneur|honneur___99999__1|nc|déshonneur
re|revenons|venons|venons|venir___60461__1__3|v|revenir
re|revenra|venra|venra|venir___60461__1__3|v|revenir


[Accéder à la liste de possibles formes préfixées](https://github.com/CristinaGHolgado/oldfrench_lexicon/blob/master/scripts/prefixes/fichiers/prefixes_stemmer1.csv)

- - - -

## :black_square_button: 4. Recherche de variants graphiques dans les lemmes OFrLex

### **Description**  
Réduire le nombre de lemmes permettrait, d’une part, de réduire le nombre d’entrées (ce qui aurait pour effet de réduire l’ambiguïté lexicale et représenterait une diminution du temps de calcul de l’analyse syntaxique), et, d’autre part, de proposer une meilleure lemmatisation au terme de l’analyse syntaxique avec MetaMOF.

### :file_folder: Ressources
- [Fichiers .md du lexique]()
- [Formes manquantes annotées]()

### :heavy_minus_sign: Instructions pour l'exécution du code  
` [distances_lemma.py] `

Fournir le fichier des formes manquantes annotées pour recherches les variants avant l'ajout au lexique, ou les fichiers `.md` du  OFrLex pour identifier les variants présents dans le lexique.

```
file = 'scripts/manques/fichiers/premier_alignement/v2_conj_manques_annote.tsv'
```

Il retourne un fichier pour chaque partie du discours dont nous trouvons plusieurs lemmes (e.g. desus (lemme TL) un lieu de dessus (lemme DMF)). 

|lemme|prox_lemme|var|
|---|---|---|
après_PRE|['apres_PRE']|    
delez_PRE|['dalez_PRE']| 
desor_PRE|['desoz_PRE']| 
dessous_PRE|['dessus_PRE']| 
desus_PRE|['dessus_PRE']|
deçà_PRE|['delà_PRE']| 
en+le_PRE|['en.le_PRE']| 
entre_PRE|['estre_PRE']| 
jusque_PRE|['jesque_PRE']|


## 5. Annotation de formes manquantes en contexte

Nous avons entraîné un modèle RNN pour l’annotation en POS et la lemmatisation afin de renseigner les formes manquantes (OFrLex) de manière contextualisée dans le corpus Profiterole. Cela permet de renseigner les formes inconnues pour les lexiques utilisés précédemment et, notamment, de les renseigner dans leur contexte d’apparition. Aussi, de comparer les étiquettes et les lemmes fournis par les ressources lexicales avec ceux appris par le modèle. 

### Ressources et outils

- [NLP Pie](https://pypi.org/project/nlp-pie/): Outil de lemmatisation et d'annotation morphosyntaxique conçu pour les langues historiques et des langues à forte variation.

- [Corpus Profiterole](): Ils font partie du découpage Train/Dev/Test (fichiers utilisés à l'entraînement, dévelopment et test du modèle).

### Lemmatisation des textes et alignement des informations morphosyntaxiques

Utiliser le [notebook](https://colab.research.google.com/drive/1_GsqMhBNCCmq5wByosM5bRCc1SEeT4tA?usp=sharing) pour charger les textes utilisés et récupérer les prédictions.

On peut sélectionner les don´´es fournis par défault dans le dictionnaire:

```
## Download traning/dev/test data
!pip install wget
import wget

urls= {'train_data':'https://sharedocs.huma-num.fr/wl/?id=LVfEryNatUmIOSrcv79qLt7Vh9xQcP5G&fmode=open',
       'dev_data': 'https://sharedocs.huma-num.fr/wl/?id=NP9ubphyOqW1kHf5E6EKdq6F4USxFLC6&fmode=open',
       'test_data': 'https://sharedocs.huma-num.fr/wl/?id=5bNmeXMzMVVOR11huaOx6aiYFVzRsRNf&fmode=open'}

for k, v in urls.items():
  print('Downloading', k)
  wget.download(v)
```

Ou les télécharger directement dans `scripts/lemmatisation/train-dev-test-data`

Pie entraînera deux modèles, où un pour les **POS** et un pour les **lemmes**. Nous pouvons les fusionner en utilisant le script `merge_lemma_pos_pie.py`. Ce script va extraire les formes manquantes annotés dans les prédictions que nous pouvons trouver dans [scripts/lemmatisation/lemmatisation_manques_Pie.tsv](https://github.com/CristinaGHolgado/oldfrench_lexicon/blob/master/scripts/lemmatisation/manques_Pie.tsv)


- - - -
- - - -
- - - -
