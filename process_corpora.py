import os, re, sys
from nltk import word_tokenize

s = int(sys.argv[1]) - 1

with open('short_inputs.txt', 'rb') as f:
    this_set = f.read().split('\n')[s].split()

root  = os.getcwd()
os.chdir('children')

corpora_fn = os.listdir(os.getcwd())

all_lines = []
for fn in corpora_fn:
    with open(fn, 'rb') as f:
        lines = f.read().decode('utf8').lower()

        # nltk tokenize
        tokens = word_tokenize(lines)

        # remove input words from corpus to avoid
        tokens_rm = [w for w in tokens if w not in this_set]

        # remove non-alphanumeric characters from list, leaving words with apostrophes inside and sentence-enders
        tokens_rm2 = [w for w in tokens if w.isalnum() or (len(w) > 2 and '\'' in w) or (w in ['.', '!', '?'])]

        # join tokens by spaces, and then split again by sentence-ender
        tokens_join = ' '.join(tokens_rm2)
        tokens_split = [t.strip() for t in re.split(r'\.|\?|\!', tokens_join) if len(t.strip()) > 0]

        all_lines += tokens_split

os.chdir(root)
with open('full_corpus.txt', 'wb') as f:
    for line in all_lines:
        f.write('%s\n' % line.encode('utf8'))