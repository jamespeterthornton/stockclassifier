from DataReader import *
#from BayesClassifier import *
from BayesClassifierHold import *
from collections import defaultdict

def eval(sText):
    totalaccuracy_numer = 0;
    totalaccuracy_denom = 0;
    for test in range(0,10):
        thisaccuracy_numer = 0
        thisaccuracy_denom = 0;
        split(sText, "output")
        for doc in range (0,5):
            print "i is: ", doc
            totaldic = defaultdict(lambda: 0)
            totalcorrectdic = defaultdict(lambda: 0)
            bc = BayesClassifier()
            bc.train("output.train{0}".format(doc%5))
            bc.train("output.train{0}".format((doc+1)%5))
            bc.train("output.train{0}".format((doc+2)%5))
            bc.train("output.train{0}".format((doc+3)%5))
            reader = DataReader("output.train{0}".format((doc+4)%5))
            correct = 0
            total = 0
            hold = 0
            for label, tokens, company, date, price, risklength in reader:
                print label
                tokenstring = " "
                tokenstring = tokenstring.join(tokens) 
                print date
                if risklength == 1:
                    print "invalid document; ignore"
                #elif bc.classify(tokenstring, risklength, date) == "HOLD":
                elif bc.classify(tokenstring, risklength) == "HOLD":
                    hold += 1
                else:
                    totaldic[label] +=1
                    total += 1
                        
                    #if bc.classify(tokenstring, risklength, date) == label:
                    if bc.classify(tokenstring, risklength) == label:
                        correct += 1
                        totalcorrectdic[label] += 1
                    
            print "Holds: ", hold
            print "Accuracy:", correct/float(total)
            thisaccuracy_numer += correct/float(total)
            thisaccuracy_denom += 1
            for key in totaldic:
                    print totalcorrectdic[key], totaldic[key]
                    print key, " precision: ", totalcorrectdic[key]/float(totaldic[key])
        
        print "This Round Accuracy: ", thisaccuracy_numer/thisaccuracy_denom
        totalaccuracy_numer += thisaccuracy_numer
        totalaccuracy_denom += thisaccuracy_denom
    print "Total Accuracy: ", totalaccuracy_numer/totalaccuracy_denom
