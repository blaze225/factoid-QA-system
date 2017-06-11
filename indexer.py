# Import the os module for file system management
import os
import nltk
from nltk.tokenize import sent_tokenize;
# Set the database path
databasePath = os.path.abspath('xapian-database')
# Make a folder at the database path
os.mkdir(databasePath)

# Import Xapian's Python bindings
import xapian

# Create the Xapian database
database = xapian.WritableDatabase(databasePath, xapian.DB_CREATE_OR_OPEN)
# Initialize indexer
indexer = xapian.TermGenerator()
# Set word stemmer to English
indexer.set_stemmer(xapian.Stem('english'))
# Import the glob module for file system browsing

import glob
# Specify the value slot to store each document's file name
xapian_file_name = 0

# For each text file,
for filePath in glob.glob('data/*.txt'):
    # Load content
    content = open(filePath).read()
    # Prepare document
    #content=content.replace("\n","")
    content=unicode(content, 'utf-8')
    paragraphs = [p for p in content.split('\n') if p]
# and here, sent_tokenize each one of the paragraphs
    for paragraph in paragraphs:
        sentences=sent_tokenize(paragraph)
    
        for i,line in enumerate(sentences):
            document = xapian.Document()
            document.set_data(line)
            # Store fileName
            fileName = os.path.basename(filePath)
            fileName+=str(i)
            document.add_value(xapian_file_name, fileName)
            # Index document
            indexer.set_document(document)
            indexer.index_text(line)
            # Store indexed content in database
            database.add_document(document)

# Save changes
database.flush()