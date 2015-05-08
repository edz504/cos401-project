## Pickles the probability models for easy access
import sys, os, re, nltk, math
from nltk.probability import FreqDist, ConditionalProbDist, ConditionalFreqDist, ELEProbDist
from nltk.probability import LidstoneProbDist, WittenBellProbDist, SimpleGoodTuringProbDist
import pronunciation
from nltk.corpus.reader import cmudict
import pickle

pathCorpus = sys.argv[1]
pathCorpusSyl = sys.argv[2]

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

cpdist = ConditionalProbDist(cfdist, ELEProbDist, cfdist.N()+1)
cpdistSyl = ConditionalProbDist(cfdistSyl, ELEProbDist, cfdistSyl.N()+1)

pickle.dump(cpdist, open('BigramModel.p', "wb"))
pickle.dump(cpdistSyl, open('PhonemeModel.p', "wb"))


