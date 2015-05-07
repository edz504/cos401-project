# This just creates the pronunciation corpus
# python probSentSyl.py corpus.txt
import sys, os, re, nltk, math
from nltk.probability import FreqDist, ConditionalProbDist, ConditionalFreqDist, ELEProbDist
from nltk.probability import LidstoneProbDist, WittenBellProbDist, SimpleGoodTuringProbDist
import pronunciation
from nltk.corpus.reader import cmudict

pathCorpus = sys.argv[1]

sylCorpus = [] # not really syllables, but pronunciations
outSyl = open('corpusSyl.txt', 'w')
c = cmudict.CMUDictCorpusReader('/Users/irvinshuster/documents/401proj', 'cmuProc.txt')
cWords = c.words()
cDict = c.dict()

for line in open(pathCorpus):
	if len(line.split()) == 0:
		continue
	words = line.split()
	lineMod = ''
	for word in words:
		#word = word.upper()
		if word in cWords:
			lineMod += " ".join(cDict[word][0]) + "  " # first list (pronunciation)
		'''
		else:
			pr = pronunciation.Pronounce(words)
			for k,v in pr.p().iteritems():
				lineMod += v[1] + '  '
		'''
	#sylCorpus.append(lineMod.strip())

	#print line + lineMod.strip()
	outSyl.write(lineMod.strip() + "\n")

outSyl.close()

# really slow, try to use cmudict instead - with this as a fallback
#c = cmudict.CMUDictCorpusReader('/Users/irvinshuster/documents/401proj', 'cmudict.txt')
