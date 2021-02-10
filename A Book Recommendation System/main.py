from book import Book
import sys
from multiprocessing import Pool
import math
import pickle
import myutils

RECOMMENDED_BOOK_CONSTANT = 18
THREAD_COUNT = myutils.THREAD_COUNT
PICKLE_FILE_NAME = "books_data.pickle"

def create_books(link):
    return Book(link)


'''
For 1800 links this process is 2 minutes
If thread count is greater than 25, I get banned from the server
time: 2 minutes 
'''
def download_links(links): 
    books = []
    with Pool(THREAD_COUNT) as p: # Be careful
        books = list(p.map(create_books, links))
    books = [i for i in books if i.done]
    print(len(books), ' books saved to pickle')
    return books

def file_path_pipeline():
    file_path = sys.argv[1]
    books = []

    with open(file_path) as file:
        books = download_links(file.readlines())
        
    #Calculate number of occurance of each word
    word_counts = {}
    for i in books:
        for w in i.description:
            try:
                word_counts[w] += 1
            except:
                word_counts[w] = 1

    # calculate tfidf scores for each book
    for book in books:
        book.calc_tf(word_counts, len(books))
    
    # Save it to pickle
    with open(PICKLE_FILE_NAME, "wb") as output_file:
        pickle.dump((books, word_counts), output_file)


def score(myBook):
    recomended_books = myBook.recommend_books()

    #PRECISION
    Precision_score = sum(map(lambda x: 1 if x[1].url in myBook.recomended_books else 0, recomended_books)) / len(recomended_books) 

    #AP@18
    AVG_score = 0
    num_correct_guess = 0
    for i in range(len(recomended_books)):
        if recomended_books[i][1].url in myBook.recomended_books:
            num_correct_guess += 1
            AVG_score += ( num_correct_guess / (i+1))
    if num_correct_guess>0:
        AVG_score /= num_correct_guess

    return Precision_score, AVG_score


'''
Reads pickle and gets books' data and word counts (to calculate given books tf-idf)
Prints title and authors for given book
'''
def link_pipeline():
    book_url = sys.argv[1]

    with open(PICKLE_FILE_NAME, "rb") as input_file: 
        myutils.books, word_counts = pickle.load(input_file)    

    myBook = Book(book_url)
    myBook.calc_tf(word_counts, len(myutils.books))
    Precision_score, AVG_score = score(myBook)
    recomended_books = myBook.recommend_books()
    for _, book in recomended_books:
        print('Title: ', book.title, ', Authors: ', book.authors)        
    print('Precision: ', Precision_score)
    print('Average Precision: ', AVG_score)



'''
Reads books from pickle
Calculates the Precision and AP@18 scores for each books and prints the mean of the scores
all process approximately 4 minutes
'''
def full_score():
    with open(PICKLE_FILE_NAME, "rb") as input_file:
        myutils.books, word_counts = pickle.load(input_file)    

    try_books = myutils.books
    scores = list(map(score, try_books))
    print(sum([i[0] for i in scores])/len(try_books) , sum([i[1] for i in scores])/len(try_books))
    


'''
needs one argument to run, 
if argument has http as a substring it runs link pipeline
if it is 'test' it calculates scores
'''
if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise "please give a file_path or url, or you can give test' as an argument which prints the avarage result"
    if 'test' == sys.argv[1]:
        full_score()
    elif 'http' in sys.argv[1]:
        link_pipeline()
    else:
        file_path_pipeline()


            

    
    