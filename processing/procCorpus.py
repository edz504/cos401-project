import sys, os, re, nltk

# path = '/Users/irvinshuster/documents/20news-18828'
path = sys.argv[1]

for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        #print(os.path.join(root, name))
        fullPath = os.path.join(root, name)
        if name == '.DS_Store':
        	continue # annoying hack

        outProc = open(fullPath + '_proc', 'w')

        currLine = ''
        #punctuation = re.compile('^[:;!?]$')
        punctuation = '[.:;!?]'

        for line in open(fullPath):
        	#if re.search("(From:)|(Subject:)|(writes:)|(^In article)", line):
        	#	continue
        	tokens = line.split()
        	#t_final = []
        	for t in tokens:
        		# end of sentence
        		if re.search(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', t)
        		#if re.search(punctuation, t): # end of sentence
        			t = re.sub(punctuation, '', t)
        			currLine += t + "\n"
        			print currLine
        			outProc.write(currLine)
        			print 'here'
        			currLine = ''
        		else:
        			t = re.sub("[^0-9a-zA-Z'-]+", '', t)	
        			currLine += t + ' '

        outProc.close()
