from itertools import permutations
import pickle

with open('full_corpus.txt', 'rb') as f:
    corp1 = f.read().split()
with open('nw_corpus.txt', 'rb') as f:
    corp2 = f.read().split()

with open('short_inputs.txt', 'rb') as f:
    inputs = f.read().split('\n')

firsts = [[''.join(p) for p in permutations(''.join([a[0] for a in i.split()]))] for i in inputs]

valids = [[a for a in v if a in corp1 or a in corp2] for v in firsts]

print [len(f) for f in firsts]
print [len(v) for v in valids]

pickle.dump(valids, open('valid_letters_mns.p', 'wb'))