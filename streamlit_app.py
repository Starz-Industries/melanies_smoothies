# Import python packages
import streamlit as st
import requests
import pandas
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":tropical_drink: Customize Your Smoothie! :tropical_drink:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

cnx = st.connection("snowflake")
session = cnx.session()
# ORDER NAME CONTENT
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ' + name_on_order)

# FRUITS CONTENT
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))

# Convert Snopark dataframe to pandas dataframe
pd_df = my_dataframe.to_pandas()
st.dataframe(data=pd_df)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients'
    , my_dataframe
    , max_selections=5
)

if ingredients_list: 
    ingredients_string = ''

    for fruit in ingredients_list:
        ingredients_string += fruit + ' '
        st.subheader(fruit + ' Nutritional Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit)
        sf_df =  st.dataframe(data=smoothiefroot_response.json())
    
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('
    """ + ingredients_string + """', '""" + name_on_order + """')"""

    # st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")
