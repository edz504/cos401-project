import sys, os, re, nltk, math
from nltk.probability import FreqDist, ConditionalProbDist, ConditionalFreqDist, ELEProbDist
from nltk.probability import LidstoneProbDist, WittenBellProbDist, SimpleGoodTuringProbDist
import pronunciation
from nltk.corpus.reader import cmudict
import pickle
import statistics
import operator
from nltk.corpus import wordnet_ic
from textstat.textstat import textstat
#brown_ic = wordnet_ic.ic('ic-brown.dat')
from nltk.corpus import wordnet as wn
stopwords = set(nltk.corpus.stopwords.words('english'))
file = sys.argv[1]
input = open(file, 'r')
lines = input.read().split('\n')
input.close()
if lines[-1] == "":
    del lines[-1]
values = open("SortedCompleteValues.txt","r").read().split("\n") #AoA 30k words
if values[-1] == "":
    del values[-1]
map = dict()
for value in values:
    word = value.split("\t")[0]
    map[word] = value.split("\t")[1:8]

results = dict()

POS_LIST = (['n','v'])

MIN_FAM = 100
MIN_CONC = 158
MIN_IMG = 129
MAX_AOA = 21
MIN_FREQ = 0.01

#HERE, we need to take care of the smoothing: Missing values
#FAM, IMG, CONC = 0
#Syllables: count it on our own
#Log Freq = 0.01
#AoA -> Max = 21
for line in lines:
    sem_scores = list()
    FAM_scores = list()
    IMG_scores = list()
    CONC_scores = list()
    NSYL_scores = list()
    FREQ_scores = list()
    AOA_scores = list()
    if line == "":
        break
    words = line.split(" ")
    n = len(words)
    for i in range(n):
        if (words[i] in stopwords or words[i]==''):
            continue
        #NOW WE GO FOR THE REST OF THE SCORING
        if (words[i] in map):
            if (float(map[words[i]][1]) == 0):
                FAM_scores.append(MIN_FAM)
            else:
                FAM_scores.append(float(map[words[i]][1]))
                
            if (float(map[words[i]][2]) == 0):
                IMG_scores.append(MIN_IMG)
            else:
                IMG_scores.append(float(map[words[i]][2]))
                
            if (float(map[words[i]][3]) == 0):
                CONC_scores.append(MIN_CONC)
            else:
                CONC_scores.append(float(map[words[i]][3]))
                
            if (float(map[words[i]][4]) == 0):
                NSYL_scores.append(textstat.syllable_count(words[i]))
            else:
                NSYL_scores.append(float(map[words[i]][4]))
                
            if (float(map[words[i]][5]) == 0):
                FREQ_scores.append(MIN_FREQ)
            else:
                FREQ_scores.append(float(map[words[i]][5]))
                
            if (float(map[words[i]][6]) == 0):
                AOA_scores.append(MAX_AOA)
            else:
                AOA_scores.append(float(map[words[i]][6]))
                
        else :
            FAM_scores.append(MIN_FAM)
            IMG_scores.append(MIN_IMG)
            CONC_scores.append(MIN_CONC)
            NSYL_scores.append(textstat.syllable_count(words[i]))
            FREQ_scores.append(MIN_FREQ)
            AOA_scores.append(MAX_AOA)
            #FIND SOMETHING TO DO TO THOSE WORDS NOT IN THE 25K words -> take median of the other values?
        if (wn.synsets(words[i]) == []):
            continue
        for j in range(i+1, n):
            if (words[j] in stopwords or words[j]=='' or wn.synsets(words[j]) == []):
                continue
            #print words[i],words[j]
            a = wn.synsets(words[i])
            b = wn.synsets(words[j])
            #score = max(a[i].wup_similarity(b[j]) for i in range(len(a)) for j in #range(len(b)))
            #LIN, JCN, RES, LCH require same POS Tag which we could impose: the first 3 require a corpus IC: like genesis or brown or something
            partial_score = 0
            for c in range(len(a)):
                for d in range(len(b)):
                    partial_score = max(a[c].path_similarity(b[d]),b[d].path_similarity(a[c])) #Between 0 and 1
                    #partial_score = max(a[c].wup_similarity(b[d]),b[d].wup_similarity(a[c]))
                    #if (a[c].pos() == b[d].pos() and a[c].pos() in POS_LIST):
                        #IC Methods are limited to Nouns\Verbs | The Similarity metods are not necessarily commutative
                        #partial_score = max(a[c].lin_similarity(b[d], brown_ic),b[d].lin_similarity(a[c], brown_ic))
                        #partial_score = max(a[c].jcn_similarity(b[d], brown_ic),b[d].jcn_similarity(a[c], brown_ic))
                        #partial_score = max(a[c].res_similarity(b[d], brown_ic),b[d].res_similarity(a[c], brown_ic))
                        #partial_score =  max(a[c].lch_similarity(b[d]), b[d].lch_similarity(a[c]))
                    sem_scores.append(partial_score)
    sem_scores = [0 if v is None else v for v in sem_scores]
    if (sem_scores == []):
        med = 0
    #    mean = statistics.mean(scores)
    #    print line, med, mean
    else:
        print sem_scores
        med = statistics.median(sem_scores)
    #    mean = 0
    med_FAM = statistics.median(FAM_scores)
    med_IMG = statistics.median(IMG_scores)
    med_CON = statistics.median(CONC_scores)
    med_NSYL = statistics.median(NSYL_scores)
    med_FREQ = statistics.median(FREQ_scores)
    med_AOA = statistics.median(AOA_scores)
    results[line] = (med, med_FAM, med_IMG, med_CON, med_NSYL, med_FREQ, med_AOA)

#----------------------------PHONETIC SCORES:

pathModelPickle = "BigramModel.p"
pathSylModelPickle = "PhonemeModel.p"
pathMnemonics = sys.argv[1]

#pathCorpus = "corpus.txt"
#pathMnemonics = "test.txt"
#pathCorpusSyl = "corpusTmp.txt"

mnemonics = []
mnemSyl = []
for line in open(pathMnemonics):
    mnemonics.append(line)

c = cmudict.CMUDictCorpusReader('/home/vagrant/gocode/src/github.com/poptip/score', 'cmuProc.txt')
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
proba = dict()
prob1 = 0
prob2 = 0

cpdist = pickle.load(open(pathModelPickle, "rb"))
cpdistSyl = pickle.load(open(pathSylModelPickle, "rb"))

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
    prob1 = log_prob
    words = mnemonics[i].split()
    for idx, word in enumerate(words):
        if idx == 0:
            condition = 'start'
        else:
            condition = words[idx-1]
        log_prob += math.log(cpdist[condition].prob(word))
        prob *= cpdist[condition].prob(word)
    prob2 = log_prob
    print ("mnemonic: " + mnemonics[i].strip())
    print ("log prob: " + str(log_prob))
    print ("prob: " + str(prob))
    proba[lines[i]] = (prob1, prob2)
    print i

 
#----------------------------------------    
output = open("results.txt","w")
out = ""
for line in results:
    out = out + line + "\t" + str(results[line][0]) + "\t" + str(results[line][1]) + "\t" + str(results[line][2]) + "\t" + str(results[line][3]) + "\t" + str(results[line][4]) + "\t" + str(results[line][5]) + "\t" + str(results[line][6]) + "\t" + str(proba[line][0]) + "\t" + str(proba[line][1])+ "\n"
    
output.write(out)
output.close()