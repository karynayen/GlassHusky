import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Company')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# # get the countries from the world bank data
# with st.echo(code_location='above'):
#     countries:pd.DataFrame = wb.get_countries()
   
#     st.dataframe(countries)

# # the with statment shows the code for this block above it 
# with st.echo(code_location='above'):
#     arr = np.random.normal(1, 1, size=100)
#     test_plot, ax = plt.subplots()
#     ax.hist(arr, bins=20)

#     st.pyplot(test_plot)


# with st.echo(code_location='above'):
#     slim_countries = countries[countries['incomeLevel'] != 'Aggregates']
#     data_crosstab = pd.crosstab(slim_countries['region'], 
#                                 slim_countries['incomeLevel'],  
#                                 margins = False) 
#     st.table(data_crosstab)

#calling companies endpoint
st.write("# Pulling all companies")

"""
Simply retrieving data from a REST api running in a separate Docker Container.

If the container isn't running, this will be very unhappy.  But the Streamlit app 
should not totally die. 
"""
co_data = {} 
try:
  #list of companyID, name, size
  co_data = requests.get('http://api:4000/co/companies').json()
  co_data = pd.DataFrame(co_data)
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  co_data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(co_data)

st.write("# Reviews for each company")
reviews_df = pd.DataFrame()
try:
  companyID = co_data['companyID']
  for id_num in companyID:
     response = requests.get(f'http://api:4000/co/companies/{id_num}/reviews').json()
     review = pd.DataFrame(response)
     reviews_df = pd.concat([reviews_df, review], axis =0, ignore_index = True)
except:
  st.write("**Important**: Could not connect to sample api, so using dummy data.")
  reviews_df = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}

st.dataframe(reviews_df)
# with st.echo(code_location='above'):
#     # arr = np.random.normal(1, 1, size=100)
#     # test_plot, ax = plt.subplots()
#     # ax.hist(arr, bins=20)

#     # st.pyplot(test_plot)
#     # companies_df = pd.DataFrame(data)
#     company1_df = data[0] #data = list of companyID, Name, size
#     st.dataframe(company1_df)
