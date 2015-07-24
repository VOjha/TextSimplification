import os
import numpy as np
from TextSource import *
from Word import *

class SingleDataAnalyzer:
	'''Transforms the text file sent off by the iPad app into usable data'''

	def __init__(self,ID):
		'''Given an ID, creates all the needed data from the textfile'''
		self.ID=ID

		#Directory of this file, to find the rawData
		self.directory=os.path.dirname( __file__ )

		#Characters which may constitute a word for use in splitString
		self.goodCharacters=list("abcdefghijklmnopqrstuvwxyz0123456789'")

		#The raw text file data transformed into usable python code
		#and a sorted version
		self.rawData=self.createDictFromString()
		self.cleanData=self.createSortedRaw() 

		#The average positive CPS per text for use in removing too negative cps
		self.forwardCPS=self.findAverageForwardCPS()

		#Text sources read by the user
		self.textSources=self.createTextSources()

		#Words with uncombined data
		self.unMappedWords=self.findAllWordFrames()

		#All words with normalized cps values
		self.words=self.mapWords()

		#The average metric values for this user per text
		self.findAverageMetrics()

	def createDictFromString(self):
		'''Opens the raw data (previously manually input) for the given
		   ID and evaluates it to a dictionary'''
		fileName=self.directory
		fileName+="/RawData/" + str(self.ID) + "-RawDataSet.txt"
		f=open(fileName,'r')
		retrievedString=f.read()
		f.close()
		retrievedDict=eval(retrievedString)
		'''The raw data is of the form:
		{'Num'+'Ver'+'Type': {
							  (time,(begIndex,endIndex)):(CPS,scaling), ...
							  }, ...
		}
		'''
		return retrievedDict

	def createSortedRaw(self):
		'''Creates the cleaned data set which will be used to generate the word mappings'''
		dataStorer={}

		for (identifiers,data) in self.rawData.items():
			cleanedData=[]
			for (timeAndIndex,cpsAndScaling) in data.items():
				cleanedData.append([timeAndIndex,cpsAndScaling])
			dataStorer[identifiers]=cleanedData

		for i in range(len(dataStorer.values())):
			'''The app does not generate new scrolling labels to save on memory issues.
			   Instead, it resets the text and resets to the zero position of the label.
			   This, however, means that for the first 0-0.6 seconds, the data will be incorrect
			   and non-valid. To correct this, we simply remove values from the time sorted dictionary
			   until the label is located at the zero position '''
			item=dataStorer.values()[i]
			#Sorts by time, so values are in time order
			item.sort()
			while True:
				if item[0][0][1][0]==0:
					#item[0][0][1][0] is the begIndex. If it is zero we are at the start position.
					break
				else:
					item.pop(0)

		return dataStorer

	def createTextSources(self):
		'''Converts the alltexts text file to an array of textSource objects'''
		fileName="allTexts.txt"
		f=open(fileName,'r')
		retrievedString=f.read()
		f.close()
		retrievedDict=eval(retrievedString)
		arrayOfTextSources=[]
		for (category,data) in retrievedDict.items():
			for (ident,rawString) in data.items():
				number=ident[0]
				version=ident[1]
				newText=TextSource(number,version,category,rawString)
				arrayOfTextSources.append(newText)
		return arrayOfTextSources

	def findAverageForwardCPS(self):
		'''Finds the average positive cps per text so that
		   later only appropriate cps values may be usedin averages'''
		forwardCPS={}
		for (ident,data) in self.rawData.items():
			forwardData=[x[0] for x in data.values() if x[0]>0]
			forwardCPS[ident]=np.average(forwardData)
		return forwardCPS

	def findAllWordFrames(self):
		'''Finds all whole words in a frame given by the begIndex and endIndex'''
		wordStorer=[]
		for textSource in self.textSources:
			#Try-except is substantially faster than if-else
			try:
				appData=self.cleanData[textSource.dictionaryKeyString]
				for ((time,(begIndex,endIndex)),(cps,scaling)) in appData:
					#If endIndex=0, we haven't started yet
					if endIndex==0:
						continue	
					#Raw string visible on screen at this point			
					textInFrame=textSource.text[begIndex:endIndex]
					#List of partial words on screen at given time
					partialsInFrame=self.splitString(textInFrame)
					#Partial words with their word indices
					annotatedPartials=self.mapIndexToWords(begIndex,endIndex,partialsInFrame,textSource)
					#Full words in frame, if enough partial word is in frame
					fullWordsInFrame=self.checkBoundaryPartials(textSource,begIndex,endIndex,annotatedPartials)
					lowDataWords=[]
					#Words are low data because they only come from one frame
					for (wordIndex,wordString) in fullWordsInFrame:
						lowDataWord=Word(wordString,textSource,wordIndex,cps)
						lowDataWords.append(lowDataWord)
					wordStorer.append(lowDataWords)
			except KeyError:
				continue
		return wordStorer

	def mapWords(self):
		'''Takes data from all frames and combines it to form 
		   the complete data set for each word for all frames it
		   occurs in.'''
		wordArray={}
		for frame in self.unMappedWords:
			#If the cps is slower than the negative average positive cps,
			#we assume the user was speeding backwards and not actually reading
			#so disregard that entire frame
			if frame[0].cpsArray[0]<(-self.forwardCPS[frame[0].textSource.dictionaryKeyString]):
				continue
			for unMappedWord in frame:
				#Try-except is MUCH faster than if-else here
				try:
					wordArray[unMappedWord]+=unMappedWord.cpsArray
				except KeyError:
					wordArray[unMappedWord]=unMappedWord.cpsArray					
		toReturn=wordArray.keys()
		map(lambda x: x.combineData(wordArray[x],np.median,np.std),toReturn)
		return toReturn

	def findAverageMetrics(self):
		'''Finds average metrics for each ID, where the average metric
		   may be specified by the tester'''
		wordCutoff=5
		cpsArray=[w.cps for w in self.words if int(w.index)>wordCutoff]

		#While defaulted to average and std, these may by changed to
		#np.median and mad respectively
		centralMetric=np.average
		deviationMetric=np.std

		self.centralMetric=centralMetric(cpsArray)
		self.deviationMetric=deviationMetric(cpsArray)
		map(lambda x: x.setNormedScore(self.centralMetric,self.deviationMetric),self.words)

	def checkBoundaryPartials(self,textSource,begIndex,endIndex,partials):
		'''Determines if a partial word is "on-screen", and if so
		   adds the entire word to the partials list. If not, removes the partial'''
		#Modifiers which determine how much of the word must be on screen
		exitingWordLengthModifier=2
		enteringWordLengthModifier=3
		if textSource.text[begIndex] in self.goodCharacters:
			masterWord=self.findMasterWord(begIndex,textSource.text)
			firstPartialString=partials[0][1]
			if len(firstPartialString*exitingWordLengthModifier)>=len(masterWord) or len(partials)==1:
				partials[0][1]=masterWord
			else:
				partials.pop(0)
		if textSource.text[endIndex-1] in self.goodCharacters:
			masterWord=self.findMasterWord(endIndex-1,textSource.text)
			firstPartialString=partials[-1][1]
			if len(firstPartialString*enteringWordLengthModifier)>=len(masterWord) or len(partials)==1:
				partials[-1][1]=masterWord
			else:
				partials.pop(-1)
		return partials		

	def findMasterWord(self,index,masterString):
		'''Given a character index referring to a character in the masterString, finds the
		   total word in the masterString which contains that character at that index'''
		lowerIndex=index
		upperIndex=index
		while masterString[lowerIndex] in self.goodCharacters and lowerIndex!=0:
			lowerIndex-=1
		while masterString[upperIndex] in self.goodCharacters and upperIndex!=len(masterString)-1:
			upperIndex+=1
		if masterString[lowerIndex] not in self.goodCharacters: 
			lowerIndex+=1
		if upperIndex==len(masterString)-1 and masterString[upperIndex] in self.goodCharacters:
			toReturn=masterString[lowerIndex:]
		else:
			toReturn=masterString[lowerIndex:upperIndex]
		return toReturn

	def mapIndexToWords(self,begIndex,endIndex,partials,textSource):
		'''For each word in partials, determines the word index'''
		for i in range(len(partials)):
			indexOfFragment=textSource.text.index(partials[i],begIndex,endIndex)
			'''begIndex must be incremented so as not to double count.
			   For instance consider the partial "stal a narr", containing the
			   truncated "partial", complete "a" and truncated "narrow". If
			   we attempted to find the word index of "a", without incrementing
			   begIndex, we would find the word index of "pedestal". The added
			   one accounts for on average 1 non-word character following each
			   word, taken to be a space.'''
			begIndex+=(len(partials[i])+1)
			partials[i]=[(textSource.wordIndices[indexOfFragment]),partials[i]]
		return partials			

	def splitString(self,string):
		'''Because the built in .split and even re.split both don't like having a lot 
		   of delimiters, this function takes a string a returns a list containing
		   each of the words, in order, in that list, where words are defined as being
		   solely composed of "goodCharacters"'''
		i=0
		begIndex=i
		listOfStrings=[]
		#If all characters are good, return one element list
		if all(characters in self.goodCharacters for characters in string):
			listOfStrings.append(string)
			return listOfStrings
		while i<len(string):
			if string[i] in self.goodCharacters:
				if i==len(string)-1:
					listOfStrings.append(string[begIndex:])
				i+=1
			else:
				if i!=begIndex:
					listOfStrings.append(string[begIndex:i])
				#keep iterating until you hit the start of a word
				while i!=len(string) and string[i] not in self.goodCharacters:
					i+=1
				begIndex=i
		return listOfStrings

def mad(data,axis=None):
	'''Finds the median absolute deviation of a set of data,
	   the equivalent of standard deviation for a median'''
	return np.median(np.absolute(data-np.median(data,axis)),axis)





