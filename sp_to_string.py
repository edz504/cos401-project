import sys 

inp = sys.argv[1]
k = sys.argv[2]

with open('mn/i%sk%s.tfst' % (inp, k), 'rb') as f:
    lines = [l.split() for l in f.read().split('\n') if len(l) > 0]

# all arcs from 0 
start_arcs = []
arc_dict = {}
for l in lines:
    if int(l[0]) == 0:
        start_arcs.append((int(l[1]), l[2], float(l[4])))
    else:
        if len(l) > 2:
            arc_dict[int(l[0])] = (int(l[1]), l[2], float(l[4]))
        else:
            arc_dict[int(l[0])] = float(l[1])

mns = []
for s in start_arcs:
    this_mn = s[1]
    this_lp = s[2]
    curr = s[0]
    while isinstance(arc_dict[curr], tuple):
        this_mn += ' ' + arc_dict[curr][1]
        this_lp += arc_dict[curr][2]
        curr = arc_dict[curr][0]

    this_lp += arc_dict[curr]

    mns.append((this_mn, this_lp))

with open('mn/i%sk%s.txt' % (inp, k), 'wb') as f:
    for mn in mns:
        f.write('%s, %f\n' % (mn[0], mn[1]))