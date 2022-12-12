import json
import os
import requests
import sqlite3
import sys
import re

api_key = 'ppGGP0asry3DGatQJSmad7k9CCJKru3S'

def write_json(cache_filename, dict):

    with open(cache_filename, 'w') as json_file:
        json.dump(dict, json_file)
    pass


def get_2010_month_data(month_index, month_name, times_mentionned):
    request_url = f'https://api.nytimes.com/svc/archive/v1/2010/{month_index}.json?api-key={api_key}'
    response = requests.get(request_url)
    dic_data = response.json()
    write_json(f'{month_name}.json', dic_data)

    
    for item in dic_data['response']['docs']:
        if (item['section_name'] == 'Movies'):
            
            # look at "snippet" section of articles and find all movie titles
            snippet = item['snippet']
            list_of_titles = re.findall(r'"(.*?)"', snippet)
            list_of_titles.extend(re.findall(r'\u201c(.*?)\u201d', snippet))

            for title in list_of_titles:
                # strip commas and periods from title
                correct_title = re.sub(r'[^a-zA-Z0-9\s]+', '', title).title().replace("  ", " ")
                times_mentionned[correct_title] = times_mentionned.get(correct_title, 0) + 1

    return times_mentionned


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    conn = sqlite3.connect('movies.sqlite')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS TimesMentionned (movie_title TEXT PRIMARY KEY, times_mentionned INTEGER)')


    times_mentionned = {}
    # month_names = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    # for i in range(len(month_names)):
    #     get_2010_month_data(i, month_names[i], times_mentionned)
    #     print(f'Fetching data for {month_names[i].capitalize()} 2010')
    #     print("________________________")


    print("Fetching NYT data from January 2010... ")
    get_2010_month_data("1", "january", times_mentionned)
    print("________________________")

    print("Fetching NYT data from February 2010... ")
    get_2010_month_data("2", "february", times_mentionned)
    print("________________________")

    print("Fetching NYT data from March 2010... ")
    get_2010_month_data("3", "march", times_mentionned)
    print("________________________")

    print("Fetching NYT data from April 2010... ")
    get_2010_month_data("4", "april", times_mentionned)
    print("________________________")

    print("Fetching NYT data from May 2010... ")
    get_2010_month_data("5", "may", times_mentionned)
    print("________________________")

    print("Fetching NYT data from June 2010... ")
    get_2010_month_data("6", "june", times_mentionned)
    print("________________________")

    print("Fetching NYT data from July 2010... ")
    get_2010_month_data("7", "july", times_mentionned)
    print("________________________")

    print("Fetching NYT data from August 2010... ")
    get_2010_month_data("8", "august", times_mentionned)
    print("________________________")

    print("Fetching NYT data from September 2010... ")
    get_2010_month_data("9", "september", times_mentionned)
    print("________________________")

    print("Fetching NYT data from October 2010... ")
    get_2010_month_data("10", "october", times_mentionned)
    print("________________________")

    print("Fetching NYT data from November 2010... ")
    get_2010_month_data("11", "november", times_mentionned)
    print("________________________")

    print("Fetching NYT data from December 2010... ")
    get_2010_month_data("12", "december", times_mentionned)
    print("________________________")


    print("Inserting data into music.sqlite...")

    for item in times_mentionned:
        cur.execute('INSERT OR IGNORE INTO TimesMentionned (movie_title, times_mentionned) VALUES (?,?)', (item, times_mentionned[item]))

    conn.commit()

    print("Finished getting NYT data.")

if __name__ == "__main__":
    main()