import json
import os
import requests
import sqlite3
import sys
import re
import time

api_key = 'ppGGP0asry3DGatQJSmad7k9CCJKru3S'


def get_2010_month_data(month_index, times_mentionned):
    request_url = f'https://api.nytimes.com/svc/archive/v1/2010/{month_index}.json?api-key={api_key}'
    response = requests.get(request_url)
    dic_data = response.json()

    # write_json(f'{month_name}.json', dic_data)
    for item in dic_data['response']['docs']:
        if (item['section_name'] == 'Movies'):
            
            # look at "snippet" section of articles and find all movie titles
            snippet = item['snippet']
            list_of_titles = re.findall(r'"(.*?)"', snippet)
            list_of_titles.extend(re.findall(r'\u201c(.*?)\u201d', snippet))

            for title in list_of_titles:
                # strip all chars that aren't letters or spaces, and capitalize title
                correct_title = re.sub(r'[^a-zA-Z0-9\s]+', '', title).title().replace("  ", " ")
                times_mentionned[correct_title] = times_mentionned.get(correct_title, 0) + 1


def insert_data(start_index, times_mentionned, cur, conn):
    finished = False
    if (start_index == 750):
        end_index = start_index + 26
        finished = True
    else:
        end_index = start_index + 25

    
    for item in range(start_index, end_index):
        cur.execute('INSERT OR IGNORE INTO TimesMentionned (movie_title, times_mentionned) VALUES (?,?)', (times_mentionned[item][0], times_mentionned[item][1]))
    conn.commit()
    return finished



def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    conn = sqlite3.connect('movies.sqlite')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS TimesMentionned (movie_title TEXT PRIMARY KEY, times_mentionned INTEGER)')


    times_mentionned = {}
    # month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    # for i in range(len(month_names)):
    #     get_2010_month_data(str(i), times_mentionned)
    #     print(f'Fetching data for {month_names[i]} 2010')
    #     print("________________________")


    print("Fetching NYT data from January 2010... ")
    get_2010_month_data("1", times_mentionned)
    print("________________________")

    print("Fetching NYT data from February 2010... ")
    get_2010_month_data("2", times_mentionned)
    print("________________________")

    print("Fetching NYT data from March 2010... ")
    get_2010_month_data("3", times_mentionned)
    print("________________________")

    print("Fetching NYT data from April 2010... ")
    get_2010_month_data("4", times_mentionned)
    print("________________________")

    print("Fetching NYT data from May 2010... ")
    get_2010_month_data("5", times_mentionned)
    print("________________________")

    print("Fetching NYT data from June 2010... ")
    get_2010_month_data("6", times_mentionned)
    print("________________________")

    print("Fetching NYT data from July 2010... ")
    get_2010_month_data("7", times_mentionned)
    print("________________________")

    print("Fetching NYT data from August 2010... ")
    get_2010_month_data("8", times_mentionned)
    print("________________________")

    print("Fetching NYT data from September 2010... ")
    get_2010_month_data("9", times_mentionned)
    print("________________________")

    print("Fetching NYT data from October 2010... ")
    get_2010_month_data("10", times_mentionned)
    print("________________________")

    print("Fetching NYT data from November 2010... ")
    get_2010_month_data("11", times_mentionned)
    print("________________________")

    print("Fetching NYT data from December 2010... ")
    get_2010_month_data("12", times_mentionned)
    print("________________________")


    print("Inserting data into movies.sqlite...")

    # convert times_mentionned to list of tuples
    new_database = []

    for item in times_mentionned:
        new_database.append((item, times_mentionned[item]))


    finished = False
    start_index = 0

    while(not finished):
        i = input("Would you like to insert 25 rows into movies.sqlite (Y/N)?")
        if (i == 'Y' or i == 'y'):
            finished = insert_data(start_index, new_database, cur, conn)
            start_index += 25
        elif(i == 'N' or i == 'n'):
            print("Quitting program... ")
            exit()
        else:
            print("Unrecognized selection")


    print("Finished getting NYT data.")

if __name__ == "__main__":
    main()