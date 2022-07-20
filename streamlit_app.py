import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt") 
my_fruit_list = my_fruit_list.set_index('Fruit')                                       

#Picking option provided here
fruits_selected= streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display
streamlit.dataframe(fruits_to_show)


def get_fruityvice_data(this_fruit_choice):
    fruitvice_response= requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruitvice_normalized=pandas.json_normalize(fruitvice_response.json())
    return fruitvice_normalized 


streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select fruit to get information')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()
    



fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)

#
  
streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list") 
        return my_cur.fetchall()
    
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

    
#streamlit.stop() 

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ("'+ new_fruit +'")")
        return "Thanks for adding " + new_fruit   

add_my_fruit = streamlit.text_input('What fruit would you like information about?')
if streamlit.button('Add fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])  
    back_from_fun = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_fun)
