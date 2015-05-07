import sys 

fn = sys.argv[1]

with open(fn, 'rb') as f:
    lines = f.read()

words = list(set(lines.split()))
firsts = list(set(w[0] for w in words))

i = 1
with open('fst/v.fst', 'wb') as f:
    for w in words:
        f.write('0 0 %s %s\n' % (w[0], w))
    f.write('0\n')

with open('fst/v.isyms', 'wb') as f:
    f.write('<eps> 0\n')
    i = 1
    for first in firsts:
        f.write('%s %d\n' % (first, i))
        i += 1
