from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
from nltk.tag import pos_tag
import string

import time

from backend.SpellChecker import SpellCheckerMedical
import Levenshtein as leven

class PreprocessText:
    def __init__(self, word_list_path):
        self.spellchecker = SpellCheckerMedical(word_list_path)
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = SnowballStemmer('english')

    def Tokenize(self, text):
        text = text.lower()
        text = pos_tag(word_tokenize(text))
        text = [word[0] for word in text if word[1].startswith("VB") or word[1].startswith("NN") or word[1].startswith("JJ")]
        text = [word.lower() for word in text]
        return text

    def CleanStopWords(self, words):
        for stopword in self.stop_words:
            if stopword in words:
                words = list(filter(lambda a: a != stopword, words))

        return words

    def Stemmer(self, words):
        for i in range(len(words)):
            words[i] = self.stemmer.stem(words[i])

        return words

    def SpellCheck(self, words):
        word_list = []

        for word in words:
            suggestions = self.spellchecker.check(word)
            if suggestions == []:
                word_list.append(word)
            else:
                distance =float('inf')
                most_similar = None
                for suggestion in suggestions:
                    dist = leven.distance(word, suggestion)
                    if dist < distance:
                        distance = dist
                        most_similar = suggestion
                word_list.append(most_similar)

        return word_list

    def process(self, text):
        words = self.Tokenize(text)
        words = self.CleanStopWords(words)
        words = self.SpellCheck(words)
        words = self.Stemmer(words)

        return ' '.join(words)

if __name__ == '__main__':
    preprocessor = Preprocess('medical_wordlist.txt')
    start = time.time()
    text = preprocessor.process('i am having a verrry bad pain in my stomach')
    print('Done: {} sec'.format(time.time() - start))
    print(text)
