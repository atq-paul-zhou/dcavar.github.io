#! /usr/bin/env python"""MIParser.py(C) 2004 by Damir Cavar, Giancarlo Schrementi, Paul Rodrigues (Indiana University)"""import sys, os.path, glob, string, re, cPickle, math__author__ = "Damir Cavar, Giancarlo Schrementi, Paul Rodrigues"__version__ = "0.1"functionWordsEN = ["A", "Abroad", "About", "Above", "Across", "After", "Again",	"Against", "Ago", "Ahead", "All", "Almost", "Alongside", "Already",	"Also", "Although", "Always", "Am", "Amid", "Amidst", "Among", "Amongst",	"An", "And", "Another", "Any", "Anybody", "Anyone", "Anything", "Anywhere",	"Apart", "Are", "Aren't", "Around", "As", "Aside", "At", "Away", "Back",	"Backward", "Backwards", "Be", "Because", "Been", "Before", "Beforehand",	"Behind", "Being", "Below", "Between", "Beyond", "Both", "But", "By",	"Can", "Can't", "Cannot", "Could", "Couldn't", "Dare", "Daren't", "Despite",	"Did", "Didn't", "Directly", "Do", "Does", "Doesn't", "Doing", "Don't",	"Done", "Down", "During", "Each", "Either", "Else", "Elsewhere", "Enough",	"Even", "Ever", "Evermore", "Every", "Everybody", "Everyone", "Everything",	"Everywhere", "Except", "Fairly", "Farther", "Few", "Fewer", "For",	"Forever", "Forward", "From", "Further", "Furthermore", "Had", "Hadn't",	"Half", "Hardly", "Has", "Hasn't", "Have", "Haven't", "Having", "He",	"Hence", "Her", "Here", "Hers", "Herself", "Him", "Himself", "His", "How",	"However", "If", "In", "Indeed", "Inner", "Inside", "Instead", "Into",	"Is", "Isn't", "It", "Its", "Itself", "Just", "Keep", "Kept", "Later",	"Least", "Less", "Lest", "Like", "Likewise", "Little", "Low", "Lower",	"Many", "May", "Mayn't", "Me", "Might", "Mightn't", "Mine", "Minus",	"Moreover", "Most", "Much", "Must", "Mustn't", "My", "Myself", "Near",	"Need", "Needn't", "Neither", "Never", "Nevertheless", "Next", "No",	"No-one", "Nobody", "None", "Nor", "Not", "Nothing", "Notwithstanding",	"Now", "Nowhere", "Of", "Off", "Often", "On", "Once", "One", "Ones",	"Only", "Onto", "Opposite", "Or", "Other", "Others", "Otherwise", "Ought",	"Oughtn't", "Our", "Ours", "Ourselves", "Out", "Outside", "Over", "Own",	"Past", "Per", "Perhaps", "Please", "Plus", "Provided", "Quite", "Rather",	"Really", "Round", "Same", "Self", "Selves", "Several", "Shall", "Shan't",	"She", "Should", "Shouldn't", "Since", "So", "Some", "Somebody", "Someday",	"Someone", "Something", "Sometimes", "Somewhat", "Still", "Such", "That",	"Than", "The", "Their", "Theirs", "Them", "Themselves", "Then", "There",	"Therefore", "These", "They", "Thing", "Things", "This", "Those", "Though",	"Through", "Throughout", "Thus", "Till", "To", "Together", "Too", "Towards",	"Under", "Underneath", "Undoing", "Unless", "Unlike", "Until", "Up", "Upon",	"Upwards", "Us", "Versus", "Very", "Via", "Was", "Wasn't", "Way", "We",	"Well", "Were", "Weren't", "What", "Whatever", "When", "Whence", "Whenever",	"Where", "Whereby", "Wherein", "Wherever", "Whether", "Which", "Whichever",	"While", "Whilst", "Whither", "Who", "Whoever", "Whom", "Whose", "Why",	"Will", "With", "Within", "Without", "Won't", "Would", "Wouldn't", "Yet",	"You", "Your", "Yours", "Yourself", "Yourselves" ]

TOKEN          = 0 # definition for type or token
TYPE           = 1

languageModel = "data.dat" # filename of language model

LEARNING      = 0          # learning from input activated = 1, deactivated = 0
DEBUG         = 1          # print debug messages = 1, be quite = 0
TAGSEP        = "/"        # seperator for token and tag

compiled=re.compile(r'(.*)\/(.*?)$');

class Data:
	"""Data structures for MI parser."""

	def __init__(self):
		"""Constructor for Data."""
		self.totoBigrams = {}		self.totyBigrams = {}		self.tytoBigrams = {}		self.tytyBigrams = {}
		self.totoLeft   = {} # key = token, value = list of bigrams with token left
		self.totoRight  = {} # key = token, value = list of bigrams with token right
		self.totyLeft   = {} # key = token, value = list of bigrams with token left
		self.totyRight  = {} # key = token, value = list of bigrams with token right
		self.tytyLeft   = {} # key = type, value = list of bigrams with token left
		self.tytyRight  = {} # key = type, value = list of bigrams with token right
		self.tytoLeft   = {} # key = type, value = list of bigrams with token left
		self.tytoRight  = {} # key = type, value = list of bigrams with token right
		self.tokens      = {}
		self.types       = {}
		self.counts      = {}
		self.counts["wordCnt"]     = 0 # wordCnt     = 0 # number of unigrams
		self.counts["bigramCnt"]   = 0 # number of bigrams
		self.counts["sentenceCnt"] = 0 # number of sentences
		#self.counts["totoLeft"]    = 0
		#self.counts["totoRight"]   = 0

class MIParser:	"""Mutual Information and Relative Entropy parser."""	def __init__(self, files):		"""Constructor of MIParser."""
		self.readMyData()
		if files[0] == "-t":	
			if DEBUG:
				print "Training phase"			for i in files[1:]:				for x in glob.glob(os.path.normcase(i)):
					if DEBUG:
						print "Training on:", x					self.getInput(x)
			self.dumpMyData()
		else:
			if DEBUG:
				print "Parsing phase"

			#self.dump()

			for i in files:
				for x in glob.glob(os.path.normcase(i)):
					if DEBUG:
						print "Parsing:", x					self.getParse(x)
			if LEARNING:
				self.dumpMyData()


	def readMyData(self):
		"""Unpickles the language model."""
		# reading back data
		if os.path.exists(languageModel):
			if DEBUG:
				print "Loading language model."
			try:				file = open(languageModel, "r")
				self.myData = Data()
				self.myData = cPickle.load(file)
			except IOError:
				file.close()
				print "Error: Cannot load language model!"
				self.myData = Data()
			except PickleError:
				print "Error: Cannot load language model!"
				file.close()
				self.myData = Data()
			else:
				if DEBUG:
					print "Language model loaded."
				file.close()
		else:
			self.myData = Data()

		self.totoBigrams = self.myData.totoBigrams		self.totyBigrams = self.myData.totyBigrams		self.tytoBigrams = self.myData.tytoBigrams		self.tytyBigrams = self.myData.tytyBigrams
		self.tokens      = self.myData.tokens
		self.types       = self.myData.types
		if DEBUG:
			print "Number of bigrams:", self.myData.counts["bigramCnt"]
			print "Number of unigrams:", self.myData.counts["wordCnt"]
			print "Number of sentences:", self.myData.counts["sentenceCnt"]

	def dumpMyData(self):
		"""Pickling data to languageModel."""
		if DEBUG:
			print "Dumping language model."
		try:
			file = open(languageModel, "w")
			cPickle.dump(self.myData, file)
		except IOError:
			file.close()
		except PickleError:
			print "Pickle error!!!"
			file.close()
		else:
			file.close()
		if DEBUG:
			print "Done."


	def getParse(self, fileName):
		"""Parses the files."""
		try: # try to read from the file			file = open(fileName, 'r')			for line in file.readlines():
				line = string.strip(line)
				if len(line) > 0:
					# automatically extending the language model
					words = string.split(line)
					if LEARNING:
						self.addBigrams(words)
						self.myData.counts["sentenceCnt"] += 1
					miparses = []
					reparses = []
					# one algorithm splits for every chunk at the lowest MI value
					mi, re = self.getSplitParse(words, TOKEN, TOKEN)
					miparses.append(mi)
					reparses.append(re)
					mi, re = self.getSplitParse(words, TOKEN, TYPE)
					miparses.append(mi)
					reparses.append(re)
					mi, re = self.getSplitParse(words, TYPE, TOKEN)
					miparses.append(mi)
					reparses.append(re)
					mi, re = self.getSplitParse(words, TYPE, TYPE)
					miparses.append(mi)
					reparses.append(re)
					print "Parses for:\t", line
					print "Token-Token:\t", miparses[0], "\n\t", reparses[0]
					print "Token-Type:\t",  miparses[1], "\n\t", reparses[1]
					print "Type-Token:\t",  miparses[2], "\n\t", reparses[2]
					print "Type-Type:\t",   miparses[3], "\n\t", reparses[3]
					# another algorithm joins the words in a bigram with the highest MI value
					#parses.append(self.getMIJoinParse(words, TOKEN, TOKEN))
					#parses.append(self.getMIJoinParse(words, TOKEN, TYPE))
					#parses.append(self.getMIJoinParse(words, TYPE, TOKEN))
					#parses.append(self.getMIJoinParse(words, TYPE, TYPE))
		except IOError: # on input-output error just quit			file.close()		else:			file.close()


	def getSplitParse(self, words, ltype, rtype):
		"""Returns a parse for a sentence that is based on TOKEN or TYPE elements in a bigram."""
		# find the lowest MI and cut there
		mis = []
		res = []
		# print words
		for i in range(len(words) - 1):
			#word1 = string.split(words[i], TAGSEP)
			#word2 = string.split(words[i + 1], TAGSEP)

			#brownsplit=re.match(r'(.*)\/(.*?)$',words[i]);
			#word1=(brownsplit.group(1),brownsplit.group(2));
			#brownsplit=re.match(r'(.*)\/(.*?)$',words[i + 1]);
			#word2=(brownsplit.group(1),brownsplit.group(2));

			brownsplit=compiled.match(words[i]);
			word1=[brownsplit.group(1), brownsplit.group(2)];
			brownsplit=compiled.match(words[i + 1]);
			word2=[brownsplit.group(1), brownsplit.group(2)];


			if len(word1[0]) == 0 or len(word1[1]) == 0 or len(word2[0]) == 0 or len(word2[1]) == 0:
				continue
			#if word1[0] in brownPunctuation:
			#	
			# lower case if function word
			if word1[0] in functionWordsEN:
				word1[0] = string.lower(word1[0])
			if word2[0] in functionWordsEN:
				word2[0] = string.lower(word2[0])
			# print word1, word2
			bigram = word1[ltype] + " " + word2[rtype]
			# mis.append(self.MI(bigram, ltype, rtype)) # MI old
			mis.append(self.MI2(bigram, ltype, rtype)) # MI old
			res.append(self.RE(bigram, ltype, rtype))
		return mis, res



	def getMIJoinParse(self, words, typeleft, typeright):
		""" """
		pass

	def REWoodoo(self):
		""" """
		pass


	def MIWoodoo(self):
		""" """
		pass


	def addToHash(self, entry, table):
		"""Does the grunt work of adding an entry to the hash tables."""
		if table.has_key(entry):
			table[entry] += 1
		else:
			table[entry] = 1


	def addUDHash(self, entry):
		"""Adds to the left and right hash tables."""
		# create the token-token left table
		if self.myData.totoLeft.has_key(entry[0]):
			if entry[2] in self.myData.totoLeft[entry[0]]:
				self.myData.totoLeft[entry[0]][0] += 1
			else:
				self.myData.totoLeft[entry[0]][0] += 1
				self.myData.totoLeft[entry[0]][1].append(entry[2])
		else:
			self.myData.totoLeft[entry[0]] = [ 1, [ entry[2] ] ]

		# create the token-type left table
		if self.myData.totyLeft.has_key(entry[0]):
			if entry[3] in self.myData.totyLeft[entry[0]]:
				self.myData.totyLeft[entry[0]][0] += 1
			else:
				self.myData.totyLeft[entry[0]][0] += 1
				self.myData.totyLeft[entry[0]][1].append(entry[3])
		else:
			self.myData.totyLeft[entry[0]] = [ 1, [ entry[3] ] ]

		# create the type-token left table
		if self.myData.tytoLeft.has_key(entry[1]):
			if entry[2] in self.myData.tytoLeft[entry[1]]:
				self.myData.tytoLeft[entry[1]][0] += 1
			else:
				self.myData.tytoLeft[entry[1]][0] += 1
				self.myData.tytoLeft[entry[1]][1].append(entry[2])
		else:
			self.myData.tytoLeft[entry[1]] = [ 1, [ entry[2] ] ]

		# create the type-type left table
		if self.myData.tytyLeft.has_key(entry[1]):
			if entry[3] in self.myData.tytyLeft[entry[1]]:
				self.myData.tytyLeft[entry[1]][0] += 1
			else:
				self.myData.tytyLeft[entry[1]][0] += 1
				self.myData.tytyLeft[entry[1]][1].append(entry[3])
		else:
			self.myData.tytyLeft[entry[1]] = [ 1, [ entry[3] ] ]

		# create the token-token right table
		if self.myData.totoRight.has_key(entry[2]):
			if entry[0] in self.myData.totoRight[entry[2]]:
				self.myData.totoRight[entry[2]][0] += 1
			else:
				self.myData.totoRight[entry[2]][0] += 1
				self.myData.totoRight[entry[2]][1].append(entry[0])
		else:
			self.myData.totoRight[entry[2]] = [ 1, [ entry[0] ] ]

		# create the token-type right table
		if self.myData.totyRight.has_key(entry[3]):
			if entry[0] in self.myData.totyRight[entry[3]]:
				self.myData.totyRight[entry[3]][0] += 1
			else:
				self.myData.totyRight[entry[3]][0] += 1
				self.myData.totyRight[entry[3]][1].append(entry[0])
		else:
			self.myData.totyRight[entry[3]] = [ 1, [ entry[0] ] ]

		# create the type-token right table
		if self.myData.tytoRight.has_key(entry[2]):
			if entry[1] in self.myData.tytoRight[entry[2]]:
				self.myData.tytoRight[entry[2]][0] += 1
			else:
				self.myData.tytoRight[entry[2]][0] += 1
				self.myData.tytoRight[entry[2]][1].append(entry[1])
		else:
			self.myData.tytoRight[entry[2]] = [ 1, [ entry[1] ] ]

		# create the type-type right table
		if self.myData.tytyRight.has_key(entry[3]):
			if entry[1] in self.myData.tytyRight[entry[3]]:
				self.myData.tytyRight[entry[3]][0] += 1
			else:
				self.myData.tytyRight[entry[3]][0] += 1
				self.myData.tytyRight[entry[3]][1].append(entry[1])
		else:
			self.myData.tytyRight[entry[3]] = [ 1, [ entry[1] ] ]


	def addBigrams(self, words):
		"""Creates a list of bigrams in an utterance. A bigram here is a list of
			two words (that include the tagging information). These bigrams are 
			then added to the bigram hash tables."""
		self.myData.counts["wordCnt"] += len(words)
		bigramList = []
		for i in range(len(words)-1):
			bigram = [words[i], words[i+1]]
			bigramList.append(bigram)
		self.myData.counts["bigramCnt"] += len(bigramList)
		for b in bigramList:
			# add the bigram to the tables
			#word1 = string.split(b[0], TAGSEP)
			#word2 = string.split(b[1], TAGSEP)
			brownsplit=compiled.match(b[0]);
			word1=[brownsplit.group(1), brownsplit.group(2)];
			brownsplit=compiled.match(b[1]);
			word2=[brownsplit.group(1), brownsplit.group(2)];

			#print "After the split:"
			#print word1
			#print word2

			# lower case if function word
			#if word1[TOKEN] in functionWordsEN:
			word1[TOKEN] = string.lower(word1[TOKEN])
			#if word2[TOKEN] in functionWordsEN:
			word2[TOKEN] = string.lower(word2[TOKEN])

			# add to directional hash tables
			self.addUDHash([ word1[TOKEN], word1[TYPE], word2[TOKEN], word2[TYPE] ])

			self.addToHash(word1[TOKEN], self.tokens)
			self.addToHash(word2[TOKEN], self.tokens)
			self.addToHash(word1[TYPE], self.types)
			self.addToHash(word2[TYPE], self.types)

			self.addToHash(word1[TOKEN]+" "+word2[TOKEN], self.totoBigrams)
			self.addToHash(word1[TOKEN]+" "+word2[TYPE], self.totyBigrams)
			self.addToHash(word1[TYPE]+" "+word2[TOKEN], self.tytoBigrams)
			self.addToHash(word1[TYPE]+" "+word2[TYPE], self.tytyBigrams)

	def getInput(self, fileName):		""" Gets the input from a file and lowercases it and removes all the		    punctuation and then tokenizes it into a list of words and processes		    them in an incremental fashion.		    fileName = string		    addUtterance = strings, name of function that takes the utterance		      string as parameter"""		try: # try to read from the file			file = open(fileName, 'r')			for line in file.readlines():
				self.myData.counts["sentenceCnt"] += 1
				line = string.strip(line)
				if len(line) > 0:
					self.addBigrams(string.split(line))
		except IOError: # on input-output error just quit			file.close()			# pass		else:			file.close()


	def entropy(self, string):
		return math.log(26, 2) * len(string)


	def RE(self, bigram, ltype, rtype):
		"""Relative entropy is P1*log2(P1/P2) where here P1 is P(rightword)
			and P2 is P(right word | left word)."""
		frames = string.split(bigram)
		#print "bigram = ", bigram, frames
		if rtype == TOKEN:
			if self.tokens.has_key(frames[1]):
				P1 = float(self.tokens[frames[1]])/float(self.myData.counts["wordCnt"])
			else:
				return self.entropy(bigram)
		else:
			if self.types.has_key(frames[1]):
				P1 = float(self.types[frames[1]])/float(self.myData.counts["wordCnt"])
			else:
				return self.entropy(bigram)
		if ltype == TOKEN and rtype == TOKEN:
			if self.totoBigrams.has_key(bigram) and self.tokens.has_key(frames[0]):
				P2 = float(self.totoBigrams[bigram])/float(self.tokens[frames[0]])
			else:
				return self.entropy(bigram)
		elif ltype == TOKEN:
			if self.totyBigrams.has_key(bigram) and self.types.has_key(frames[0]):
				P2 = float(self.totyBigrams[bigram])/float(self.types[frames[0]])
			else:
				return self.entropy(bigram)
		elif rtype == TOKEN:
			if self.tytoBigrams.has_key(bigram) and self.tokens.has_key(frames[0]):
				P2 = float(self.tytoBigrams[bigram])/float(self.tokens[frames[0]])
			else:
				return self.entropy(bigram)
		else:
			if self.tytyBigrams.has_key(bigram) and self.types.has_key(frames[0]):
				P2 = float(self.tytyBigrams[bigram])/float(self.types[frames[0]])
			else:
				return self.entropy(bigram)

		RE = P1 * math.log(P1/P2, 2)

		return RE


	def MI(self, bigram, ltype, rtype):		"""Calculate the mutual information for bigram.			MI = log2 ( P(XY) / P(X) P(Y) )."""
		if ltype == TOKEN and rtype == TOKEN:
			bigrams  = self.totoBigrams
			unileft  = self.tokens
			uniright = self.tokens
		elif ltype == TOKEN and rtype == TYPE:
			bigrams = self.totyBigrams
			unileft = self.tokens
			uniright = self.types
		elif ltype == TYPE and rtype == TOKEN:
			bigrams = self.tytoBigrams
			unileft = self.types
			uniright = self.tokens
		elif ltype == TYPE and rtype == TYPE:
			bigrams = self.tytyBigrams
			unileft = self.types
			uniright = self.types
		mi = 0.0
		words = string.split(bigram)
		if bigrams.has_key(bigram):
			if unileft.has_key(words[0]):
				if uniright.has_key(words[1]):
					pxy = float(bigrams[bigram]) / float(self.myData.counts["bigramCnt"])
					px  = float(unileft[words[0]]) / float(self.myData.counts["wordCnt"])
					py  = float(uniright[words[1]]) / float(self.myData.counts["wordCnt"])
					mi = math.log(pxy / (px * py), 2)		return mi

	def MI2(self, bigram, ltype, rtype):		"""Calculate the mutual information for bigram.			MI = P(XY|X) log2 ( P(XY) / P(X) P(Y) )			P(XY|X) = num of bigrams XY over num bigrams with X left			Interested in MI left of X			Looking at bigrams with X in the left		"""		if ltype == TOKEN and rtype == TOKEN:
			leftbigrams  = self.myData.totoLeft
			rightbigrams = self.myData.totoRight
			bigrams      = self.totoBigrams
			lunigrams     = self.tokens
			runigrams     = self.tokens
		elif ltype == TOKEN and rtype == TYPE:
			leftbigrams  = self.myData.totyLeft
			rightbigrams = self.myData.totyRight
			bigrams      = self.totyBigrams
			lunigrams     = self.tokens
			runigrams     = self.types
		elif ltype == TYPE and rtype == TOKEN:
			leftbigrams  = self.myData.tytoLeft
			rightbigrams = self.myData.tytoRight
			bigrams      = self.tytoBigrams
			lunigrams     = self.types
			runigrams     = self.tokens
		elif ltype == TYPE and rtype == TYPE:
			leftbigrams  = self.myData.tytyLeft			rightbigrams = self.myData.tytyRight
			bigrams      = self.tytyBigrams
			lunigrams     = self.types
			runigrams     = self.types

		words = string.split(bigram)

		bigramcount = float(self.myData.counts["bigramCnt"])		tokencount  = float(self.myData.counts["wordCnt"])		# calculate right side MI of left unigram
		rightMI = 0.0
		unigram = words[0]
		if leftbigrams.has_key(unigram):
			for gram in leftbigrams[unigram][1]:				if bigrams.has_key(unigram + " " + gram):					pxyx = float(bigrams[unigram + " " + gram]) / float(leftbigrams[unigram][0])					pxy  = float(bigrams[unigram + " " + gram]) / bigramcount					if lunigrams.has_key(unigram):						px = float(lunigrams[unigram]) / tokencount					else:						continue					if runigrams.has_key(gram):						py = float(runigrams[gram]) / tokencount					else:						continue					rightMI += (pxyx * math.log(pxy / (px * py), 2))		# calculate left side MI of right unigram		leftMI = 0.0
		unigram = words[1]		if rightbigrams.has_key(unigram):			for gram in rightbigrams[unigram][1]:				if bigrams.has_key(gram + " " + unigram):					pxyx = float(bigrams[gram + " " + unigram]) / float(rightbigrams[unigram][0])					pxy  = float(bigrams[gram + " " + unigram]) / bigramcount					if lunigrams.has_key(gram):						px   = float(lunigrams[gram]) / tokencount					else:						continue					if runigrams.has_key(unigram):						py   = float(runigrams[unigram]) / tokencount					else:						continue					leftMI += (pxyx * math.log(pxy / (px * py), 2))
		# sum the values up and return		return leftMI + rightMI	def dump(self):		""" """
		#print "Token-token bigrams:"
		#for i in self.totoBigrams.keys():
		#	print i, self.totoBigrams[i]		#print "Token-type bigrams:"
		#for i in self.totyBigrams.keys():
		#	print i, self.totyBigrams[i]		#print "Type-token bigrams:"
		#for i in self.tytoBigrams.keys():
		#	print i, self.tytoBigrams[i]		#print "Type-type bigrams:"
		#for i in self.tytyBigrams.keys():
		#	print i, self.tytyBigrams[i]
		#for i in self.myData.totyRight.keys():
		#	print i, self.myData.totyRight[i]		print "Tokens:"
		for i in self.tokens.keys():
			print i, self.tokens[i]		print "Types:"
		for i in self.types.keys():
			print i, self.types[i]


if __name__ == "__main__":	myMIParser = MIParser(sys.argv[1:])	# myMIParser.dump()
