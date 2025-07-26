import js
import re
import random
import numpy as np
from collections import defaultdict

# Custom Lexicon with Emotional Weights
LEXICON = {
    'noun': {
        'happy': ['smile', 'sunlight', 'hope', 'friend'],
        'sad': ['tear', 'shadow', 'loss', 'rain'],
        'fearful': ['darkness', 'whisper', 'danger', 'mist'],
        'suspense': ['mystery', 'silence', 'secret', 'echo'],
        'comedy': ['clown', 'joke', 'party', 'giggle']
    },
    'verb': {
        'happy': ['laughed', 'danced', 'sang', 'embraced'],
        'sad': ['cried', 'sighed', 'wandered', 'mourned'],
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
    'happy': 0.8, 'sad': -0.5, 'fearful': -0.7, 'suspense': -0.3, 'comedy': 0.9,
    'smile': 0.5, 'hope': 0.4, 'friend': 0.3, 'tear': -0.4, 'loss': -0.5,
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

# Narrative Engine with Extensions
class WordWeaver:
    def __init__(self, emotion, protagonist, setting):
        self.emotion = emotion.lower()
        self.memory = EntityMemory(protagonist, setting)
        self.semantic_checker = SemanticChecker()
        self.story_sentences = []

    def choose_word(self, pos):
        words = LEXICON.get(pos, {}).get(self.emotion, [])
        if not words:
            return random.choice(LEXICON[pos][random.choice(list(LEXICON[pos].keys()))])
        return random.choice(words)

    def generate_phrase(self, structure):
        if structure in GRAMMAR['DET'] + GRAMMAR['PREP']:
            return structure
        if structure in ['NOUN', 'VERB', 'ADJ', 'ADV']:
            word = self.choose_word(structure.lower())
            if structure == 'NOUN':
                self.memory.track_noun(word)
            return word
        if structure == '{protagonist}':
            return self.memory.get_entity('protagonist')
        if structure == '{setting}':
            return self.memory.get_entity('setting')
        return ' '.join(self.generate_phrase(part) for part in GRAMMAR[structure][random.randint(0, len(GRAMMAR[structure])-1)].split())

    def generate_sentence(self):
        structure = random.choice(GRAMMAR['SENTENCE'])
        sentence = ' '.join(self.generate_phrase(part) for part in structure.split())
        sentence = sentence.replace('{protagonist}', self.memory.get_entity('protagonist'))
        sentence = sentence.replace('{setting}', self.memory.get_entity('setting'))
        sentence = sentence[0].upper() + sentence[1:] + '.'
        self.story_sentences.append(sentence)
        self.semantic_checker.build_vector(sentence)
        return sentence

    def generate_story(self, length=3):
        story = [f"{self.memory.get_entity('protagonist')}'s journey began in {self.memory.get_entity('setting')}."]
        for _ in range(length - 1):
            new_sentence = self.generate_sentence()
            if self.story_sentences:
                prev_sentence = self.story_sentences[-1]
                sim_score = self.semantic_checker.similarity(prev_sentence, new_sentence)
                if sim_score < 0.2:
                    new_sentence = self.generate_sentence()
            story.append(new_sentence)
        return ' '.join(story)

    def calculate_moral_score(self, story):
        words = re.findall(r'\b\w+\b', story.lower())
        score = sum(MORAL_WEIGHTS.get(word, 0) for word in words)
        return round(score / max(1, len(words)), 2)

    def rewrite_tone(self, story, new_tone):
        words = re.findall(r'\b\w+\b', story.lower())
        new_words = []
        for word in words:
            if word in MORAL_WEIGHTS:
                pos = next((p for p, d in LEXICON.items() if word in sum(d.values(), [])), None)
                if pos and new_tone in LEXICON[pos]:
                    new_words.append(random.choice(LEXICON[pos][new_tone]))
                else:
                    new_words.append(word)
            else:
                new_words.append(word)
        sentences = story.split('.')
        new_sentences = []
        for sent in sentences:
            if sent.strip():
                new_sent = sent
                for i, word in enumerate(words):
                    if word in MORAL_WEIGHTS:
                        new_sent = re.sub(r'\b' + word + r'\b', new_words[i], new_sent, flags=re.IGNORECASE)
                new_sentences.append(new_sent)
        return '. '.join(new_sentences) + ('.' if new_sentences else '')

    def generate_plot_twist(self):
        last_sentence = self.story_sentences[-1] if self.story_sentences else ''
        contradiction = {
            'happy': 'But then, a shadow loomed over the cheerful scene.',
            'sad': 'Yet, a spark of hope flickered in the gloom.',
            'fearful': 'Suddenly, the danger vanished, revealing a surprising ally.',
            'suspense': 'But the mystery unraveled, exposing a mundane truth.',
            'comedy': 'Then, the joke turned into an unexpected challenge.'
        }
        twist = contradiction.get(self.emotion, 'But then, an unexpected event changed everything.')
        self.story_sentences.append(twist)
        return twist

js.WordWeaver = WordWeaver