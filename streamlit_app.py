# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":tropical_drink: Customize Your Smoothie! :tropical_drink:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

session = get_active_session()
# ORDER NAME CONTENT
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ' + name_on_order)

# FRUITS CONTENT
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients'
    , my_dataframe
    , max_selections=5
)

if ingredients_list: 
    ingredients_string = ''

    for fruit in ingredients_list:
        ingredients_string += fruit + ' '
    
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('
    """ + ingredients_string + """', '""" + name_on_order + """')"""

    # st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")
