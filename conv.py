import re
import nltk
import string
import os
import sys
from os import walk

# read in input to make sure those words don't get left in corpus (2nd cmd line arg)
s = int(sys.argv[2]) - 1

with open('short_inputs.txt', 'rb') as f:
    this_set = f.read().split('\n')[s].split()

def tokenize(text):
    text = re.sub(r"([^\w\.\'\-\/,&])", r' \1 ', text)
    text = re.sub(r"(,\s)", r' \1', text)
    text = re.sub('\. *(\n|$)', ' . ', text)
    return text.split()
    
if len(sys.argv) < 2:
        sys.exit('Usage: %s [output file]' % sys.argv[0])
input_directory = "corpus"
if not os.path.exists(input_directory):
    sys.exit('ERROR: Input Directory %s was not found!' % input_directory)
files = []
for (dirpath, dirnames, filenames) in walk(input_directory):
    for file in filenames:
        str = os.path.join(dirpath, file)
        files.append(str)

output_file = sys.argv[1]
output = open(output_file, 'w')

for file in files:
    input = open(file, 'r')
    text = input.read().decode('utf8')
    input.close()
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
    tokens = list()

    for s in sentences:
        tokens.append(tokenize(s))
    for sent in tokens:
        valid_words = [i for i in sent if not all(j.isdigit() or j in string.punctuation for j in i)]
        final_words = list()
        for word in [w for w in valid_words if w not in this_set]:
            word = final_words.append(word.lstrip())
        output.write(" ".join(final_words).lower().encode('utf8')+"\n")
    print "Done WITH FILE: " + file
print "Done with All"
output.close()