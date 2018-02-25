from bfex.models import *
from .key_generation_approach import KeyGenerationApproach
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from collections import Counter

class GenericApproach(KeyGenerationApproach):
"""
A generic approach that finds most common words w/o stop words
"""
    def __init__(self):
        self.description = """word frequency minus nltk stop words http://www.nltk.org/data.html"""
        self.approach_id = 1
    def generate_keywords(self, scrapp):
        """Tokenizes, remove stopwords, and counts word frequency"""
        stop_words = set(stopwords.words('english'))
        words = wordpunct_tokenize(scrapp.text)
        wordsFiltered = [] 
        for w in words:
            if w not in stop_words:
                wordsFiltered.append(w)
        word_counts = Counter(wordsFiltered)
        return word_counts
        
    def get_id(self):
        """The assigned id for the approach"""
        return self.approach_id
