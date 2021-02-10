import re
import string
import pickle

query = input()
(tree, tree_ans) = pickle.load( open( "pre_processed.p", "rb" ) )
now = 0
for j in query:
    if j == '*':
        break
    if j not in tree[now].keys():
        now = -1
        break
    now=tree[now][j]
if now==-1:
    print('Not Found')
else:
    print(tree_ans[now])