import nltk
from nltk.tag.stanford import StanfordNERTagger
from nltk.util import ngrams

def nerTagger(sentence):
    st= StanfordNERTagger('ner/english.all.3class.distsim.crf.ser.gz','ner/stanford-ner.jar',encoding='utf-8')
    words = nltk.word_tokenize(sentence)
    tagged_words = st.tag(words)
    return tagged_words


def nerTagResults(results):
	answer_tags=[]
	for result in results:
		answer_tag=nerTagger(result)
		answer_tags.append( (result,answer_tag) )

	return answer_tags

def wordCountScore(qwords,awords):
	qwords=set(qwords)
	awords=set(awords)

	return float(len(qwords.intersection(awords)) )/( len(qwords)+len(awords) )
	# return len(qwords.intersection(awords)) 

def trigramMatchScore(qwords,awords):
	trigrams1=ngrams(qwords,3)
	trigrams2=ngrams(awords,3)
	trigrams1=set(trigrams1)
	trigrams2=set(trigrams2)
	#print trigrams1
	#print trigrams2

	return float( len(trigrams1.intersection(trigrams2)) )/( len(trigrams1)+len(trigrams2) )
	# return len(trigrams1.intersection(trigrams2))

def bigramMatchScore(qwords,awords):
	bigrams1=ngrams(qwords,2)
	bigrams2=ngrams(awords,2)
	bigrams1=set(bigrams1)
	bigrams2=set(bigrams2)
	#print trigrams1
	#print trigrams2
	
	return float( len(bigrams1.intersection(bigrams2)) )/( len(bigrams1)+len(bigrams2) )
	# return len(bigrams1.intersection(bigrams2))