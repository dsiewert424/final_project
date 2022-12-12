import plotly.express as px
import plotly.graph_objects as go
import os
import sqlite3
import unittest
import pandas as pd

import numpy as np 

#scatterplot

# df = px.data.tips()
# fig = px.scatter(df, x="total_bill", y="tip", trendline="ols")
# fig.show()

# #bar chart

# x = ['Product A', 'Product B', 'Product C']
# y = [20, 14, 23]

# # Use the hovertext kw argument for hover text
# fig = go.Figure(data=[go.Bar(x=x, y=y,
#             hovertext=['27% market share', '24% market share', '19% market share'])])
# # Customize aspect
# fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
#                   marker_line_width=1.5, opacity=0.6)
# fig.update_layout(title_text='January 2013 Sales Report')
# fig.show()

# #pie chart

# df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
# df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
# fig = px.pie(df, values='pop', names='movies', title='Popular Movies of 2019')
# fig.show()


# def get_restaurant_data(db_filename):
#     """
#     This function accepts the file name of a database as a parameter and returns a list of
#     dictionaries. The key:value pairs should be the name, category, building, and rating
#     of each restaurant in the database.
#     """
#     conn = sqlite3.connect(db_filename)
#     cur = conn.cursor()
    
#     cur.execute(
#         """
#         SELECT restaurants.name, categories.category, buildings.building, restaurants.rating FROM restaurants
#         JOIN categories ON categories.id = restaurants.category_id
#         JOIN buildings ON buildings.id = restaurants.building_id
#         """
#     )
#     restaurant_list = cur.fetchall()
#     conn.commit()

#     restaurants = []
#     for restaurant in restaurant_list:
#         temp = {}
#         temp['name'] = restaurant[0]
#         temp['category'] = restaurant[1]
#         temp['building'] = restaurant[2]
#         temp['rating'] = restaurant[3]

#         restaurants.append(temp)
    
#     return restaurants

# def barchart_restaurant_categories(db_filename):
#     """
#     This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
#     restaurant categories and the values should be the number of restaurants in each category. The function should
#     also create a bar chart with restaurant categories and the counts of each category.
#     """
#     conn = sqlite3.connect(db_filename)
#     cur = conn.cursor()
    
#     cur.execute(
#         """
#         SELECT category, COUNT (category_id) FROM restaurants
#         JOIN categories ON restaurants.category_id = categories.id
#         GROUP BY category_id
       
#         """
#     )
#     restaurant_list = cur.fetchall()
#     conn.commit()

#     restaurant_categories = {}
#     for restaurant in restaurant_list:
#         restaurant_categories[restaurant[0]] = restaurant[1]

#     sorted_categories = dict(sorted(restaurant_categories.items(), key=lambda x: x[1]))
    
#     # plt.barh((list(sorted_categories.keys())), (list(sorted_categories.values())))
#     # plt.title("Number of Restuarants per Category in South U")
#     # plt.ylabel("Restaurant Category")
#     # plt.xlabel("Number of Restaurants")
#     # plt.tight_layout()

#     return restaurant_categories

def make_scatter_plot(cur, conn):
    cur.execute('SELECT TimesMentionned.times_mentionned FROM ImdbStats JOIN TimesMentionned ON ImdbStats.title = TimesMentionned.movie_title')
    x_axis = []
    for item in cur.fetchall():
        x_axis.append(item[0])
    # print(x_axis)

    cur.execute('SELECT ImdbStats.rating FROM ImdbStats JOIN TimesMentionned ON ImdbStats.title = TimesMentionned.movie_title')
    y_axis = []
    for item in cur.fetchall():
        y_axis.append(item[0])
    # print(y_axis)
    # sql_query = pd.read_sql_query ('SELECT ImdbStats.rating, TimesMentionned.times_mentionned FROM ImdbStats JOIN TimesMentionned ON ImdbStats.title = TimesMentionned.movie_title', conn)

    # df = pd.DataFrame(sql_query, columns = ['Times Mentionned in NYT articles', 'IMDB Rating'])

    # print(len(x_axis))
    # print(len(y_axis))
    # plot = px.scatter(x_axis, y_axis)

    df = pd.DataFrame(dict(Rating=y_axis, Times_Mentionned=x_axis))

    plot = px.scatter(df, x="Times_Mentionned", y = "Rating", marginal_x="histogram")

    plot.title("Average Number of New York Times Articles that Mentionned 2010 Movies vs. IMDB Ratings")
    plot.ylabel("IMDB Rating (out of 10 stars)")
    plot.xlabel("Average Number of New York Times Articles that Mentionned Movie")

    # np.random.seed(42) 
    
    # random_x= np.random.randint(1,101,100) 
    # random_y= np.random.randint(1,101,100) 
    
    # plot = px.scatter(random_x, random_y)
    # plot.show()
        
    # "Times Mentionned in NYT articles", y = "IMDB Rating")
    plot.show()

def make_scatter_plot_2(cur, conn):
    cur.execute('SELECT TimesMentionned.times_mentionned FROM ImdbStats JOIN TimesMentionned ON ImdbStats.title = TimesMentionned.movie_title')
    x_axis = []
    # print(x_axis)
    for item in cur.fetchall():
        x_axis.append(item[0])


    print(x_axis)

    cur.execute('SELECT ImdbStats.profit FROM ImdbStats JOIN TimesMentionned ON ImdbStats.title = TimesMentionned.movie_title')
    y_axis = []
    for item in cur.fetchall():
        y_axis.append(item[0])
    
    print(y_axis)
    # sql_query = pd.read_sql_query ('SELECT ImdbStats.rating, TimesMentionned.times_mentionned FROM ImdbStats JOIN TimesMentionned ON ImdbStats.title = TimesMentionned.movie_title', conn)

    # df = pd.DataFrame(sql_query, columns = ['Times Mentionned in NYT articles', 'IMDB Rating'])

    # print(len(x_axis))
    # print(len(y_axis))
    # plot = px.scatter(x_axis, y_axis)

    df = pd.DataFrame(dict(profit=y_axis, times=x_axis))

    plot = px.scatter(df, x="times", y = "profit", width=800, height=400)

    # np.random.seed(42) 
    
    # random_x= np.random.randint(1,101,100) 
    # random_y= np.random.randint(1,101,100) 
    
    # plot = px.scatter(random_x, random_y)
    # plot.show()

def make_bar_graph(cur, conn):

    cur.execute('SELECT genre FROM ImdbStats')
    list_of_genres = [*set(cur.fetchall())]
    genres = []
    for item in list_of_genres:
        genres.append(item[0])

    cur.execute('SELECT ImdbStats.genre, TimesMentionned.times_mentionned FROM ImdbStats JOIN TimesMentionned ON ImdbStats.title = TimesMentionned.movie_title')
    list_to_count_averages = cur.fetchall()
    total = {}
    count = {}
    bar_graph_genres = []
    bar_graph_list = []

    for item in list_to_count_averages:
        total[item[0]] = total.get(item[0], 0) + item[1]
        count[item[0]] = count.get(item[0], 0) + 1

    for genre in total:
        bar_graph_genres.append(genre)
        bar_graph_list.append(total[genre] / count[genre])

    fig = go.FigureWidget(data=go.Bar(x=bar_graph_genres, y=bar_graph_list))

    # fig.layout.title = "Average Number of Times 2010 Movies of Most Popular Genres were Mentionned in New York Times Articles"
    fig.update_layout(title = "Average Number of New York Times Articles that Mentionned 2010 Movies of Most Popular Genres", xaxis_title='Movie Genre', yaxis_title='Average Number of Times Mentionned in New York Times Articles')

    fig.show()
        

    # plot = go.Figure(data = [

    

#Try calling your functions here
def main():
    # get_restaurant_data('South_U_Restaurants.db')
    # barchart_restaurant_categories('South_U_Restaurants.db')
    # fig.show()
    # fig.show()

    conn = sqlite3.connect('movies.sqlite')
    cur = conn.cursor()

    


    make_scatter_plot(cur, conn)
    make_scatter_plot_2(cur, conn)
    # make_bar_graph(cur, conn)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)