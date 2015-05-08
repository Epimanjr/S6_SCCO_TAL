#!/usr/bin/env python

### POUR EXECUTER LE FICHIER DANS NOTEPAD++ : 	C:\Python34\python.exe ex1.py
### POUR EXECUTER EN LIGNES DE COMMANDES : 		python ex1.py
 
import re
import nltk
 
import itertools
from os.path import splitext
from difflib import unified_diff, SequenceMatcher
 
import subprocess
import platform

def clear():
    subprocess.Popen( "cls" if platform.system() == "Windows" else "clear", shell=True)

clear()
 
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
	# ^(?:[01][0-9]|2[0-3]) match 1999, 2000, ...
	# ((?:19|20)\d\d)
	
	# # 85.54%
	# pattern = r'''(?x)  # (?x) to make the remainder of the regex free-spacing
	# \w+
	# '''
	
	# # 88.45%
	# pattern = r'''(?x)  # (?x) to make the remainder of the regex free-spacing
	# \w+
	# |\,
	# '''
	
	# # 85.83%
	# pattern = r'''(?x)  # (?x) to make the remainder of the regex free-spacing
	# \w+[.]?
	# |\,
	# '''
	
	# # 92.79%
	# pattern = r'''(?x)  # (?x) to make the remainder of the regex free-spacing
	# \w+(-\w+)*          # mots pleins
	# |([A-Za-z].)+       # abbreviations
	# |'s                 # appartenance
	# |[^\w\s]            # ponctuations
	# |\w'                # contractions
	# |\d+(\.\d+)?\s*%?    # pourcentages et nombres
	# '''
	
	# # 0.8641975308641975
	# pattern = r'''(?x)  # (?x) to make the remainder of the regex free-spacing
	# \$?\d+(\.\d+)?
	# |\w+[.]?
	# |\,
	# '''
	
	# # 0.865409744259847
	# pattern = r'''(?x)  # (?x) to make the remainder of the regex free-spacing
	# \$?\d+(\.\d+)?
	# |(\w+[.]?){2}
	# |\,
	# '''
	
	# # 0.9329224075416969
	# pattern = r'''(?x) # (?x) to make the remainder of the regex free-spacing
	# \$?\d+(\.\d+)?
	# |([A-Z](\.))+
	# |(\w+[-]?(\*)?){2}
	# |n\'t
	# |\"
	# |\.
	# |\,
	# '''
	
	# # 0.9484963083018189
	# pattern = r'''(?x) # (?x) to make the remainder of the regex free-spacing
	# \$?\d+(\.\d+)?
	# |([A-Z](\.))+
	# |(Mr\.|Mrs\.)
	# |(\w+[-]?(\*)?){2}
	# |(a|an)
	# |n\'t
	# |\"
	# |\.
	# |\,
	# '''
	
	# # 0.9532090354965937
	# pattern = r'''(?x) # (?x) to make the remainder of the regex free-spacing
	# \$?\d+(\.\d+)?
	# |([A-Z](\.))+
	# |(n't|'s)
	# |(Mr\.|Mrs\.)
	# |(\w+[-]?(\*)?){2}
	# |(a|an)
	# |\"
	# |\.
	# |\,
	# '''
	
	# # 0.9796726029861486
	# pattern = r'''(?x) # (?x) to make the remainder of the regex free-spacing
	# \$
	# |;
	# |%
	# |[\.]{3}
	# |\d+((,|\.)\d+)+
	# |([A-Z](\.))+
	# |(n't|'s)
	# |[A-Z][a-z]*[\.]
	# |(Mr\.|Mrs\.)
	# |((\d|\w)+[-]?(\*)?(/)?){2,}
	# |(A|An)
	# |(a|an)
	# |\"
	# |\.
	# |\,
	# '''
	
	# # 0.9796726029861486
	# pattern = r'''(?x) # (?x) to make the remainder of the regex free-spacing
	# \$
	# |;
	# |%
	# |(\w+[^n't])(n't)
	# |\d+((,|\.)\d+)+
	# |([A-Z](\.))+
	# |[A-Za-z]*(\.){3}
	# |(n't|'s)
	# |[A-Z][a-z]*[\.]
	# |(Mr\.|Mrs\.)
	# |((\d|\w)+[-]?(\*)?(/)?){2,}
	# |(A|An)
	# |(a|an)
	# |\"
	# |(\.){3}
	# |\.
	# |\,
	# '''
	
	# # 0.9796726029861486
	# pattern = r'''(?x) # (?x) to make the remainder of the regex free-spacing
	# \$
	# |;
	# |%
	# |\d+((,|\.)\d+)+
	# |([A-Z](\.))+
	# |[A-Za-z]*(\.){3}
	# |\w+[^n't]\>
	# |(n't)
	# |(n't|'s)
	# |[A-Z][a-z]*[\.]
	# |(Mr\.|Mrs\.)
	# |((\d|\w)+[-]?(\*)?(/)?){2,}
	# |(A|An)
	# |(a|an)
	# |\"
	# |(\.){3}
	# |\.
	# |\,
	# '''
	
	# # 0.981320940209134
	# pattern = r'''(?x) # (?x) to make the remainder of the regex free-spacing
	# \$
	# |;
	# |%
	# |\d+((,|\.)\d+)+
	# |([A-Z](\.))+
	# |(Co\.|Colo\.|Messrs\.|Mr\.|Mrs\.)
	# |((\d|\w)+[-]?(\*)?(/)?){2,}
	# |[A-Z][a-z]*
	# |[A-Za-z]*\.{3}
	# |\w+[^n't]\>
	# |(n't)
	# |(n't|'s)
	# |(A|An)
	# |(a|an)
	# |\"
	# |(\.){3}
	# |\.
	# |\,
	# '''
	
	# # 0.9855851016205569
	# pattern = r'''(?x) # (?x) to make the remainder of the regex free-spacing
	# \$
	# |;
	# |%
	# |\d+((,|\.)\d+)+
	# |([A-Z](\.))+
	# |(Co\.|Colo\.|Corp\.|Ltd\.|Inc\.|Messrs\.|Mr\.|Mrs\.)
	# |((\d|\w)+[-]?(\*)?(/)?){2,}
	# |[A-Z][a-z]*
	# |[A-Za-z]*(s')?(\.){3}
	# |\w+[^n't]\>
	# |(n't)
	# |(n't|'s)
	# |(A|An)
	# |(a|an)
	# |\"
	# |(\.){3}
	# |\.
	# |\,
	# '''
	
	# # 0.9915034433413827
	# pattern = r'''(?x) # (?x) to make the remainder of the regex free-spacing
	# \$
	# |;
	# |%
	# |\w+(?=n't)
	# |\d+((,|\.)\d+)+
	# |([A-Z](\.))+
	# |(Co\.|Colo\.|Corp\.|Ltd\.|Inc\.|Ill\.|Dec\.|Feb\.|Jr\.|Messrs\.|Mr\.|Mrs\.)
	# |((\d|\w)+[-]?(\*)?(/)?){2,}
	# |[A-Z][a-z]*
	# |[A-Za-z]*(s')?(\.){3}
	# |[A-Za-z]+n't\s
	# |(n't)
	# |(n't|'s)
	# |(A|An)
	# |(a|an)
	# |\"
	# |(\.){3}
	# |\.
	# |\,
	# '''
	
	# # 0.9918611930954297
	# # |\w+(?=n't)|n't|\w+(?=')|'\w+|\w+
	# pattern = r'''(?x) # (?x) to make the remainder of the regex free-spacing
	# \$
	# |;
	# |%
	# |(?=\.\.\.)
	# |(n't)
	# |\w+(?=n't)|n't|\w+(?=')|'\w+
	# |\d+((,|\.)\d+)+
	# |([A-Z](\.))+
	# |(Co\.|Colo\.|Corp\.|Ltd\.|Inc\.|Ill\.|Dec\.|Feb\.|Jr\.|Messrs\.|Mr\.|Mrs\.)
	# |((\d|\w)+[-]?(\*)?(/)?){2,}
	# |[A-Z][a-z]*
	# |[A-Za-z]*(s')?(\.){3}
	# |[A-Za-z]+n't\s
	# |('s)
	# |(A|An)
	# |(a|an)
	# |\"
	# |(\.)+
	# |\,
	# '''
	
	# # 0.9918611930954297
	# # |\w+(?=n't)|n't|\w+(?=')|'\w+|\w+
	pattern = r'''(?x) # (?x) to make the remainder of the regex free-spacing
	\$
	|;
	|%
	|(?=\.\.\.)
	|(n't)
	|\w+(?=n't)|n't|\w+(?=')|'\w+
	|\d+((,|\.)\d+)+
	|([A-Z](\.))+
	|(Co\.|Colo\.|Corp\.|Ltd\.|Inc\.|Ill\.|Dec\.|Feb\.|Jr\.|Messrs\.|Mr\.|Mrs\.)
	|((\d|\w)+[-]?(\*)?(/)?){2,}
	|[A-Z][a-z]*
	|[A-Za-z]*(s')?(\.){3}
	|[A-Za-z]+n't\s
	|('s)
	|(A|An)
	|(a|an)
	|\"
	|(\.)+
	|\,
	'''
	
	return nltk.regexp_tokenize(text,pattern)
	# return re.split(r'\s', text)
 
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
# print("Score: " + str(quality))
 
# On fait un diff entre la version officielle et la notre et on le montre
# sur la sortie.
# PROCHAINS HASHTAGS/DIESES (#) A ENLEVER POUR REAFFICHER LA SORTIE
#print_lines(unified_diff(official, our_try,\
	#fromfile='offical', tofile='our_try',\
	#lineterm='')) 

# On affiche le score
print("Score: " + str(quality))
