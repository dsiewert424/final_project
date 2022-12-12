from xml.sax import parseString
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import string
import sys
import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

# Your name: Debby Chung
# Your student id: 24199350
# Your email: debchung@umich.edu
# List who you have worked with on this project: Dylan Siewert
    

# Task 2: Look at the Get the URL that links to webpage of universities with Olympic medal wins
# search for the url in the University of Michgian wikipedia page (in the third pargraph of the intro)
# HINT: You will have to add https://en.wikipedia.org to the URL retrieved using BeautifulSoup
def get_data_from_url(soup, cur, conn):
    data_url = []
    
    #find container of movies
    movie_list = soup.find_all('div', class_='lister-item mode-advanced')

    for item in movie_list:
        caption = item.find('div', class_='lister-item-content')
        #title
        title_chunk = caption.find('h3')
        title = title_chunk.find('a').text.replace("\n", "")
        correct_title = re.sub(r'[^a-zA-Z0-9\s]+', '', title).title()
        #genre
        genre_str = item.find('span', class_='genre').text.strip()
        genre_list = genre_str.split(",")
        genre = genre_list[0]
        print(genre)
        #rating
        rating = float(item.find('div', class_='inline-block ratings-imdb-rating').text.strip())
        #profit
        gross = item.find('p', class_='sort-num_votes-visible').text
        gross_list = re.findall( r"\$\d+\.\d+M", gross)
        if len(gross_list) == 1:
            profit = gross_list[0]
        elif len(gross_list) == 0:
            profit = "None"

        cur.execute("INSERT OR IGNORE INTO ImdbStats (title, genre, rating, profit) VALUES (?,?,?,?)",(correct_title, genre, rating, profit))


def main():

    # Create table
    conn = sqlite3.connect('movies.sqlite')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ImdbStats (title TEXT PRIMARY KEY, genre TEXT, rating REAL, profit TEXT)')

    # Task 1: Create a BeautifulSoup object and name it soup. Refer to discussion slides or lecture slides to complete this
    for num in [1, 51]:
        url = f'https://www.imdb.com/search/title/?title_type=feature&year=2010-01-01,2010-12-31&start={num}' 
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        get_data_from_url(soup, cur, conn)
    
    conn.commit()


#class TestAllMethods(unittest.TestCase):
    # def setUp(self):
    #     self.soup = BeautifulSoup(requests.get('https://en.wikipedia.org/wiki/University_of_Michigan').text, 'html.parser')

    # def test_link_nobel_laureates(self):
    #     self.assertEqual(getLink(self.soup), 'https://en.wikipedia.org/wiki/List_of_American_universities_with_Olympic_medals')


if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)