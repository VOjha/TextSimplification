class TextSource:
	'''This object holds the data corresponding to a single text source
	   from which a user may read from.'''

	def __init__(self,number,version,category,rawString):
		'''Initializes the various parameters of the text source'''
		#Defines characters which may constitute a "word"
		self.goodCharacters=list("abcdefghijklmnopqrstuvwxyz0123456789'")

		#Define various parameters describing a text
		self.number=number
		self.version=version
		self.category=category

		#A single variable for use in dictionary keys and checking equality
		self.dictionaryKeyString=number+version+category

		#The text of the passage, and its lowered version
		self.rawString=rawString
		self.text=self.rawString.lower()

		#A list which translate character index to word index within the text
		self.wordIndices=self.findWordIndexForString()

	def __eq__(self,other):
		'''Text Sources are equal if their various qualifiers are equal'''
		return self.dictionaryKeyString==other.dictionaryKeyString

	def findWordIndexForString(self):
		'''Given a string, creates a list of the same length as the string, where
		   each item in the list is 1:1 with the corresponding character in the string
		   and demarks the word index of the word containing that character in the overall
		   string'''
		'''Example input-output:
		   input: "haha! hmm, don't go!"
		   output: [1,1,1,1,-,-,2,2,2,-,-,3,3,3,3,3,-,4,4,-]'''

		string=self.text
		wordIndex=0
		indexString=[]
		startedWord=False
		for i in range(len(string)):
			character=string[i]
			if character in self.goodCharacters:
				indexString.append(str(wordIndex))
				startedWord=True
			else:
				indexString.append('-')
				#only iterates wordIndex if just left a word
				if startedWord:
					wordIndex+=1
				startedWord=False

		return indexString




