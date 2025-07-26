import js
import re
import random
import numpy as np
from collections import defaultdict

# Custom Lexicon with Emotional Weights
LEXICON = {
    'noun' : {
        'happy': ['smile', 'sunlight', 'hope', 'friend'],
        'sad': ['tear', 'shadow', 'loss', 'rain'],
        'fearful': ['darkness', 'whisper', 'danger', 'mist'],
        'suspence': ['mystery', 'silence', 'secret', 'echo'],
        'comedy': ['clown', 'joke', 'party', 'giggle']    
    },
    'verb': {
        'happy' : ['laughed', 'danced', 'sang', 'embraced'],
        'sad' : ['cried',  'sighed', 'wandered', 'mourned'],
        'fearful': ['trembled', 'fled', 'hid', 'shuddered'],
        'suspense': ['crept', 'watched', 'waited', 'listened'],
        'comedy': ['juggled', 'tickled', 'pranced', 'chuckled']
    },
    'adjective': {
        'happy': ['bright', 'joyful', 'warm', 'cheerful'],
        'sad': ['gloomy', 'lonely', 'bleak', 'sorrowful'],
        'fearful': ['eerie', 'haunting', 'terrifying', 'grim'],
        'suspense': ['mysterious', 'tense', 'ominous', 'shadowy'],
        'comedy': ['funny', 'silly', 'zany', 'hilarious']
    },
    'adverb': {
        'happy': ['cheerfully', 'brightly', 'happily', 'eagerly'],
        'sad': ['sadly', 'quietly', 'mournfully', 'slowly'],
        'fearful': ['nervously', 'fearfully', 'cautiously', 'anxiously'],
        'suspense': ['silently', 'carefully', 'stealthily', 'warily'],
        'comedy': ['clumsily', 'goofily', 'merrily', 'playfully']
    }
}

# Context-Free Grammar Rules
GRAMMAR = {
    'SENTENCE': ['NP VP', 'NP VP PP', 'NP VP ADV'],
    'NP': ['NOUN', 'ADJ NOUN', 'DET ADJ NOUN'],
    'VP': ['VERB', 'VERB NP', 'VERB ADV'],
    'PP': ['PREP NP'],
    'DET': ['the', 'a', 'an'],
    'PREP': ['in', 'through', 'behind', 'beyond'],
    'NOUN': ['{noun}'],
    'VERB': ['{verb}'],
    'ADJ': ['{adjective}'],
    'ADV': ['{adverb}']
}

# Moral Score Dictionary
MORAL_WEIGHTS = {
    'happy' : 0.8, 'sad' : 0.5, 'fearful' : -0.7, 'suspense' : -0.3, 'comedy' : 0.9,
    'smile' : 0.5, 'hope' : 0.4, 'friend' : 0.3, 'tear' : -0.4, 'loss' : -0.5,
    'danger': -0.6, 'mystery': -0.2, 'laughed': 0.5, 'cried': -0.4,
    'trembled': -0.5, 'crept': -0.3, 'bright': 0.4, 'gloomy': -0.4,
    'eerie': -0.5, 'funny': 0.6
}

