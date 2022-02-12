import sys
import os
from preprocess import load_data_set 
from Model import Model
import random

train = load_data_set('training')
test = load_data_set('test')

model = Model(train[0], train[1])

def calculate_scores(predict, actual): # given predicted array, and actual array. Return Avaraged F1
    tp = 0
    fp = 0
    fn = 0
    tn = 0    
    for i in range(len(predict)):
        if predict[i] == True and actual[i]==True:
            tp += 1
        elif predict[i] == False and actual[i]==True:
            fn += 1
        elif predict[i] == True and actual[i]==False:
            fp += 1
        elif predict[i] == False and actual[i]==False:
            tn += 1
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    F1 = 2*precision*recall / (precision + recall)
    
    tp, tn = tn, tp
    fp, fn = fn, fp

    precision2 = tp/(tp+fp)
    recall2 = tp/(tp+fn)
    F12 = 2*precision2*recall2 / (precision2 + recall2)
    
    return (F1+F12)/2
    
def calculate_test(model, legismate, verbose): # legismate is true, when testing scores for legismate
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for i in test[0]:
        if model.predict(i):
            tp += 1
        else:
            fn += 1

    for i in test[1]:
        if model.predict(i):
            fp += 1
        else:
            tn += 1
    
    if legismate: #
        tp, tn = tn, tp
        fp, fn = fn, fp


    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    F1 = 2*precision*recall / (precision + recall)
    if verbose:
        print('Precision: ', precision) # not avarage
        print('recall: ', recall)
        print('F-Measure: ', F1)

    return precision/2, recall/2, F1/2

def avg_res(model, verbose): # macro-avarage scpres
    p, r, f = calculate_test(model, True, 0)
    p2, r2, f2 = calculate_test(model, False, 0 )
    p+=p2
    r+=r2
    f+=f2
    if verbose:
        print('Precision: ', p)
        print('recall: ', r)
        print('F-Measure: ', f)
    return p,r,f


def scores(modelNum,verbose):
    model.setMutualInformation(100 if modelNum == 2 else 0)
    return avg_res(model,verbose)

def randomizationTest():
    model1 = Model(train[0], train[1])
    model2 = Model(train[0], train[1])
    model2.setMutualInformation(1000)

    diff = abs(scores(1,0)[2] - scores(2,0)[2])
    counter = 0
    R = 100 
    for i in range(R):
        predict1 = []
        predict2 = []
        actual = []
        for j in test[0]: # spams
            r1 = model1.predict(j)
            r2 = model2.predict(j)
            if random.randint(0,1) == 1:
                r1, r2 = r2, r1
            predict1.append(r1)
            predict2.append(r2)
            actual.append(True)
        for j in test[1]: # non-spams
            r1 = model1.predict(j)
            r2 = model2.predict(j)
            if random.randint(0,1) == 1:
                r1, r2 = r2, r1
            predict1.append(r1)
            predict2.append(r2)
            actual.append(False)
        if abs(calculate_scores(predict1,actual) - calculate_scores(predict2, actual))>diff:
            counter+=1
    p = (counter+1)/(R+1)

    print('Randomization Test result: ', p)




print("First version:")

print("\nResults for Class Spam:")
calculate_test(model, False, 1)

print("\nResults for Class Legismate:")
calculate_test(model, True, 1)

print("\nMacro-averaged:")
scores(1,1)
print('\n')



model.setMutualInformation(100)
print("---------\n\nSecond version:")
print("\nResults for Class Spam:")
calculate_test(model, False, 1)

print("\nResults for Class Legismate:")
calculate_test(model, True, 1)

print("\nMacro-averaged:")
scores(2,1)
print('\n')

randomizationTest()