import questiontype as qt
import xapianSearch as xs
while(True):
    print("Enter Question:")
    question=raw_input()
    type,target=qt.returnKeywords(question)
    print type
    print target

    print "=========================================================================================================="

    results=xs.searchQuery(target)
    res2=[]
    for line in results:
    	#line=line.replace("\n"," ")
    	line=line.strip()
    	res2.append(line)
    for result in res2:
    	print result
    	print ""