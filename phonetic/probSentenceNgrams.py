# Outputs probabilities of each mnemonic (maybe should normalize, format..) - bigrams
# python probSentenceNgrams.py corpus.txt mnemonic corpusSyl.txt
import sys, os, re, nltk, math
from nltk.probability import FreqDist, ConditionalProbDist, ConditionalFreqDist, ELEProbDist
from nltk.probability import LidstoneProbDist, WittenBellProbDist, SimpleGoodTuringProbDist
import pronunciation
from nltk.corpus.reader import cmudict

pathCorpus = sys.argv[1]
pathMnemonics = sys.argv[2]
pathCorpusSyl = sys.argv[3]

mnemonics = []
mnemSyl = []
for line in open(pathMnemonics):
	mnemonics.append(line)

c = cmudict.CMUDictCorpusReader('/Users/irvinshuster/documents/401proj', 'cmuProc.txt')
cWords = c.words()
cDict = c.dict()

# process the mnemonic to have pronunciation
for idx, line in enumerate(mnemonics):
	words = line.strip().split()
	lineMod = ''
	for word in words:
		#word = word.upper()
		if word in cWords:
			lineMod += " ".join(cDict[word][0]) + "  " # first list (pronunciation)
		else: # last ditch effort - finds pronunciation online
			pr = pronunciation.Pronounce(words)
			for k,v in pr.p().iteritems():
				lineMod += v[1] + '  '
	mnemSyl.append(lineMod.strip())

#print mnemonics, len(mnemonics)
#print mnemSyl, len(mnemSyl)

corpus = []
for line in open(pathCorpus):
	corpus.append(line)

corpusSyl = []
for line in open(pathCorpusSyl):
	corpusSyl.append(line)

# frequencies (unigram) - unnecessary
#fdist = FreqDist()
cfdist = ConditionalFreqDist()
for line in corpus:
	words = line.split()
	for idx, word in enumerate(words):
		condition = ''
		if idx == 0:
			condition = 'start'
		else:
			condition = words[idx-1]
		cfdist[condition][word] += 1

cfdistSyl = ConditionalFreqDist()
for line in corpusSyl:
	words = line.split()
	for idx, word in enumerate(words):
		condition = ''
		if idx == 0:
			condition = 'start'
		else:
			condition = words[idx-1]
		cfdistSyl[condition][word] += 1

# conditional probability distribution (for bigrams)
# or, SimpleGoodTuringProbDist
cpdist = ConditionalProbDist(cfdist, ELEProbDist)
cpdistSyl = ConditionalProbDist(cfdistSyl, ELEProbDist)

for i,m in enumerate(mnemSyl):
	words = m.split()
	log_prob = 0 # do log prob
	prob = 1
	for idx, word in enumerate(words):
		if idx == 0:
			condition = 'start'
		else:
			condition = words[idx-1]
		log_prob += math.log(cpdistSyl[condition].prob(word))
		prob *= cpdistSyl[condition].prob(word)

	words = mnemonics[i].split()
	for idx, word in enumerate(words):
		if idx == 0:
			condition = 'start'
		else:
			condition = words[idx-1]
		log_prob += math.log(cpdist[condition].prob(word))
		prob *= cpdist[condition].prob(word)

	print ("mnemonic: " + mnemonics[i].strip())
	print ("log prob: " + str(log_prob))
	print ("prob: " + str(prob))

'''
for m in mnemonics:
	words = m.split()
	log_prob = 0 # do log prob
	prob = 1
	for idx, word in enumerate(words):
		if idx == 0:
			condition = 'start'
		else:
			condition = words[idx-1]
		log_prob += math.log(cpdist[condition].prob(word))
		prob *= cpdist[condition].prob(word)

	print ("mnemonic: " + m.strip())
	print ("log prob: " + str(log_prob))
	print ("prob: " + str(prob))
'''
