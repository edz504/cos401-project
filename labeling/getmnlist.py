with open('googleform.csv', 'rb') as f:
    lines = f.read().split('\n')

mn_list = lines[0].split(',')
mns = [l[l.find('[') + 1:l.find(']')] for l in mn_list if '[' in l]

with open('mn_list_from.txt', 'wb') as f:
    for mn in mns:
        f.write('%s\n' % mn)