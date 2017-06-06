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

def printResults(results):
    for result in results:
        print result;

def containsQuestionType(questiontype,taggedResult):

    for taggedword in taggedResult:
        if taggedword[1] == questiontype:
            return True

    return False


def findQuestionTypeAnswers(questiontype,taggedResults):
    qtresults=[]
    for taggedResult in taggedResults:
        if containsQuestionType(questiontype,taggedResult[1]) :
            for taggedword in taggedResult[1]:
                if taggedword[1] == questiontype:
                    qtresults.append(taggedword[0])

    return qtresults;

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

    print answer,score
    return score


def scoreResults(question,results):
    for answer in results:
        scoreResult(question,answer)

while(True):
    print("Enter Question:")
    question=raw_input()
    type,clean_qwords=qt.returnKeywords(question)
    print type
    print clean_qwords
    print "=========================================================================================================="
    
    results=xs.searchQuery(clean_qwords)
    results=cleanResults(results)
    #taggedResults=ra.nerTagResults(results)
    #print taggedResults
    #questiontype=type
    #qtresults=findQuestionTypeAnswers(questiontype,taggedResults)
    #printResults(qtresults)
    
    scoreResults(question,results)
    


