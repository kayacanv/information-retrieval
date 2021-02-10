import os
import re
import string
import pickle
import json

#This is my tri structure
tree = []   # this one keeps the nodes and paths from this node
tree.append(dict()) 
tree_ans = []    # this one keeps the answers for this node, for example root has all the words as an answer
tree_ans.append([])
node = 0 ## number of nodes in trie
##########################

stopWords = [i.rstrip().casefold() for i in open('stopwords.txt', 'r', encoding='latin-1').readlines()]

index = {} #inverted index

cnt = 0
for i in range(22):
    input_path = 'reuters21578/reut2-0{}.sgm'.format('0'+str(i) if i<10 else i)
    with open(input_path, 'r', encoding='latin-1') as reader:
        data = reader.read().replace('\n', ' ')

    texts = re.findall("<TEXT(.*?)</TEXT>",  data)
    for text in texts:
        cnt += 1
        try:
            body = re.findall("<BODY(.*?)</BODY>",  text)[0]
        except:
            body = ''
        try:
            title = re.findall("<TITLE(.*?)</TITLE>",  text)[0]
        except:
            title = ''

        title = title.translate(str.maketrans(string.punctuation, len(string.punctuation)*' '))
        body = body.translate(str.maketrans(string.punctuation, len(string.punctuation)*' '))

        for word in set(((title + ' ' + body).casefold().split())):            
            if word not in stopWords: 

                # add word to inverted_index
                if word not in index:
                    index[word] = [cnt]
                else:
                    index[word].append(cnt)

                # add word to trie
                now = 0
                tree_ans[now].append(cnt)
                for j in word:
                    if j not in tree[now].keys():
                        node += 1
                        tree_ans.append([])
                        tree.append(dict())
                        tree[now][j] = node
                    now=tree[now][j]
                    tree_ans[now].append(cnt)

for i in range(len(tree_ans)):
    tree_ans[i] = sorted(set(tree_ans[i]))

with open('inverted_index.json', 'w') as outfile:
    json.dump(index, outfile)
    
pickle.dump( (tree, tree_ans), open( "pre_processed.p", "wb" ) )

s = "rm -rf reuters21578"
print(s)
os.system(s)
