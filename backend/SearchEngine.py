from whoosh.index import open_dir
from whoosh.qparser import *
from whoosh.query import *
import fasttext

from tqdm import tqdm

from backend.PreprocessText import *
from backend.KeywordExtractor import KeywordExtractor

import os
import string
import shutil

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SearchEngine:
    def __init__(self, index_dir='IndexedDatabase'):
        self.index_dir = index_dir

        if not os.path.exists(index_dir):
            print('ERROR: Index \'{}\' not found'.format(index_dir))
            sys.exit(1)
        else:
            self.indexer = open_dir(self.index_dir)

        self.parser = QueryParser('keywords', self.indexer.schema)
        self.keywordextractor = KeywordExtractor()

    def preprocess_input(self, query_text, word_list_path='backend/medical_wordlist.txt'):
        translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
        query_text = query_text.translate(translator)

        self.preprocessor = PreprocessText(word_list_path)
        text = self.preprocessor.process(query_text)
        return text

    def check_uniqueness(self, toCheck, sent_pdfs):
        toCheck_keywords, _ = self.keywordextractor.extract(toCheck)
        results = self.indexer.searcher().documents()

        for path in sent_pdfs:
            keywords = ''
            for result in results:
                if result['pdf_path'] == path:
                    keywords = result['keywords']
                    break

            if keywords == toCheck_keywords:
                return False

        return True

    def search(self, keyword, sent_pdfs, operation='OR'):
        keywords = keyword.split(',')
        updated_keywords = []
        total_keywords = []
        for word in keywords:
            updated_keywords.append(self.preprocess_input(word))
            total_keywords += updated_keywords[-1].split(' ')

        keyword = ','.join(updated_keywords)

        keyword = keyword.replace(' ', ' {} '.format('AND'))
        keyword = keyword.replace(',', ' {} '.format(operation))

        query = self.parser.parse(keyword, normalize=False)

        result_ = []
        with self.indexer.searcher() as engine:
            result = list(engine.search(query, terms=True))
            for hit in result:
                if len(hit.matched_terms()) > 0:
                    if {'pdf_path': hit['pdf_path'],'title': hit['title'],'abstract': hit['abstract']} not in result_:
                        isUnique = self.check_uniqueness(hit['pdf_path'], sent_pdfs)

                        if isUnique:
                            relevance = (len(hit.matched_terms())/len(total_keywords))*100
                            result_.append({'pdf_path': hit['pdf_path'],
                                        'title': hit['title'],
                                        'abstract': hit['abstract'],
                                        'creation_date': hit['creation_date'],
                                        'relevance': '{}%'.format(relevance)})
                        else:
                            shutil.copyfile(hit['pdf_path'], os.path.join('copies/', os.path.basename(hit['pdf_path'])))

        return result_


class SimilaritySearchEngine(SearchEngine):
    def __init__(self, model_path='skipgram.bin', index_dir='IndexedDatabase'):
        self.index_dir = index_dir

        if not os.path.exists(index_dir):
            print('ERROR: Index \'{}\' not found'.format(index_dir))
            sys.exit(1)
        else:
            self.indexer = open_dir(self.index_dir)
        self.model = fasttext.load_model(model_path)
        self.keywordextractor = KeywordExtractor()

    def cosine_similarity(self, word1, word2):
        metrices = np.array([self.model[word1], self.model[word2]])
        similarity = cosine_similarity(metrices)
        return similarity[0][1]

    def search(self, keyword, sent_pdfs, operation='AND'):
        threshold = 0.70
        keywords = keyword.split(',')
        updated_keywords = []
        for word in keywords:
            preprocessed = self.preprocess_input(word)
            updated_keywords += preprocessed.split(' ')

        all_docs = self.indexer.searcher().documents()
        matched_pdfs = []

        for doc in tqdm(all_docs):
            keywords = doc['keywords']
            all_result = set()
            for keyword in keywords.split(' '):
                for query in  updated_keywords:
                    similarity = self.cosine_similarity(query, keyword)
                    if similarity > threshold:
                        all_result.add(query)

                if len(all_result) == len(updated_keywords):
                    matched_pdfs.append(doc)
                    break

        return matched_pdfs

if __name__ == '__main__':
    query = 'controlled ovarian stimulation,inflamatory response,cytokene,window of implantation'
    print('------------------------------------------------------------------------------------------------')
    engine = SearchEngine('IndexedDatabase-Small')
    result = engine.search(query, [''], 'OR')
    for i in range(len(result)):
        print()
        print(result[i]['pdf_path'])
    print(len(result))

    print('------------------------------------------------------------------------------------------------')

    engine = SimilaritySearchEngine('skipgram.bin', 'IndexedDatabase-Small')
    start = time.time()
    result = engine.search(query, [''])
    print(time.time() - start)
    for i in range(len(result)):
        print()
        print(result[i]['pdf_path'])
    print(len(result))

    print('------------------------------------------------------------------------------------------------')
