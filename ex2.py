#!/usr/bin/env python
 
### POUR EXECUTER LE FICHIER DANS NOTEPAD++ : 	        C:\Python34\python.exe ex2.py
### POUR EXECUTER EN LIGNES DE COMMANDES : 		python ex2.py

### PENSER A FAIRE UN : 				import ex1
### PENSER A FAIRE UN :					import tokenize
### PENSER A FAIRE UN :					from ex1 import tokenize
### TESTER EN LANCANT LA FONCTION :		        tokenize(docs[1])
 
import re
import operator

# ajouté
from ex1 import tokenize
 
# Le chemin vers le dossier contenant les fichiers de la Cranfield collection.
#data_path = "./cran"
data_path = "./ex2"
 
def read_docs():
    with open(data_path + "/cran.all.1400") as f:
        docs = re.findall(r"^\.I ([0-9]+)\n((?:.(?!\n\.I [0-9]+\n))*.)",\
                          f.read(), flags = re.M | re.S)
        id_body_pairs = map(lambda p: (int(p[0]), re.sub(r"^\.[TABW]\n", "\n",\
                                                         p[1],\
                                                         flags = re.M | re.S)),\
                            docs)
        return dict(id_body_pairs)
 
# Un dictionnaire qui donne pour un docID son contenu.
docs = read_docs()
 
def read_queries():
    with open(data_path + "/cran.qry") as f:
        queries = re.findall(r"^\.I [0-9]+\n.W\n((?:.(?!\n\.I [0-9]+\n))*.)",\
                             f.read(), flags = re.M | re.S)
        id_query_pairs = enumerate(queries, start = 1)
        return dict(id_query_pairs)
 
# Un dictionnaire qui relie les queryIDs et leurs contenus.
queries = read_queries()
 
def read_relevance():
    with open(data_path + "/cranqrel") as f:
        qd_pairs = map(lambda l: (int(l.split()[0]), int(l.split()[1])),\
                       f.readlines())
        return set(qd_pairs)
 
# Un ensemble des pairs (q,d) ou q est le queryID d'une question pour
# laquelle d est un docID d'un document qui lui est pertinent.
relevance = read_relevance()

 
# NOUVELLE FONCTION 1
# frequencies(["ab","bc","ab"]) --> { "ab" : 2, "bc" : 1 }
#def frequencies(toks):
    #freqs = {}
    #for tok in toks:
        #if tok in freqs:
            #freqs[tok] += 1
        #else:
            #freqs[tok] = 1
    #return freqs

def frequencies(toks):
    freqs = {}
    for tok in toks:
        if tok in freqs:
            freqs[tok] += 1
        else:
            freqs[tok] = 1
    #for tok in freqs:
    #        freqs[tok] = (1,freqs[tok])
    return freqs

# NOUVELLE FONCTION 2
#def build_index(docs):
#    """VOTRE CODE ICI
#
#       A partir de la collection des documents, construisez une structure
#       des donnees qui vous permettra d'identifier des documents pertinents
#       pour une question (e.g., l'index inversee qu'on a vu en classe).
#    """
#    index = {}
#
#    #for docID in docs:
#        #freqs = frequencies(tokenize(docs[docID]))
#        #...
#
#    return docs

#def build_index(docs):
#    """VOTRE CODE ICI
#
#       A partir de la collection des documents, construisez une structure
#       des donnees qui vous permettra d'identifier des documents pertinents
#       pour une question (e.g., l'index inversee qu'on a vu en classe).
#    """
#    index = {}
#
#    for docID in docs:
#        freqs = frequencies(tokenize(docs[docID]))
#        for tok in freqs: ###
#            freqs[tok] = (docID,freqs[tok]) ###
#        print(freqs) ###
#        # ID DU DOCUMENT ACTUEL
#        print(docID) ###
#        # POUR EVITER DE BLOQUER LE PROCESSUS, METTRE UNE VALEUR FAIBLE (EXEMPLE : 'if docID > 10:')
#        if docID > 10: ###
#            break ###
#    # ...
#    return docs

# Ce que retourne la fonction
# build_index(...) --> { "mot1": [(1,6), (2,3), ...] "mot2": [(1,9), (2,0), ...]}

def build_index(docs):
    """VOTRE CODE ICI

       A partir de la collection des documents, construisez une structure
       des donnees qui vous permettra d'identifier des documents pertinents
       pour une question (e.g., l'index inversee qu'on a vu en classe).
    """
    index = {}

    for docID in docs:
        freqs = frequencies(tokenize(docs[docID]))
        for tok in freqs: ###
            if tok not in index.keys():
                index[tok] = [] 
            index[tok].append((docID, freqs[tok]));
        # print(freqs) ###
        # ID DU DOCUMENT ACTUEL
        print(docID) ###
        # POUR EVITER DE BLOQUER LE PROCESSUS, METTRE UNE VALEUR FAIBLE (EXEMPLE : 'if docID > 10:')
        if docID > 2: ###
            break ###
    # ...
    print(index)
    print(index.keys())
    return index
 
def rank_docs(index, query):
    """VOTRE CODE ICI

       Retournez la serie des docIDs ordonner par leur pertinence vis-a-vis
       la question 'query'.
    """

    rank = {}

    for i in range(1, 1401):
        rank[i] = 0

    
    for mot in tokenize(query):
        
        if mot in index.keys():
            for item in index[mot]:
                rank[item[0]] += item[1]

    print(rank)
    sorted_x = sorted(rank.items(), key=operator.itemgetter(1))
    
    return sorted_x.keys()
 
 
 
def average_precision(qid, ranking):
    print(qid)
    relevant = 0
    total = 0
    precisions = []
    
    for did in ranking:
        print(did)
        total += 1
        if (qid, did) in relevance:
            relevant += 1
            precisions.append(relevant / total)
 
    return sum(precisions) / len(precisions)
 
       
 
def mean_average_precision():
    index = build_index(docs)
 
    aps = []
    for qid in queries:
        ranking = rank_docs(index, queries[qid])
        assert len(set(ranking)) == len(ranking), "Duplicates in document ranking."
        assert len(ranking) == len(docs), "Not enough (or too many) documents in ranking."
        aps.append(average_precision(qid, ranking))
        break
    return sum(aps) / len(aps)

# ajouté
#tokenize(docs[1])
 
# Imprime le MAP de l'approche implemente
print("Mean average precision: " + str(mean_average_precision()))

# NOTES
# liste = { "cle1": "valeur1", "cle2": "valeur2" }
# liste = [2,5]
# liste = (2,5)
