from DataReader import *
from BayesClassifier import *
from collections import defaultdict

def eval(sText):
        totaldic = defaultdict(lambda: 0)
        totalcorrectdic = defaultdict(lambda: 0)
        split(sText, "output")
        bc = BayesClassifier()
        bc.train("output.train")
        reader = DataReader("output.test")
        correct = 0
        total = 1
        for label, tokens, company, date, price, risklength in reader:
                print label
      
                totaldic[label] +=1
                total += 1
                tokenstring = " "
                tokenstring = tokenstring.join(tokens)          
                if bc.classify(tokenstring) == label:
                        correct += 1
                        totalcorrectdic[label] += 1
              
        print "accuracy:", correct/float(total) 
        for key in totaldic:
                print totalcorrectdic[key], totaldic[key]
                print key, " precision: ", totalcorrectdic[key]/float(totaldic[key])
