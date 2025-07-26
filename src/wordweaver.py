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

# Entity Memory 
class EntityMemory:
    def __init__(self, protagonist, setting):
        self.protagonist = protagonist
        self.setting = setting
        self.entities = {'protagonist': protagonist, 'setting': setting}
        self.used_nouns = set()

    def get_entity(self, entity_type):
        return self.entities.get(entity_type, '')
    
    def add_entity(self, entity_type, value):
        self.entities[entity_type] = value
    
    def track_noun(self, noun):
        self.used_nouns.add(noun)

# Semantic Checker
class SemanticChecker:
    def __init__(self):
        self.word_vectors = {}
        self.word_freq = defaultdict(lambda: defaultdict(int))
        self.doc_count = 0

    def build_vector(self, sentence):
        words = re.findall(r'\b\w+\b', sentence.lower())
        for word in words:
            self.word_freq[word][self.doc_count] += 1
        self.doc_count += 1
        vector = {}
        for word in words:
            tf = self.word_freq[word][self.doc_count - 1] / len(words)
            idf = np.log(self.doc_count / (1 + len(self.word_freq[word])))
            vector[word] = tf * idf
        self.word_vectors[sentence] = vector
        return vector

    def similarity(self, sent1, sent2):
        vec1 = self.word_vectors.get(sent1, self.build_vector(sent1))
        vec2 = self.word_vectors.get(sent2, self.build_vector(sent2))
        words = set(vec1.keys()) & set(vec2.keys())
        if not words:
            return 0.0
        dot_product = sum(vec1[word] * vec2[word] for word in words)
        norm1 = np.sqrt(sum(v ** 2 for v in vec1.values()))
        norm2 = np.sqrt(sum(v ** 2 for v in vec2.values()))
        return dot_product / (norm1 * norm2 + 1e-10)
