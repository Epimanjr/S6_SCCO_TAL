#!/usr/bin/env python

import re
import nltk

import itertools
from os.path import splitext
from difflib import unified_diff, SequenceMatcher


def expand(token):
    """Remplace des (\/) avec des (/) dans la tokenisation officielle pour etre
       en harmonie avec le texte brut.
    """
    return re.sub(r"``|''", '"', \
           re.sub(r'\\/', '/', \
           token))

def normalize(words):
    """Sert a normaliser la version officielle tokenisee pour qu'elle ressemble
       plus au text qu'on trouve dans les fichiers bruts.
    """
    expanded = map(expand, words)
    filtered = filter(lambda word: '*' not in word and word != '0', expanded)
    return list(filtered)

def print_lines(lines):
    """Imprime une liste, un element par une ligne. Utile pour imprimer soit
       votre liste des tokens ou la liste des differences, ligne par ligne.
    """
    for line in lines:
        print(line)

# Le corpus qu'on utilisera, le Penn Treebank.
corpus = nltk.corpus.treebank
corpus_raw = nltk.corpus.treebank_raw

def raw_version(fileid):
    """A partir d'un fileid dans le treebank, ca nous donne la version raw
       (brute/crue) de sa contenu.
    """
    contents = corpus_raw.raw(splitext(fileid)[0])
    return contents[8:]

def raw_versions(fileids):
    """Version generalisee de raw_version qui cherche la version brute des
       plusieurs extraits (fileids) et les colle ensemble.
    """
    return ''.join(itertools.chain(map(raw_version, fileids)))


def tokenize(text):
    """VOTRE CODE ICI!

       Voici votre fonction de tokenisation. Elle devrait transformer le
       texte brut (represente en tant qu'un chaine des caracteres) en liste
       des tokens individuels.
    """
    pattern = r'''(?x) # necessaire pour rendre des espaces pas importants!
                  \w+  # les mots
                | ,    # comma'''
    tokens = nltk.regexp_tokenize(text, pattern)
    return tokens



# Les identifiants des fichiers sur lesquels on veut tester notre
# tokeniseur. Pour retrouver tous les identifiants possible, lancer
# nltk.corpus.treebank.fileids().
# Maintenant, on utilise que les 20 premiers extraits pour que l'experience
# prends moins du temps.
fileids = nltk.corpus.treebank.fileids()[:20]

# La tokenisation officielle et celle fait de facon automatique avec notre
# algorithme.
official = normalize(corpus.words(fileids))
our_try = tokenize(raw_versions(fileids))

# On donne un score qui montre la qualite de notre tokenisation.
quality = SequenceMatcher(None, official, our_try).ratio()
print("Score: " + str(quality))

# On fait un diff entre la version officielle et la notre et on le montre
# sur la sortie.
print_lines(unified_diff(official, our_try,\
                         fromfile='official', tofile='our_try',\
                         lineterm='')) 
