import plotly.express as px
import plotly.graph_objects as go
import os
import sqlite3
import unittest
import pandas as pd
import numpy as np 

def make_rating_scatter_plot(cur, conn):
    cur.execute('SELECT TimesMentionned.times_mentionned, ImdbStats.rating, ImdbStats.title FROM ImdbStats JOIN TimesMentionned ON ImdbStats.title = TimesMentionned.movie_title')
    x_axis = []
    y_axis = []
    movie_titles = []

    fout = open("NYT_movies_mentioned_and_ratings.csv", "w")
    line = "Count of Articles Mentioned, Ratings, Movie Title\n"
    fout.write(line)
    row = ""

    for item in cur.fetchall():
        x_axis.append(item[0])
        row = row + str(item[0]) + ','
        y_axis.append(item[1])
        row = row + str(item[1]) + ','
        movie_titles.append(item[2])

        row = row + str(item[2])
        line = row + "\n"
        fout.write(line)
        row = ""

    fout.close()
    # print(x_axis)


    df = pd.DataFrame(dict(Rating=y_axis, Times_Mentionned=x_axis, Movie_Title=movie_titles))

    plot = px.scatter(df, x="Times_Mentionned", y = "Rating", hover_name="Movie_Title", marginal_x="histogram", title="Number of New York Times Articles that Mentionned 2010 Movies vs. IMDB Ratings", labels={"Times_Mentionned": "Number of New York Times Articles that Mentionned Movie", "Rating": "IMDB Rating (out of 10 stars)"})

    plot.show()



def make_profit_scatter_plot(cur, conn):
    cur.execute('SELECT TimesMentionned.times_mentionned, ImdbStats.profit, ImdbStats.title FROM ImdbStats JOIN TimesMentionned ON ImdbStats.title = TimesMentionned.movie_title')
    x_axis = []
    y_axis = []
    movie_titles = []

    fout = open("NYT_movies_mentioned_and_profits.csv", "w")
    line = "Count of Articles Mentioned, Gross Profit ($ in millions), Movie Title\n"
    fout.write(line)
    row = ""
    # print(x_axis)
    for item in cur.fetchall():
        x_axis.append(item[0])
        row = row + str(item[0]) + ','
        y_axis.append(item[1])
        row = row + '$' + str(item[1]) + ' M,'
        movie_titles.append(item[2])
        row = row + str(item[2])
        line = row + "\n"
        fout.write(line)
        row = ""

    fout.close()


    df = pd.DataFrame(dict(Gross_Profit=y_axis, Times_Mentionned=x_axis, Movie_Title=movie_titles))

    plot = px.scatter(df, x="Times_Mentionned", y = "Gross_Profit", hover_name="Movie_Title", marginal_x="histogram", title="Number of New York Times Articles that Mentionned 2010 Movies vs. Gross Profit", labels={"Times_Mentionned": "Number of New York Times Articles that Mentionned Movie", "Gross_Profit": "Gross Profit (USD in Millions)"})


    plot.show()



def make_avg_times_mentionned_bar_graph(cur, conn):

    cur.execute('SELECT ImdbStats.genre, TimesMentionned.times_mentionned FROM ImdbStats JOIN TimesMentionned ON ImdbStats.title = TimesMentionned.movie_title')
    list_to_count_averages = cur.fetchall()
    total = {}
    count = {}
    bar_graph_genres = []
    bar_graph_list = []

    fout = open("avg_articles_per_genre.csv", "w")
    line = "Genre, Number of Articles Mentioning Genre, Number of Movies of Genre, Average Number Calculated\n"
    fout.write(line)
    row = ""

    for item in list_to_count_averages:
        total[item[0]] = total.get(item[0], 0) + item[1]
        count[item[0]] = count.get(item[0], 0) + 1

    for genre in total:
        bar_graph_genres.append(genre)
        row = row + str(genre) + ','
        bar_graph_list.append(total[genre] / count[genre])
        row = row + str(total[genre]) + ','
        row = row + str(count[genre]) + ','
        row = row + str(total[genre] / count[genre])
        line = row + "\n"
        fout.write(line)
        row = ""
        
    fout.close()

    fig = go.FigureWidget(data=go.Bar(x=bar_graph_genres, y=bar_graph_list))

    # fig.layout.title = "Average Number of Times 2010 Movies of Most Popular Genres were Mentionned in New York Times Articles"
    fig.update_layout(title = "Average Number of New York Times Articles that Mentionned 2010 Movies of Most Popular Genres", xaxis_title='Movie Genre', yaxis_title='Average Number of Times Mentionned in New York Times Articles')

    fig.show()

def make_avg_gross_profit_bar_graph(cur, conn):


    cur.execute('SELECT ImdbStats.genre, ImdbStats.profit FROM ImdbStats')
    list_to_count_averages = cur.fetchall()
    total = {}
    count = {}
    bar_graph_genres = []
    bar_graph_list = []

    fout = open("avg_gross_profit_per_genre.csv", "w")
    line = "Genre, Total Profit of Genre, Number of Movies of Genre, Average Number Calculated\n"
    fout.write(line)
    row = ""

    for item in list_to_count_averages:
        if (item[1] != 'None'):
            total[item[0]] = total.get(item[0], 0) + float(item[1])
            count[item[0]] = count.get(item[0], 0) + 1
        
    for genre in total:
        bar_graph_genres.append(genre)
        row = row + str(genre) + ','
        bar_graph_list.append(total[genre] / count[genre])
        row = row + str(total[genre]) + ','
        row = row + str(count[genre]) + ','
        row = row + str(total[genre] / count[genre])
        line = row + "\n"
        fout.write(line)
        row = ""
        
    fout.close()

    fig = go.FigureWidget(data=go.Bar(x=bar_graph_genres, y=bar_graph_list))

    # fig.layout.title = "Average Number of Times 2010 Movies of Most Popular Genres were Mentionned in New York Times Articles"
    fig.update_layout(title = "Average Gross Profit of 2010 Movies by Genre", xaxis_title='Movie Genre', yaxis_title='Gross Profit (USD in Millions)')

    fig.show()
        


    
def main():

    conn = sqlite3.connect('movies.sqlite')
    cur = conn.cursor()

    #get list of genres
    cur.execute('SELECT genre FROM ImdbStats')
    list_of_genres = [*set(cur.fetchall())]
    genres = []
    for item in list_of_genres:
        genres.append(item[0])


    make_rating_scatter_plot(cur, conn)
    make_profit_scatter_plot(cur, conn)
    make_avg_times_mentionned_bar_graph(cur, conn)
    make_avg_gross_profit_bar_graph(cur, conn)

if __name__ == '__main__':
    main()