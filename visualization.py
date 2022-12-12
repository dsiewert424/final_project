import plotly.express as px
import plotly.graph_objects as go
import os
import sqlite3
import unittest

#scatterplot

df = px.data.tips()
fig = px.scatter(df, x="total_bill", y="tip", trendline="ols")
fig.show()

#bar chart

x = ['Product A', 'Product B', 'Product C']
y = [20, 14, 23]

# Use the hovertext kw argument for hover text
fig = go.Figure(data=[go.Bar(x=x, y=y,
            hovertext=['27% market share', '24% market share', '19% market share'])])
# Customize aspect
fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
fig.update_layout(title_text='January 2013 Sales Report')
fig.show()

#pie chart

df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
fig = px.pie(df, values='pop', names='movies', title='Popular Movies of 2019')
fig.show()


def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    
    cur.execute(
        """
        SELECT restaurants.name, categories.category, buildings.building, restaurants.rating FROM restaurants
        JOIN categories ON categories.id = restaurants.category_id
        JOIN buildings ON buildings.id = restaurants.building_id
        """
    )
    restaurant_list = cur.fetchall()
    conn.commit()

    restaurants = []
    for restaurant in restaurant_list:
        temp = {}
        temp['name'] = restaurant[0]
        temp['category'] = restaurant[1]
        temp['building'] = restaurant[2]
        temp['rating'] = restaurant[3]

        restaurants.append(temp)
    
    return restaurants

def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    
    cur.execute(
        """
        SELECT category, COUNT (category_id) FROM restaurants
        JOIN categories ON restaurants.category_id = categories.id
        GROUP BY category_id
       
        """
    )
    restaurant_list = cur.fetchall()
    conn.commit()

    restaurant_categories = {}
    for restaurant in restaurant_list:
        restaurant_categories[restaurant[0]] = restaurant[1]

    sorted_categories = dict(sorted(restaurant_categories.items(), key=lambda x: x[1]))
    
    plt.barh((list(sorted_categories.keys())), (list(sorted_categories.values())))
    plt.title("Number of Restuarants per Category in South U")
    plt.ylabel("Restaurant Category")
    plt.xlabel("Number of Restaurants")
    plt.tight_layout()

    return restaurant_categories

#Try calling your functions here
def main():
    pass
    get_restaurant_data('South_U_Restaurants.db')
    barchart_restaurant_categories('South_U_Restaurants.db')
    fig.show()
    fig.show()

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)