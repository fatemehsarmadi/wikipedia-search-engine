import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
from gensim.parsing.preprocessing import remove_stopwords

class Document:
    def __init__(self, id, url, content):
        self.id = id
        self.url = url
        self.content = content
        self.main_content = self.remove_unusable()
        
    # removing extra words and characters from the content of the document
    def remove_unusable(self):
        main = remove_stopwords(re.sub('[.,()[]]', '', self.content.lower()).replace("\'s", "").replace('’s', '')).split(' ')
        return main

class SE:
    def __init__(self):
        self.documents = [] # new documents are added to this list
        
    def add_doc(self, url):
        request = requests.get(url) # sending get request
        soup = BeautifulSoup(request.text, 'html.parser')
        parser = soup.select('.mw-parser-output > p:not(.mw-empty-elt)') # getting all content of the article
        if len(parser) == 0: # for articles without content
            output = ' '
        elif len(parser) >= 1: # for articles with one paragraph
            output = '{}'.format(re.sub('\[[\d]]', '', parser[0].text).replace('\n', '')) # separating reference numbers
            output += '\n'
        if len(parser) >= 2: # for articles with two paragraphs or more
            output += '{}'.format(re.sub('\[[\d]]', '', parser[1].text).replace('\n', '')) # separating reference numbers
        current_id = len(self.documents)
        for doc in self.documents: # assigning a unique id to the document
            if doc.id == current_id:
                current_id += 1
        d = Document(current_id, url, output) # create a new document
        self.documents.append(d) # add a new document to the list of documents
        
    def delete_doc(self, url):
        for doc in self.documents:
            # search for the input URL in the URL of all documents
            if doc.url == url:
                # delete the document from the list of documents
                self.documents.remove(doc)
                print(f'The document with ID {doc.id} was deleted')
                return
        print('There is no document with this url!')
        
    # finding all documents that contain a specific word
    def search(self, word):
        number = 0
        for doc in self.documents:
            # search word in all documents case-insensitively
            if re.search(word, doc.content, re.IGNORECASE):
                # printing documents containing the input word and their ids
                print('id: ', doc.id)
                print(doc.content + '\n---------')
                number += 1 # adding to the number of documents containing this word
        print(f'{number} documents contain "{word}"!')
        
    # finding the most frequent words in a document
    def most_repeated(self, id):
        for doc in self.documents:
            if doc.id == id:
                frequency = Counter(doc.main_content) # number of repetitions of each word
                words_frequency = {}
                # sorting the dictionary based on the number of occurrences of words
                sorted_keys = sorted(frequency, key = frequency.get, reverse = True)
                for w in sorted_keys:
                    words_frequency[w] = frequency[w]
                number = 0
                most_repeated_words = []
                # finding the three most repeated words
                for textword in words_frequency:
                    if(number < 3):
                        most_repeated_words.append(textword)
                        number += 1
                print(most_repeated_words)
                return
        print('There is no document with this id!')
        
    # finding the most frequent word in all documents
    def most_popular(self):
        all = []
        for doc in self.documents:
            # find all words in documents
            all += doc.main_content
        frequency = Counter(all)
        wordsFrequency = {}
        sorted_keys = sorted(frequency, key = frequency.get, reverse = True)
        # the most frequent word in the content of all documents
        return sorted_keys[0]