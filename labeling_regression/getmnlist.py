import pandas as pd

with open('googleform.csv', 'rb') as f:
    lines = f.read().split('\n')

mn_list = lines[0].split(',')
mns = [l[l.find('[') + 1:l.find(']')] for l in mn_list if '[' in l]

with open('mn_list_from.txt', 'wb') as f:
    for mn in mns:
        f.write('%s\n' % mn)

names = [l.split(',')[len(l.split(',')) - 1] + ' Borda' for l in lines[1:]]
vote_df = pd.DataFrame(index=mns, columns=names)
N = 10

i = 0
for vote in lines[1:]:
    vote_df[vote_df.columns[i]] = [(N - int(v)) for v in vote.split(',')[1:171]]
    i += 1

y = vote_df.sum(axis=1)
y.to_csv('borda_y.csv')