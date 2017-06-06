# Import system modules
import os
import xapian
import datetime
# Import custom modules
from query_process_simplified import TextMachine


# Load the Xapian database
databasePath = os.path.abspath('xapian-database')
database = xapian.WritableDatabase(databasePath, xapian.DB_OPEN)
# Set slot constants
xapian_file_name, xapian_when, xapian_owner_id = xrange(3)


def search(queryString, byDate=False, ownerID=None, extractLength=32):
    # Parse query string
    queryParser = xapian.QueryParser()
    queryParser.set_stemmer(xapian.Stem('english'))
    queryParser.set_database(database)
    queryParser.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
    query = queryParser.parse_query(queryString)
    # Set offset and limit for pagination
    offset, limit = 0, database.get_doccount()
    # Start query session
    enquire = xapian.Enquire(database)
    enquire.set_query(query)
    # Sort by date
    if byDate:
        enquire.set_sort_by_value(xapian_when)
    if ownerID == None:
        matches = enquire.get_mset(offset, limit)
    else:
        # Filter by ownerID
        matches = enquire.get_mset(offset, limit, None, MatchDecider(ownerID))
    # Display matches
    for match in matches:
        # Load
        documentWhen = match.document.get_value(xapian_when)
        # documentOwnerID = int(xapian.sortable_unserialise(match.document.get_value(xapian_owner_id)))
        # Display
        print '==================='
        print 'rank=%s, documentID=%s' % (match.rank, match.docid)
        # Process
        content = match.document.get_data()
        extract = TextMachine(extractLength, '*%s*').process(queryString, content)
        print extract.replace('\n', ' ')
    print '==================='
    print 'Number of documents matching query: %s' % matches.get_matches_estimated()
    print 'Number of documents returned: %s' % matches.size()

# Import regular expression library
import re

# IMPORTANT
# You must run queryParser on the content before calling these functions.
# queryParser.parse_query(content)

def extractRelevantText(query, queryParser, content):
    """
    Illustrate the use of unstemming to extract parts of the document
    that contain keywords from the search query.
    """
    # Initialize
    extracts = []
    # For each query word,
    for queryWord in set(query):
        # Reverse map query words to document words
        documentWords = list(queryParser.unstemlist(queryWord))
        # If the query word is not in the document, skip it
        if not documentWords:
            continue
        # Prepare regular expression using matching document words
        searchExpression = r'.{0,10}%s.{0,10}' % '|'.join(documentWords)
        pattern = re.compile(searchExpression, re.DOTALL | re.IGNORECASE)
        # Extract relevant text
        extracts.extend(pattern.findall(content))
    # Return
    return extracts

def highlightWords(query, queryParser, content, highlight_template):
    """
    Illustrate the use of unstemming to highlight keywords in the document
    that match the search query.
    """
    # For each query word,
    for queryWord in set(query):
        # Reverse map query words to document words
        documentWords = list(queryParser.unstemlist(queryWord))
        # If the query word is not in the document, skip it
        if not documentWords:
            continue
        # Prepare regular expression using matching document words
        searchExpression = r'(%s)' % '|'.join(documentWords)
        # Compile pattern
        pattern = re.compile(searchExpression, re.IGNORECASE)
        # Highlight matching words
        content = pattern.sub(highlight_template % r'\1', content)
    # Return
    return content

search_line=raw_input();
search(search_line)