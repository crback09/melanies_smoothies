# Import python packages
import streamlit as st


# Establish connection using the configuration in secrets.toml
conn = st.connection("snowflake")
session = conn.session()
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤Customize Your Smoothie!🥤")
st.write (
"🍓🍌🍍Choose the fruits you want your custom Smoothie!"
)

# Input: Name on the Smoothie
name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be:',name_on_order)

# Connect to Snowflake and get fruit options
cnx = st.connection("snowflake",
      account = "DGIVXIM-RNB69144",
      user = "CRBACK09",
      authenticator = "externalbrowser",
      role = "SYSADMIN",
      warehouse = "COMPUTE_WH",
      database = "SMOOTHIES",
      schema = "PUBLIC",
)
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
    )

# Only proceed if ingredients are selected
if ingredients_list:
    # Build ingredients string
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # Create SQL insert statement with both columns
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string.strip()}', '{name_on_order}')
    """

    # Optional: debug the SQL before executing
    # st.write(my_insert_stmt)
    # st.stop()

    # Button to trigger the insert
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'✅ Your Smoothie is ordered, {name_on_order}!')

