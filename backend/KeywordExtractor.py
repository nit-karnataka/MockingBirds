import pdftotext

import pandas as pd
import numpy as np
import sys
from collections import Counter
import string
import os
import time
from tqdm import tqdm

from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
from nltk.tag import pos_tag

from backend.PreprocessText import PreprocessText
from backend.SpellChecker import SpellCheckerMedical

class KeywordExtractor(PreprocessText):
    def __init__(self, word_list_path='backend/all_word_list.txt'):
        self.spellchecker = SpellCheckerMedical(word_list_path)
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = SnowballStemmer('english')

    def read_pdf(self, pdf_file):
        with open(pdf_file, 'rb') as file_:
            pdf = pdftotext.PDF(file_)

        text = []
        for i in range(len(pdf)):
            text.append(pdf[i].replace('  ', ''))

        return text

    def calculate_tf_idf(self, raw_count, max_raw_count_in_document, no_documents, no_documents_in_which_word_occured):
        tf = 0.5 + 0.5*(raw_count/max_raw_count_in_document)
        idf = np.log(no_documents/(1 + no_documents_in_which_word_occured))
        return tf*idf

    def extract(self, pdf_file):
        document_text = self.read_pdf(pdf_file)

        page_1 = document_text[0]

        # Tokenizing Words
        for i in range(len(document_text)):
            document_text[i] = self.Tokenize(document_text[i])

        # Removing Stopwords
        for i in range(len(document_text)):
            document_text[i] = self.CleanStopWords(document_text[i])

        # Stemming
        for i in tqdm(range(len(document_text))):
            document_text[i] = self.Stemmer(document_text[i])

        total_text = []

        for text in document_text:
            total_text += list(text)

        words = set(total_text)

        # Raw Count for all keywords
        word_count = Counter(total_text)
        raw_count = Counter(total_text)
        max_raw_count_in_document = next(iter(word_count.values()))

        # Calculating TF-IDF Values for all keywords
        for word in word_count:
            count = 0
            for text in document_text:
                if word in text:
                    count += 1

            no_documents_in_which_word_occured = count
            word_count[word] = self.calculate_tf_idf(word_count[word], max_raw_count_in_document, len(document_text), no_documents_in_which_word_occured)

        word_count = list(word_count.items())

        i = 0
        for w in raw_count:
            word_count[i] = word_count[i] + (raw_count[w], )
            i += 1

        # Storing all the keywords in Data-Frame
        df = pd.DataFrame(list(word_count), columns=['Keywords', 'TF_IDF', "Raw_Count"])

        df = df.sort_values('TF_IDF', ascending=True)

        #df.to_csv('keywords.csv', sep=',')
        word_list = df['Keywords']

        no_words = len(word_list)

        word_list = word_list[:int(no_words*.9)]

        words = []
        for word in word_list:
            if len(word) > 2:
                words.append(word)

        keywords = ' '.join(words)

        return keywords, page_1
