from SingleDataAnalysis import *
import matplotlib.pyplot as plt

class MultiDataAnalyzer:
	'''Creates multiple single data analyzers and then combines their data using
	   a specified metric for the purpose of simplified output and graphing'''

	def __init__(self,IDs):
		'''Initializes all needed data to be printed out or graphed'''
		self.IDs=IDs

		#The texts used in the study
		self.textSources=['1ALexical', '1BLexical', '2ALexical', '2BLexical', '3ALexical', '3BLexical', '4ALexical', '4BLexical', '1ASemantics', '1BSemantics', '2ASemantics', '2BSemantics', '3ASemantics', '3BSemantics', '4ASemantics', '4BSemantics', '1ASyntactic', '1BSyntactic', '2ASyntactic', '2BSyntactic', '3ASyntactic', '3BSyntactic', '4ASyntactic', '4BSyntactic']
		
		#The indices in each text where a problem spot was expected
		self.testIndices=[(19,20,19,20,'Lexical','1'),(49,50,49,50,'Lexical','1'),(95,96,95,96,'Lexical','1'),\
						  (23,24,23,24,'Lexical','2'),(43,44,43,44,'Lexical','2'),(88,89,88,89,'Lexical','2'),\
						  (21,22,21,22,'Lexical','3'),(35,36,35,36,'Lexical','3'),(75,76,75,76,'Lexical','3'),\
						  (19,20,19,20,'Lexical','4'),(63,64,63,64,'Lexical','4'),(80,81,80,81,'Lexical','4'),\
						  (9,10,9,10,'Semantics','1'),(59,60,59,60,'Semantics','1'),(92,93,92,93,'Semantics','1'),\
						  (27,28,27,28,'Semantics','2'),(77,78,77,78,'Semantics','2'),(93,94,93,94,'Semantics','2'),\
						  (21,22,21,22,'Semantics','3'),(52,53,52,53,'Semantics','3'),(85,86,85,86,'Semantics','3'),\
						  (31,32,31,32,'Semantics','4'),(65,66,65,66,'Semantics','4'),(94,95,94,95,'Semantics','4'),\
						  (46,47,48,49,'Syntactic','1'),(78,79,81,82,'Syntactic','1'),(110,111,115,116,'Syntactic','1'),\
						  (40,41,40,41,'Syntactic','2'),(73,74,74,75,'Syntactic','2'),(102,103,104,105,'Syntactic','2'),\
						  (17,18,18,19,'Syntactic','3'),(47,48,51,52,'Syntactic','3'),(88,89,93,94,'Syntactic','3'),\
						  (30,31,31,32,'Syntactic','4'),(61,62,63,64,'Syntactic','4'),(85,86,85,86,'Syntactic','4')]
		
		#List of single data analyzers
		self.rawData=self.getSingleDatum()

		#List of all words across all texts/users
		self.words=self.createMasterMapping()
		print "DONE WITH INIT"

	def getSingleDatum(self):
		'''Creates an array holding single data analyzers with the IDs given by self.IDs'''
		idData=[]
		for ID in self.IDs:
			idData.append(SingleDataAnalyzer(ID))
			print "DONE WITH "+str(ID)
		#If you want to add a threshhold variance each sda must exceed, do it here
		#Like this
		# variance=np.average([x.deviationMetric for x in idData])
		# idData=[x for x in idData if x.deviationMetric>variance]
		# print len(idData)
		return idData

	def createMasterMapping(self):
		'''Combines the data of the multiple SDAs to create an array of all words
		   across all texts/users where each words zscore is somehow a normalization
		   from all input users.'''
		dataStorer={}
		for sda in self.rawData:
			for word in sda.words:
				#Use try-except as it is substantially faster than if-else
				try:
					dataStorer[word].append(word.zscore)
				except KeyError:
						dataStorer[word]=[word.zscore]
		toReturn=dataStorer.keys()
		map(lambda x: x.combineZScores(dataStorer[x],np.average,np.std),toReturn)
		return toReturn

	def printFromText(self,textIdentifier):
		'''Allows you to just find all words which come from a specific text'''
		textData=[x for x in self.words if x.textSource.dictionaryKeyString==textIdentifier]
		return self.sortByIndex(textData)

	def sortByIndex(self,arrayOfWords):
		'''Sorts an array of words by there respective indices'''
		arrayOfWords.sort(key=lambda x: int(x.index))
		return arrayOfWords

	def compareWordsInIndex(self,aBeg,aEnd,bBeg,bEnd,textType,textNumber,toPrint=False):
		'''Allows you to compare words in A vs B texts at only specified indices,
		   useful if trying to compare problem spots.'''
		dataToReturn=[]
		aIdent,bIdent=textNumber+'A'+textType,textNumber+'B'+textType
		aData=[x for x in self.words if x.textSource.dictionaryKeyString==aIdent]
		self.sortByIndex(aData)
		bData=[x for x in self.words if x.textSource.dictionaryKeyString==bIdent]
		self.sortByIndex(bData)
		if toPrint:
			print aIdent
		for word in aData:
			if int(word.index) in range(aBeg,aEnd):
				dataToReturn.append(word)
				if toPrint:
					print "    "+word.printMetrics()
		if toPrint:
			print
			print bIdent
		for word in bData:
			if int(word.index) in range(bBeg,bEnd):
				dataToReturn.append(word)
				if toPrint:
					print "    "+word.printMetrics()
		if toPrint:	
			print
			print "----------------"
			print
		return dataToReturn

	def compareAcrossAllTexts(self,interval,toPrint=False):
		'''Checks all the problem spots across all texts for use in graphing'''
		dataToReturn=()
		i=interval
		for (aB,aE,bB,bE,tType,tNum) in self.testIndices:
			dataToReturn+=((self.compareWordsInIndex(aB-i,aE+i,bB-i,bE+i,tType,tNum,toPrint)),)
		return dataToReturn

	def graphWordByWord(self):
		'''Creates a word v. word comparison of A vs B texts, 3 subplots per graph,
		   one graph per text'''
		dataToGraph=self.compareAcrossAllTexts(0)
		for i in range(0,len(dataToGraph),3):
			#Three subplots per figure
			fig=plt.figure()
			textIdent=dataToGraph[i][0].textSource.category+" "+dataToGraph[i][0].textSource.number
			fig.canvas.set_window_title(textIdent)
			fig.suptitle(textIdent,fontsize=20)
			for j in range(3):
				#One subplot
				plt.subplot(1,3,j+1)
				#Only need one ylabel
				if j==0:
					plt.ylabel('ZScore of Word')
				pair=dataToGraph[i+j]
				words=[pair[0],pair[1]]
				data=[x.zscore for x in words]
				dataSTD=[x.zscoreSTD for x in words]
				dataLabels=[x.string for x in words]
				x=[0,1]
				plt.xticks(x,dataLabels,rotation=20)
				plt.errorbar(0,data[0],fmt='ro',yerr=dataSTD[0],elinewidth=7,markersize=35)
				plt.errorbar(1,data[1],fmt='bo',yerr=dataSTD[1],elinewidth=7,markersize=35)
				plt.xlim([-0.5,1.5])
		plt.show()

	def graphRangeByRange(self,interval):
		'''Graphs a range from both the A and B texts to demonstrate relative deviations
		   across trouble spots or in general'''
		dataToGraph=self.compareAcrossAllTexts(interval)
		for i in range(0,len(dataToGraph),3):
			fig=plt.figure()
			textIdent=dataToGraph[i][0].textSource.category+" "+dataToGraph[i][0].textSource.number
			fig.canvas.set_window_title(textIdent)
			fig.suptitle(textIdent,fontsize=20)
			for j in range(3):
				pairs=dataToGraph[i+j]
				aWords=[x.string for x in pairs if x.textSource.version=='A']
				bWords=[x.string for x in pairs if x.textSource.version=='B']
				aData=[x.zscore for x in pairs if x.textSource.version=='A']
				bData=[x.zscore for x in pairs if x.textSource.version=='B']
				axA=fig.add_subplot(3,1,j+1)
				axB=axA.twiny()
				map(lambda x: x.set_xlim(-1,(2*interval+1)),[axA,axB])
				axA.set_xlabel("A Version")
				axB.set_xlabel("B Version")
				axA.set_ylabel("ZScore of Word")
				axA.set_xticks(range(len(aWords)))
				axB.set_xticks(range(len(bWords)))
				axA.set_xticklabels(aWords,rotation=10)
				axB.set_xticklabels(bWords,rotation=10)
				axA.plot(range(len(aWords)),aData,"or-",label="A Data",linewidth=5,markersize=25)
				axB.plot(range(len(bWords)),bData,"ob-",label="B Data",linewidth=5,markersize=25)
				lines,labels=axA.get_legend_handles_labels()
				lines2,labels2=axB.get_legend_handles_labels()
				#axB.legend(lines+lines2,labels+labels2,loc=0)
				axA.tick_params(direction='out',pad=-30)
				axB.tick_params(direction='out',pad=-30)
		plt.show()

	def getTypeData(self):
		'''Prints trouble words nicely'''
		troubleWords=self.compareAcrossAllTexts(0)
		for i in range(0,len(troubleWords),12):
			typeData=troubleWords[i:i+12]
			aWords=[x[0] for x in typeData]
			bWords=[x[1] for x in typeData]
			aData=[x.zscore for x in aWords]
			bData=[x.zscore for x in bWords]
			aMetric=np.median(aData)
			aSTD=mad(aData)
			bMetric=np.median(bData)
			bSTD=mad(bData)
			print typeData[0][0].textSource.category
			print "  A: "+"%.4f"%aMetric+"    "+"%.4f"%aSTD
			print "  B: "+"%.4f"%bMetric+"    "+"%.4f"%bSTD
			print 



