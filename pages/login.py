import streamlit as st
from auth.login import render_login

if 'logged_in' in st.session_state and st.session_state['logged_in']:
    st.switch_page("pages/dashboard.py")

render_login()
