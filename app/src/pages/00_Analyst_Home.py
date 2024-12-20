import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Analyst, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Company Ratings', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Company_Ratings.py')

if st.button('View General Ratings By College', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/05_General_Ratings_By_College.py')