import re, random

class DataReader:
   '''This class supports a functionality to read in data from the data files.
   the class supports iteration and can be used in a for each loop'''

   def __init__(self, dataFile):
      '''Initialize the DataReader.  Pass in a datafile'''
      self.f = open(dataFile, "r")
      self.price2 = 0
       
   def __iter__(self):
      return self

   def next(self):
      ''' Returns the next label/data pair from the data file'''

      #MODIFY THIS TO RETURN DATE AND PRICE ETC
      self.readNext()

      if self.data == "":
         raise StopIteration
      else:
         #MODIFY HERE
         return (self.label, self.data, self.company, self.date, self.price, int(self.risklength[0]))

   def readNext(self):
      '''Read and tokenize the next labal/data pair from the file'''
      self.data = ""
      self.label = ""
      self.company = ""
      self.date = ""
      self.price = ""
      self.risklength = ""
      

      for line in self.f:
         line = line.strip()
         company = re.match(r"<[cC][oO][mM][pP][aA][nN][yY]>(.*)<\/[cC][oO][mM][pP][aA][nN][yY]>", line)
         date = re.match(r"<[dD][aA][tT][eE]>(.*)<\/[dD][aA][tT][eE]>", line)
         price = re.match(r"<[pP][rR][iI][cC][eE]>(.*)<\/[pP][rR][iI][cC][eE]>", line)
         risklength = re.match(r"<[rR][iI][sS][kK][lL][eE][nN][gG][tT][hH]>(.*)<\/[rR][iI][sS][kK][lL][eE][nN][gG][tT][hH]>", line)

         if company:
            self.company = company.group(1)
         if date:
            self.date = date.group(1)
         if price:
            self.price = price.group(1)
         if risklength:
            self.risklength = risklength.group(1)

         elif line == "</DOC>":
            #IF there is data and there is a label
            if self.data != "" and self.price != "" and self.risklength != "" and self.company != "" and self.price != "" and self.date != "":
               self.data = tokenize(self.data)
               self.company = tokenize(self.company)
               self.date = tokenize(self.date)
               self.price = tokenize(self.price)
               self.price = int(self.price[0])
               if(self.price > self.price2):
                   self.label = "SELL"
               else:
                   self.label = "BUY"
               self.price2 = self.price
               self.risklength = tokenize(self.risklength)
               break
            else:
               print "company" + self.company + "price" + self.price + "risklength" + self.risklength + "date" + self.date
               print "Warning: found empty doc11"
         elif line == "<DOC>":
            #the start of a new document
            self.data = ""
            self.company = ""      
            self.date = ""
            self.price = ""
            self.risklength = ""        
         else:
            self.data += line + "\n"
            
def tokenize(sText):
   '''Given a string of text sText, returns a list of the individual tokens that 
   occur in that string (in order).'''

   lTokens = []
   sText = sText.lower().strip()
   sToken = ""
   for c in sText:
      if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\'" or c == "_" or c == '-':
         sToken += c
      else:
         if sToken != "":
            lTokens.append(sToken)
            sToken = ""
         if c.strip() != "":
            lTokens.append(str(c.strip()))
               
   if sToken != "":
      lTokens.append(sToken)

   return lTokens

def split(dataFile, outputLabel):   
   '''Splits data into 80% train, 10% dev and 10% test'''
   reader = DataReader(dataFile)

   train0 = open(outputLabel + ".train0", "w")
   train1 = open(outputLabel + ".train1", "w")
   train2 = open(outputLabel + ".train2", "w")
   train3 = open(outputLabel + ".train3", "w")
   train4 = open(outputLabel + ".train4", "w")

   for label, tokens, company, date, price, risklength in reader:
      
      
      output = "<DOC>\n<LABEL>" + label + "</LABEL>\n" + "<COMPANY>" + company[0] + "</COMPANY>\n" + "<DATE>" + date[0] + "</DATE>\n" + "<PRICE>" + str(price) + "</PRICE>\n" + "<RISKLENGTH>"+ str(risklength) + "</RISKLENGTH>\n" + " ".join(tokens) + "\n</DOC>\n"

      # random selection -- (0,9)
      selection = random.randint(0,4)

      # Note - selection used to equal random.randint(1, 10)
      # Also, if selection == 2 used to be elif selection ==3
      # Overall we changed the split from 80/20 to 50/50

      if selection == 0:
         train0.write(output)
      elif selection == 1:
         train1.write(output)
      elif selection == 2:
         train2.write(output)
      elif selection == 3:
         train3.write(output)
      else:
         train4.write(output)
      
   
   train0.close()
   train1.close()
   train2.close()
   train3.close()
   train4.close()
   

