import requests
import re
import string
import myutils
from collections import Counter
import math
from multiprocessing import Pool


class Book(object):
    """
    docstring
    """
    def calc_tf(self, word_counts, book_count):
        counter = Counter(self.description)
        count = len(self.description)
        for w in self.description:
            tf = counter[w] / count
            try:
                df = word_counts[w]
            except:
                df = 0 
            idf = math.log((book_count+1)/(df+1))
            self.tf_idf[w] = tf * idf

    def __init__(self, url):
        self.url = url.strip()
        try:
            page = requests.get(url) #get page
            self.description = myutils.tokenize(myutils.clear_tags(re.findall('<span id.*?</span>', page.text)[1])) # ADD TITLE?
            self.title = re.findall('temprop="name">\n.*\n</h1>', page.text)[0].split('\n')[1].strip()
            self.authors = [myutils.clear_tags(i) for i in re.findall('<span itemprop="name">.*?</span>', page.text)]
            self.recomended_books = [i[:-45] for i in re.findall('https.*\?from_choice=false&amp;from_home_module=false', page.text) ]
            self.genres = [myutils.clear_tags(i) for i in re.findall('<a class="actionLinkLite bookPageGenreLink" href="/genres/.*</a>', page.text) ]
            self.tf_idf = {}
            self.recomended_books = list(map(lambda x: x.strip(), self.recomended_books))
            self.done = True
        except:
            print("ERROR: ", url)
            self.done = False
#           print(page.text)
    def cossim_desc(self, bookB): # calculates the score for a given book
        xx = 0 
        yy = 0
        xy = 0
        for i in set(self.description + bookB.description):
            try:
                x = self.tf_idf[i]
            except:
                x = 0
            try:
                y = bookB.tf_idf[i]
            except:
                y = 0
            xx += x*x
            yy += y*y
            xy += x*y
        if xx == 0 or yy==0:
            score = 0
        else:
            score = xy/math.sqrt(xx*yy)
        score += sum(myutils.GENRE_POINT for i in bookB.genres if i in self.genres)
        return (score, bookB)
    
    #recommends books from the book list
    def recommend_books(self):
        book_scores = list(map(self.cossim_desc, myutils.books))
        book_scores.sort(key=lambda tup: tup[0], reverse = True)

        if book_scores[0][1].url.strip() == self.url.strip():
            book_scores.pop(0)
        book_scores = book_scores[:myutils.RECOMMENDED_BOOK_CONSTANT]
        
        return book_scores