import streamlit as st
from auth.register import render_registration
if 'logged_in' in st.session_state and st.session_state['logged_in']:
    st.switch_page("pages/dashboard.py")
render_registration()
 