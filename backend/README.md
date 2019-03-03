# SIH2019-Backend

Backend for SearchEngine for Library resources

## Usage

 - Index Database:
   - One time step for existing process. Run `IndexDataBase.py` file to index all the database (PDFs). Name of Indexed database by default is `IndexedDatabase`. Edit file to your need.
  
 - Search Engine:
   - Enter keyword and get a list of dictionary of matched pdfs. The dictionary is of format - 
   ```
   {'title': '...', 
    'pdf_path': '...',
    'abstract': '...',
    'creation_date': '...'}
   ```
  
## Dependencies

 - Whoosh: `pip3 install whoosh`
 - Levenshtein: `pip3 install python-Levenshtein`
 - PdfToText: `pip3 install pdftotext`
 - NLTK: `pip3 install nltk`
 - tqdm: `pip3 install tqdm`
 - PyEnchant: `pip3 install pyenchant`
 - pdfrw: `pip3 install pdfrw`
 - Pandas: `pip3 install pandas`
 - NumPy: `pip3 install numpy`
