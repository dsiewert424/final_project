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
    
def set_genre(id, cur, conn):
    genre = ""
    if id == 1:
        genre = "Drama"
        cur.execute("INSERT OR IGNORE INTO Genres (genre_id, genre) VALUES (?,?)",(id, genre))
        conn.commit()
    elif id == 2:
        genre = "Action"
        cur.execute("INSERT OR IGNORE INTO Genres (genre_id, genre) VALUES (?,?)",(id, genre))
        conn.commit()
    elif id == 3:
        genre = "Mystery"
        cur.execute("INSERT OR IGNORE INTO Genres (genre_id, genre) VALUES (?,?)",(id, genre))
        conn.commit()
    elif id == 4:
        genre = "Comedy"
        cur.execute("INSERT OR IGNORE INTO Genres (genre_id, genre) VALUES (?,?)",(id, genre))
        conn.commit()
    elif id == 5:
        genre = "Biography"
        cur.execute("INSERT OR IGNORE INTO Genres (genre_id, genre) VALUES (?,?)",(id, genre))
        conn.commit()
    elif id == 6:
        genre = "Adventure"
        cur.execute("INSERT OR IGNORE INTO Genres (genre_id, genre) VALUES (?,?)",(id, genre))
        conn.commit()
    elif id == 7:
        genre = "Horror"
        cur.execute("INSERT OR IGNORE INTO Genres (genre_id, genre) VALUES (?,?)",(id, genre))
        conn.commit()
    elif id == 8:
        genre = "Crime"
        cur.execute("INSERT OR IGNORE INTO Genres (genre_id, genre) VALUES (?,?)",(id, genre))
        conn.commit()
    elif id == 9:
        genre = "Animation"
        cur.execute("INSERT OR IGNORE INTO Genres (genre_id, genre) VALUES (?,?)",(id, genre))
        conn.commit()

def prompt_user():
    i = input("Would you like to insert 25 rows into movies.sqlite (Y/N)?")
    if (i == 'Y' or i == 'y'):
        return
    elif(i == 'N' or i == 'n'):
        print("Quitting program... ")
        exit()
    else:
        print("Unrecognized selection")

def get_data_from_url(soup, cur, conn):
    data_url = []
    
    #find container of movies
    movie_list = soup.find_all('div', class_='lister-item mode-advanced')

    count = 0
    
    for item in movie_list:
        caption = item.find('div', class_='lister-item-content')
        #title
        title_chunk = caption.find('h3')
        title = title_chunk.find('a').text.replace("\n", "")
        #genre
        genre_str = item.find('span', class_='genre').text.strip()
        genre_list = genre_str.split(",")
        genre = genre_list[0]
        
        if genre == "Drama":
            genre_id = 1
        elif genre == "Action":
            genre_id = 2
        elif genre == "Mystery":
            genre_id = 3
        elif genre == "Comedy":
            genre_id = 4
        elif genre == "Biography":
            genre_id = 5
        elif genre == "Adventure":
            genre_id = 6
        elif genre == "Horror":
            genre_id = 7
        elif genre == "Crime":
            genre_id = 8
        elif genre == "Animation":
            genre_id = 9

        set_genre(genre_id, cur, conn)

        #rating
        rating = float(item.find('div', class_='inline-block ratings-imdb-rating').text.strip())
        #profit
        gross = item.find('p', class_='sort-num_votes-visible').text
        gross_list = re.findall( r"\$(\d+\.\d+)M", gross)
        if len(gross_list) == 1:
            profit = gross_list[0]
        elif len(gross_list) == 0:
            profit = "None"

        cur.execute("INSERT OR IGNORE INTO ImdbStats (title, genre_id, rating, profit) VALUES (?,?,?,?)",(title, genre_id, rating, profit))
        conn.commit()
        count += 1
        if (count % 25 == 0):
            prompt_user()
            

def main():

    # Create table
    conn = sqlite3.connect('movies.sqlite')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ImdbStats (title TEXT PRIMARY KEY, genre_id INTEGER, rating REAL, profit REAL)')
    cur.execute('CREATE TABLE IF NOT EXISTS Genres (genre_id INTEGER PRIMARY KEY, genre TEXT)')

    # Task 1: Create a BeautifulSoup object and name it soup. Refer to discussion slides or lecture slides to complete this
    for num in [1, 51]:
        url = f'https://www.imdb.com/search/title/?title_type=feature&year=2010-01-01,2010-12-31&start={num}' 
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        get_data_from_url(soup, cur, conn)
    
if __name__ == "__main__":
    main()