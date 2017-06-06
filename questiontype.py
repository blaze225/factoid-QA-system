import sys
import numpy
import nltk
import nltk.data
import collections
from nltk.corpus import stopwords
from nltk.tag.stanford import StanfordNERTagger
import nltk

yesnowords = ["can", "could", "would", "is", "does", "has", "was", "were", "had", "have", "did", "are", "will"]
commonwords = ["the", "a", "an", "is", "are", "were", "."]
questionwords = ["who", "what", "where", "when", "why", "how", "whose", "which", "whom"]
stopwords=list(stopwords.words('english'))

def NerTagger(text):
    st= StanfordNERTagger('ner/english.all.3class.distsim.crf.ser.gz','ner/stanford-ner.jar',encoding='utf-8')
    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)
# Take in a tokenized question and return the question type and body
def processquestion(qwords):
    
    # Find "question word" (what, who, where, etc.)
    questionword = ""
    qidx = -1

    for (idx, word) in enumerate(qwords):
        if word.lower() in questionwords:
            questionword = word.lower()
            qidx = idx
            break
        elif word.lower() in yesnowords:
            return ("YESNO", qwords)

    if qidx < 0:
        return ("MISC", qwords)

    if qidx > len(qwords) - 3:
        target = qwords[:qidx]
    else:
        target = qwords[qidx+1:]
    type = "MISC"

    # Determine question type
    if questionword in ["who", "whose", "whom"]:
        type = "PERSON"
    elif questionword == "where":
        type = "PLACE"
    elif questionword == "when":
        type = "TIME"
    elif questionword == "how":
        if target[0] in ["few", "little", "much", "many"]:
            type = "QUANTITY"
            target = target[1:]
        elif target[0] in ["young", "old", "long"]:
            type = "TIME"
            target = target[1:]

    # Trim possible extra helper verb
    if questionword == "which":
        target = target[1:]
    if target[0] in yesnowords:
        target = target[1:]
    # Remove Stopwords
    for i,item in enumerate(target):
        if item in stopwords:
            target.remove(target[i])
            
    # Return question data
    return (type, target)

def returnKeywords(question):
    # Hardcoded word lists
    qwords = nltk.word_tokenize(question.replace('?', ''))
    (type, target) = processquestion(qwords)
    return (type,target)
    

