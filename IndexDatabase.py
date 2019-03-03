from whoosh.index import create_in, open_dir
from whoosh.fields import *

from pdfrw import PdfReader

import nltk.data

import os
from math import log
from tqdm import tqdm
import platform
import shutil
import time

from datetime import datetime

from backend.KeywordExtractor import KeywordExtractor
from backend.PreprocessText import PreprocessText
from backend.TextSummarizer import TextSummarizer

class CreationDate:
    def __init__(self):
        self.month_to_index = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6,
                               'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec': 12}

    def creation_date_fstat(self, path_to_file):
        if platform.system() == 'Windows':
            date = os.path.getctime(path_to_file)
        else:
            stat = os.stat(path_to_file)
            try:
                date = stat.st_birthtime
            except AttributeError:
                date = stat.st_mtime

        return datetime.fromtimestamp(date)

    def extract(self, path_to_file):
        reader = PdfReader(path_to_file)
        date = str(reader.Info.CreationDate)
        if date == None or date == 'None':
            date = str(self.creation_date_fstat(path_to_file))

        date = date.replace('(', '')
        date = date.replace(')', '')

        if date.startswith('D:'):
            year = date[2:6]
            month = date[6:8]
            day = date[8:10]
        else:
            if len(date.split()) == 2:
                year = str(date.split(' ')[0].split('-')[0])
                month = str(date.split(' ')[0].split('-')[1])
                day = str(date.split(' ')[0].split('-')[2])
            elif len(date.split()) == 3:
                year = str(date.split(' ')[2])
                month = str(date.split(' ')[1])
                month = str(self.month_to_index[month[:3]])
                day = str(date.split(' ')[0])[:2]
            else:
                year = str(date.split(' ')[-1])
                month = str(date.split(' ')[1])
                month = str(self.month_to_index[month[:3]])
                day = str(date.split(' ')[2])

        return '{}-{}-{}'.format(year, month, day)

class TitleExtractor:
    def __init__(self, word_list_path='backend/all_word_list.txt'):
        self.single_line_summariation = TextSummarizer(length=1)

    def extract(self, pdf_file, page_1):
        reader = PdfReader(pdf_file)
        title = reader.Info.Title

        if (title == None) or (title == '(untitled)') or (len(title.split(' ')) < 5):
            title = self.single_line_summariation.summarize(page_1)

        title = title.replace('(', '')
        title = title.replace(')', '')

        return title

class AbstractExtractor:
    def __init__(self):
        self.word_limit = 500
        self.sent_limit = 10
        self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    def extract(self, text):
        lines = text.split('\n')
        index = 0
        for i, line in enumerate(lines):
            if 'abstract' in line.lower():
                index = i
                break
            elif 'introduction' in line.lower():
                index = i
                break

        text = ' '.join(lines[index+1:])

        return text


class Indexer:
    def __init__(self, index_dir='IndexedDatabase'):
        print('Initializing Database ..')
        self.index_dir = index_dir

        if not os.path.exists(index_dir):
            self.schema = Schema(title=TEXT(stored=True), keywords=TEXT(stored=True),
                            pdf_path=TEXT(stored=True), abstract=TEXT(stored=True),
                            creation_date=TEXT(stored=True))

            os.mkdir(self.index_dir)

            self.indexer = create_in(self.index_dir, self.schema)
        else:
            self.indexer = open_dir(self.index_dir)

        self.writer = self.indexer.writer()

        self.titleextractor = TitleExtractor(word_list_path='backend/all_word_list.txt')
        self.keywordextractor = KeywordExtractor()
        self.abstractextractor = AbstractExtractor()
        self.textsummarizer = TextSummarizer()

        self.creationdate = CreationDate()
        print('Done.!')

    def add(self, database_dir='pdfs/'):
        for file_ in tqdm(os.listdir(database_dir), desc='Indexing Database'):
            try:
                pdf_path = os.path.join(database_dir, file_)

                creation_date = self.creationdate.extract(pdf_path)
                year = int(datetime.now().year)
                year_paper = int(creation_date.split('-')[0])

                if year - year_paper < 10:
                    keywords, page_1 = self.keywordextractor.extract(pdf_path)

                    text = self.abstractextractor.extract(page_1)
                    summary = self.textsummarizer.summarize(text)

                    title = self.titleextractor.extract(pdf_path, text)
                    self.writer.update_document(title=title, keywords=keywords, pdf_path=os.path.join('pdfs', file_),
                                                abstract=summary, creation_date=creation_date)

                shutil.copyfile(pdf_path, os.path.join('pdfs', file_))

            except Exception as e:
                #print('---------------------------------------------')
                #print(e, file_)
                #print('---------------------------------------------')
                pass

        self.writer.commit()
        print('\n')

if __name__ == '__main__':
    indexer = Indexer('IndexedDatabase')
    start = time.time()
    indexer.add('SampleDocs')
    print(time.time() - start)
