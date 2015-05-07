# gets rid of counters, fixes cmudict.txt
import re

cmuProc = open('cmuProc.txt', 'w')

for line in open('cmudict.txt'):
	line = re.sub('\([0-9]\)', '', line) # get rid of counter nonsense
	fields = line.split()
	line = fields[0] + " x " + " ".join(fields[1:]) # gets all phonemes
	cmuProc.write(line + "\n")

cmuProc.close()
