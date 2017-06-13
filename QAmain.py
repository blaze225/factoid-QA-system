import questiontype as qt
import xapianSearch as xs
import rankAnswers as ra
import nltk 

def cleanResults(results):
    res2=[]
    
    for line in results:
        line=line.replace("\n"," ")
        res2.append(line)

    return res2

def printList(lst):
    for it in lst:
        print it;

def containsQuestionType(questiontype,taggedResult):

    for taggedword in taggedResult:
        if taggedword[1] == questiontype:
            return True

    return False


# def findQuestionTypeAnswers(questiontype,taggedResults):
#     qtresults=[]
#     for taggedResult in taggedResults:
#         if containsQuestionType(questiontype,taggedResult[1]) :
#             for taggedword in taggedResult[1]:
#                 if taggedword[1] == questiontype:
#                     qtresults.append(taggedword[0])

#     return qtresults;
def getQuestionTypeAnswer(qtype,tagged_words):
	answer=""
	for word,tag in tagged_words:
		if tag==qtype:
			answer=answer+word+" "

	return answer;


def scoreResult(question,answer):
    qwords = nltk.word_tokenize(question.lower())
    awords = nltk.word_tokenize(answer.lower())


    
    triscore=ra.trigramMatchScore(qwords,awords)
    #print triscore

    biscore=ra.bigramMatchScore(qwords,awords)
    #print biscore

    wcScore=ra.wordCountScore(qwords,awords)
    #print wcScore
    score=3*triscore+2*biscore+wcScore

    #print answer,score
    return (score,answer)


def scoreResults(question,results):
    scoredanswers=[]
    for answer in results:
        scoredanswer=scoreResult(question,answer)
        scoredanswers.append(scoredanswer)

    return scoredanswers


while(True):
    print("Enter Question:")
    question=raw_input()
    qtype,clean_qwords=qt.returnKeywords(question)
    print qtype
    print clean_qwords
    print "=========================================================================================================="
    
    results=xs.searchQuery(clean_qwords)
    results=cleanResults(results)
    
    scoredanswers=scoreResults(question,results)
    scoredanswers=sorted(scoredanswers,reverse=True)

    printList(scoredanswers)
    print ""
    print ""
    print "=========================================================================================================="


    for sentence in results:
    	tagged_words=ra.nerTagger(sentence)
    	answer=getQuestionTypeAnswer(qtype,tagged_words);
    	print answer