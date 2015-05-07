##############################################################
# finds all mnemonics for a string
# --need to implement where order doesn't matter
##############################################################

import sys, os, re, nltk
# python findMnemonics.py corpus.txt "[mnemonic] [true/false]"
path = sys.argv[1]
mnString = sys.argv[2]
mnemonic = sys.argv[2].split()
isOrdered = sys.argv[3]
mnLetters = {}
for idx,word in enumerate(mnemonic):
	mnLetters[idx] = mnemonic[idx][0].lower()
	# mnLetters contains all of the first letters

stopwords = set(nltk.corpus.stopwords.words('english'))
solutions = set()
'''
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        #print(os.path.join(root, name))
        fullPath = os.path.join(root, name)
        if "_proc" not in fullPath:
        	continue
'''
if isOrdered == 'true':
	for line in open(path):
		words = line.split()
		solveWords = ""
		currIndexMn = 0
		currStopCnt = 0
		for i in words:
			i = i.lower()
			if i in stopwords or (currIndexMn < len(mnLetters) and i[0] == mnLetters[currIndexMn]): 
			# same first letters, or a stopword

				if i[0] == mnLetters[currIndexMn]:
					currIndexMn += 1
					currStopCnt = 0
				else:
					currStopCnt += 1
				if currStopCnt > 2:
					solveWords = ""
					currIndexMn = 0
					currStopCnt = 0
				else:
					solveWords += i + " "
					if currIndexMn == len(mnLetters):
						solutions.add(solveWords)
						#print solveWords
						solveWords = "" # maybe comment out if ending with a stopword is ok
						currIndexMn = 0
			else:
				solveWords = ""
				currIndexMn = 0
else:
	for line in open(path):
		# remove one at a time
		currLetters = [] 
		for k,v in mnLetters.iteritems():
			currLetters.append(v)
		words = line.split()
		solveWords = ""
		currStopCnt = 0
		for i in words:
			i = i.lower()
			if i in stopwords or i[0] in currLetters: 
			# same first letters, or a stopword
				if i[0] in currLetters:
					currLetters.remove(i[0])
					currStopCnt = 0
				else:
					currStopCnt += 1
				if currStopCnt > 2:
					solveWords = ""
					currLetters = [] 
					for k,v in mnLetters.iteritems():
						currLetters.append(v)
					currStopCnt = 0
				else:
					solveWords += i + " "
					#print solveWords
					#print found
					#if all(f == True for f in found):
					if len(currLetters) == 0:	
						solutions.add(solveWords)
						#print solveWords
						solveWords = ""
						currLetters = [] 
						for k,v in mnLetters.iteritems():
							currLetters.append(v)
						currStopCnt = 0
			else:
				solveWords = ""
				currLetters = [] 
				currStopCnt = 0
				for k,v in mnLetters.iteritems():
					currLetters.append(v)

for m in solutions:
	if m.strip() != mnString: # not the mnemonic itself
		print m.strip()