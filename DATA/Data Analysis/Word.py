import numpy as np

class Word:
	'''This object defines a word within a text, and all the various
	   metrics which may apply to that word'''

	def __init__(self,string,textSource,index,cps):
		'''Maps parameters given by iPad app to self qualities'''
		#The text of the word
		self.string=string

		#The text from which the word comes from, and word index in that text
		self.textSource=textSource
		self.index=index

		#A unique identifier describing each word
		self.identifier=self.string+self.textSource.dictionaryKeyString+self.index
		
		#An array holding the words (currently) singular cps
		self.cpsArray=[cps]

	def addNewData(self,otherWord):
		'''Given another word, assumed to have the same identifier
		   for performance sake, stores the new cps'''
		self.cpsArray+=otherWord.cpsArray

	def combineData(self,cpsArray,function,stdFunction):
		'''Given an array of cps, and functions to use upon
		   that array, creates metric values'''
		self.cpsArray=cpsArray
		self.cps=function(self.cpsArray)
		self.std=stdFunction(self.cpsArray)

	def setNormedScore(self,centralMetric,deviation):
		'''Finds the zscore of the word's zscore based on a 
		   given centralMetric function (mean or median), and a deviation
		   function either standard deviation for mean or average median
		   deviation. Note the term zscore here is thus used 
		   generally, and if not referring to a value derived 
		   from an average is not a "true" zscore'''
		self.zscore=(self.cps-centralMetric)/deviation

	def combineZScores(self,zScoreArray,function,stdFunction):
		'''Given an array of normalized "zscores" and two functions
		   with which to operate on it, altering self.zscore'''
		self.zscoreArray=zScoreArray
		self.zscore=function(zScoreArray)
		self.zscoreSTD=stdFunction(zScoreArray)

	def printMetrics(self):
		'''Nicely prints out the word and its constituent metrics'''
		toReturn=self.spaces(self.string,15)+self.spaces(self.index,5)+\
		self.spaces("%.4f"%self.zscore,8)+("%.4f"%self.zscoreSTD)
		return toReturn

	def spaces(self,string,numberOfSpaces):
		'''Gives appropriate spacing to a printed string'''
		return string+" "*(numberOfSpaces-len(string))

	def findTimeOnScreen(self,arrayOfTimes,lengthOfWord):
		'''NOTE: This is a depreciated function. During the 2015 summer
		   research term we ended up not using the time value for words.
		   However, if future research does wish to use it, this method
		   allows you to find how long a word was on screen given an array
		   of recorded times, and normalizes that time based on the word length.'''
		'''Given an array of times, finds the amount of consecutive time
		   a word appears on screen, allowing for multiple appearances
		   with an interim non-appearance period'''
		frameSize=10
		#2 and 3 are the reciprocal values of the fraction of the word
		#which must be visible on the screen for it to be recorded as
		#present for exiting and entering words respectivelyy h
		normalizingFactor=frameSize/(frameSize+np.floor(lengthOfWord/2)-np.floor(lengthOfWord/3))
		if len(arrayOfTimes)==1:
			return 0.2*normalizingFactor
		time=0
		startTime=arrayOfTimes[0]
		for i in range(1,len(arrayOfTimes)):
			if arrayOfTimes[i]-arrayOfTimes[i-1]<0.3:
				if i==len(arrayOfTimes)-1:
					time+=arrayOfTimes[i]-startTime
				continue
			time+=arrayOfTimes[i-1]-startTime+0.2
			startTime=arrayOfTimes[i]
		return time*normalizingFactor

	def __repr__(self):
		return str((self.index,self.string))

	def __eq__(self,other):
		return self.identifier==other.identifier

	def __hash__(self):
		return hash(self.identifier)




