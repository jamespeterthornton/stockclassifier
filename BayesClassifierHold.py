# Name: Dylan Hurwitz and James Thornton
# Date: 3/23/13
# Description: Sentiment Analysis by a Naive Bayes Classifier: For this project, 
# we implement a program that uses Bayes' Law to analyze sentiment in text documents
# within two possible labels.

import math, os, pickle
from DataReader import *
from collections import defaultdict

class BayesClassifier:

   def __init__(self):
      '''This method initializes the Naive Bayes classifier'''
      #The positive and negative dictionaries will hold all words that appear in positive and negative documents
      #"defaultdict" sets up a dictionary where the value of a previously unseen key is zero
      # self.allwords will hold all of the words we've ever seen, for generating "k"
      self.positivedict = defaultdict(lambda:0)
      self.negativedict = defaultdict(lambda:0)  
      self.allwords = {}  
      #These two variables will hold the two labels
      self.label1 = ""
      self.label2 = ""
      #These variables hold the average risk length of positive documents, the average risk length of negative documents, and the average of those two
      self.avlpositive = 0
      self.avlnegative = 0
      self.avl = 0

   def train(self, dataFile):   
      '''Trains the Naive Bayes Sentiment Classifier.'''
      reader = DataReader(dataFile)
      #There may be a better way to get the two labels, but we just grabbed one label with the next three lines ...
      for label, tokens, company, date, price, risklength in reader:
              self.label2 = label
              break
      # ...and then grabbed the other label by iterating through until we found a label different from the first one
      for label, tokens, company, date, price, risklength in reader:
              if self.label2 != label:
                      self.label1 = label
      reader = DataReader(dataFile)
      #Iterate through all of the documents in the training set
      for label, tokens, company, date, price, risklength in reader:
               #Check if the document is positive or negative, so that we can modify the according dictionary
              if label == self.label1:
                      #using i and tokens[i], we iterate through all of the words in the document
                      for i in range(0,len(tokens)):
                              #for each word, add one to it's count in the dictionary,
                              # add one to "total*" tracking the number of words in positive documents,
                              # and add the word to "allwords" (this only changes anything if the word is not already in allwords) by setting its value equal to zero
                              self.positivedict[tokens[i]] +=1
                              self.positivedict['total*'] += 1
                              self.allwords[tokens[i]] = 0

              # Repeat for negative
              if label == self.label2:
                      for i in range(0,len(tokens)):
                              self.negativedict[tokens[i]]+=1
                              self.negativedict['total*'] += 1
                              self.allwords[tokens[i]] = 0



   def classify(self, sText, risklength):
      '''Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive or negative ).
      '''
      #add the total words from positive and negative to obtain totalwords
      bigtotal = self.positivedict['total*'] + self.negativedict['total*']
      #tokenize the text, get k, and initialize the probabilities we will later compare
      a = tokenize(sText)
      k = len(self.allwords)
      probpos = 0
      probneg = 0
      #using i and a[i], iterate through all words in the text to be analyzed
      for i in range(0, len(a)):
              #For positive:
              #Get the count for this word and the total count for positive
              count = float(self.positivedict[a[i]])
              total = float(self.positivedict['total*'])
              # Add lambda to count, which will serve as the numerator
              count += .25
              # Add lambda * k to total, which will serve as the denom
              total += float(k*.25)
              # Divide count by total and add the log of that to probpos, a variable tracking the probability that this document is positive
              probpos += math.log(float(count)/float(total))
              #Repeat for negative
              count = float(self.negativedict[a[i]])
              total = float(self.negativedict['total*'])
              count += .25
              total += float(k*.25)
              probneg += math.log(float(count)/float(total))
      #Finally, add the p(positive) to probpos and p(negative) to probneg
      probpos += math.log(float(self.positivedict['total*'])/bigtotal)
      probneg += math.log(float(self.negativedict['total*'])/bigtotal)
         
      # Return the more likely label
      print probpos/probneg
      if (probpos - probneg) > 1750:
              return self.label1
      elif (probneg - probpos) > 1750:
              return self.label2
      else:
              return "HOLD"

   def save(self, sFilename):
      '''Save the learned data during training to a file using pickle.'''

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      # use dump to dump your variables
      p.dump(self.positivedict)
      p.dump(self.negativedict)
      f.close()
   
   def load(self, sFilename):
      '''Given a file name of stored data, load and return the object stored in the file.'''

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      # use load to load in previously dumped variables
      self.positivedict = u.load()
      self.negativedict = u.load()
      f.close()
