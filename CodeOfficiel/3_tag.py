#!/usr/bin/env python

def train_model(corpus):
    """VOTRE CODE ICI

       Cette fonction devrait servir pour extraire des statistiques a
       partir du corpus des donnees d'entrainement. Le resultat pourrait
       avoir forme d'une representation d'un modele de Markov cache (HMM),
       cette valeur sera transmise au fonction `tag_sentence` en tant que
       l'argument `model`.

       `corpus` est une liste des phrases ou chaque phrase est une liste
       des pairs d'un mot et de sa étiquette (i.e. [[... for (word, tag) in
       sentence] for sentence in corpus]).
    """

    return None

def tag_sentence(sent, model):
    """VOTRE CODE ICI

       Cette fonction a pour but de etiquetter la phrase `sent` avec des
       part of speech. `sent` est representee sous forme d'une liste des
       mots. Le resultats devrait avoir forme d'une liste des pairs dont le
       premier element est un mot du phrase et le deuxieme element et sa
       etiquette.
    """

    return [(word, "NN") for word in sent]



# EVALUATION

import nltk
from nltk.corpus import treebank

training_size = 150
development_size = 25

training_data = list(treebank.tagged_sents(treebank.fileids()[:training_size]))
development_data = list(treebank.tagged_sents(treebank.fileids()[training_size : training_size + development_size]))

def flatten(lol):
    """A partir d'une liste des listes des valeurs, produit une liste des
       simple valeurs en concatenant les listes."""
    return [value for l in lol for value in l]

def filter_text(corpus):
    return [[(word, tag) for (word, tag) in sent if tag != '-NONE-'] \
            for sent in corpus]

def measure_accuracy():
    """Mesure l'efficacite de votre approche en comptant la proportion
       des mots pour lesquels la bonne etiquette ete recuperee par votre
       algorithme."""

    model = train_model(filter_text(training_data))
    filtered_data = filter_text(development_data)
    scrubbed_data = [[word for (word, tag) in sent] \
                     for sent in filtered_data]
    tagged_data = [tag_sentence(sent, model) for sent in scrubbed_data]
    return nltk.metrics.scores.accuracy(flatten(filtered_data),
                                        flatten(tagged_data))


print("Accuracy:", measure_accuracy())
