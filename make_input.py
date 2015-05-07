import sys

s = int(sys.argv[1]) - 1

with open('short_inputs.txt', 'rb') as f:
    sets = f.read().split('\n')

i = 0
with open('fst/mn.fst', 'wb') as f:
    for w in sets[s].split():
        f.write('%d %d %s\n' % (i, i + 1, w[0]))
        i += 1
    f.write('%d\n' % i)
