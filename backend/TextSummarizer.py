from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict

class TextSummarizer:
    def __init__(self, length=5):
        self.stop_words = set(stopwords.words('english') + list(punctuation))
        self.length = length

    def sanitize_input(self, text):
        replace = {ord('\f') : ' ',
                   ord('\t') : ' ',
                   ord('\n') : ' ',
                   ord('\r') : None}

        return text.translate(replace)

    def tokenize(self, text):
        words = word_tokenize(text.lower())

        return [
            sent_tokenize(text),
            [word for word in words if word not in self.stop_words]
        ]

    def score_tokens(self, filtered_words, sentence_tokens):
        word_freq = FreqDist(filtered_words)

        ranking = defaultdict(int)

        for i, sentence in enumerate(sentence_tokens):
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    ranking[i] += word_freq[word]

        return ranking

    def summarize(self, text):
        text = self.sanitize_input(text)
        sentence_tokens, word_tokens = self.tokenize(text)
        sentence_ranks = self.score_tokens(word_tokens, sentence_tokens)

        if int(self.length) > len(sentence_tokens):
            indexes = nlargest(len(sentence_tokens), sentence_ranks, key=sentence_ranks.get)
        else:
            indexes = nlargest(self.length, sentence_ranks, key=sentence_ranks.get)

        final_sentences = [sentence_tokens[j] for j in sorted(indexes)]
        return ' '.join(final_sentences)
