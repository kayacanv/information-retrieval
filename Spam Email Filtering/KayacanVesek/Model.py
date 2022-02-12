from collections import Counter
import math 

class Model(object):
    
    def __init__(self, spams, legis):
        self.vocabulary = Counter(z for x in [spams, legis] for y in x for z in y) 
        self.spamsCounter= Counter(y for x in spams for y in x) 
        self.legisCounter= Counter(y for x in legis for y in x) 
        self.spamProb = 0.5
        self.legisProb = 0.5
        self.vocSize = len([z for x in [spams, legis] for y in x for z in y])
        self.spamWordsCount = len([z for x in [spams] for y in x for z in y])
        self.legisWordsCount = len([z for x in [legis] for y in x for z in y])
        self.alpha = 1
        self.k=0
        self.discWords = self.vocabulary
        
        
    def getIvalue(self, word):
        tmp = [[self.legisWordsCount - self.legisCounter[word] , self.spamWordsCount - self.spamsCounter[word] ] , [ self.legisCounter[word] ,  self.spamsCounter[word]]  ]
        ans = 0
        all_sum = 0
        for i in range(2):
            for j in range(2):
                all_sum+=tmp[i][j]
        for i in range(2):
            for j in range(2):
                dom = (tmp[i][j] + tmp[i][j ^ 1]) * (tmp[i][j] + tmp[i ^ 1][j])
                if(all_sum * tmp[i][j] / dom == 0):
                    continue
                ans += tmp[i][j] * math.log2(all_sum * tmp[i][j] / dom ) /all_sum
        return ans

    def spamPofWord(self, word): # spam probabilitsy of word P(W | S) 
       return (self.spamsCounter[word] + self.alpha) / (self.spamWordsCount + self.alpha * self.vocSize)

    def legisPofWord(self, word):
       return (self.legisCounter[word] + self.alpha) / (self.legisWordsCount + self.alpha * self.vocSize)

    def PofWord(self, word):
        if self.vocabulary[word] < 1:
            return 1, 1
        return self.spamPofWord(word) , self.legisPofWord(word)

    def setMutualInformation(self, k): # disable by making 0, use most k words
        self.k = k
        if k==0:
            self.discWords = self.vocabulary
            return 

        l = []
        for i in self.vocabulary:
            l.append( (i, self.getIvalue(i)) )
        l.sort(key=lambda item: (item[1], item[0]), reverse=True)
        self.discWords = set(i[0] for i in l[:k])
    
    def predict(self, text): # returns true if it is spam
        spamP = math.log(self.spamProb)
        legisP = math.log(self.legisProb)
        for i in text:
            if self.k > 0 and i not in self.discWords:
                continue
            x,y = self.PofWord(i)
            spamP += math.log(x)
            legisP += math.log(y)
        if spamP > legisP:
            return True 
        return False
            
