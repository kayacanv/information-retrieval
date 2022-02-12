import os
import string

def clean_text(text): # removes punctuations
    return text.lower().translate(str.maketrans('','',string.punctuation))

def tokenize(text): # gets text  and returns array of tokenized words
    words = clean_text(text).split() 
    answer = []

    for w in words:
#        if w not in stop_words:
        answer.append(w)
    return answer


def readFiles(fileList):
    result = []
    for i in fileList:
        with open(i) as file:
            result.append(tokenize(file.read()))
    return result

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def load_data_set(data_type): #type "train" "test"
    legitimate = sorted(list(filter(lambda x: x.endswith('.txt'), listdir_fullpath(os.path.join(os.getcwd(), 'dataset/' + data_type + '/legitimate/')))))
    spam = sorted(list(filter(lambda x: x.endswith('.txt'), listdir_fullpath(os.path.join(os.getcwd(), 'dataset/' + data_type + '/spam/')))))
    return readFiles(legitimate) , readFiles(spam)
