#!/usr/bin/env python
 
import re
# Utile pour les fonctions de tri de listes
import operator

# On importe la fonction tokenize du TP précédent.
from tokenizer import tokenize
 
# Le chemin vers le dossier contenant les fichiers de la Cranfield collection.
data_path = "./cran"
 
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

def tokenize(text):
    return text.split()

# frequencies(["ab", "bc", "ab"]) = { "ab" : 2, "bc" : 1 }

def frequencies(toks):
    freqs = {}
    for tok in toks:
        if tok in freqs:
            freqs[tok] += 1
        else:
            freqs[tok] = 1
    return freqs

# build_index(...) = { "slipstream": [(1,6), (16,3), ...],
#                      "configuration": [(1,1), ...],
#                      ... }

def build_index(docs):
    """VOTRE CODE ICI

       A partir de la collection des documents, construisez une structure
       des donnees qui vous permettra d'identifier des documents pertinents
       pour une question (e.g., l'index inversee qu'on a vu en classe).
    """
    # Initialize index (empty list)
    index = {}

    # Loop for all documents: 1400
    for docID in docs:
        # Get frequencies for document number docID
        freqs = frequencies(tokenize(docs[docID]))
        # For each word in this document
        for word in freqs:
            # If word is not in our index
            if word not in index.keys():
                # Add a new entry
                index[word] = []
            # In all case, add a new value
            index[word].append((docID, freqs[word]))
        #if docID > 10:
        #    break

    return index
 
def rank_docs(index, query):
    """VOTRE CODE ICI

       Retournez la serie des docIDs ordonner par leur pertinence vis-a-vis
       la question 'query'.
    """
    # Initialize new list
    ranking = {}
    for i in range(1, 1401):
        ranking[i] = 0

    # For each word in query
    for word in tokenize(query):
        # If we have this word in our index
        if word in index.keys():
            # For each document in which we can find the word
            for item in index[word]:
                # Increase the score
                ranking[item[0]] += item[1]

    # Sort the list with score
    sorted_ranking = sorted(ranking.items(), key=operator.itemgetter(1), reverse=True)

    ranking = []
    for couple in sorted_ranking:
        ranking.append(couple[0])
        
    return ranking



def average_precision(qid, ranking):
    relevant = 0
    total = 0
    precisions = []
    
    for did in ranking:
        total += 1
        if (qid, did) in relevance:
            relevant += 1
            precisions.append(float(relevant) / float(total))

    return float(sum(precisions)) / float(len(precisions))

       

def mean_average_precision():
    index = build_index(docs)
    aps = []

    for qid in queries:
        ranking = rank_docs(index, queries[qid])
        assert len(set(ranking)) == len(ranking), "Duplicates in document ranking."
        assert len(ranking) == len(docs), "Not enough (or too many) documents in ranking."
        aps.append(average_precision(qid, ranking))

    return float(sum(aps)) / float(len(aps))

# Imprime le MAP de l'approche implemente
print("Mean average precision: " + str(mean_average_precision()))

