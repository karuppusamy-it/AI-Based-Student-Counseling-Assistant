import streamlit as st
import time
from database.mongodb import db

def render_login():
    st.markdown("""
        <style>
            .stApp, [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #f3e8ff 0%, #d8b4fe 100%) !important;
                /* Background set to a soft purple gradient */
            }
        </style>
    """, unsafe_allow_html=True)

    if st.button("←", key="back_login"):
        st.switch_page("pages/home.py")
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.markdown("<h2 style='text-align: center; color: #2C3E50; margin-top: -2rem;'>Welcome Back</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #7F8C8D;'>Log in to continue your counseling journey</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="student@example.com")
            password = st.text_input("Password", type="password")
            
            submit_button = st.form_submit_button("Log In", type="primary", use_container_width=True)
            
            st.markdown("<p style='text-align: center; margin-top: 1rem; margin-bottom: 0;'>Don't have an account?</p>", unsafe_allow_html=True)
            register_button = st.form_submit_button("Register Now", use_container_width=True)
            
        if register_button:
            st.switch_page("pages/register.py")
            
        if submit_button:
            if not email or not password:
                st.error("Please enter both email and password.")
            else:
                with st.spinner("Authenticating..."):
                    success, message, user_data = db.authenticate_user(email, password)
                    
                if success:
                    st.success("Login successful! Redirecting...")
                    st.session_state['logged_in'] = True
                    st.session_state['user'] = user_data
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(message)

def render_logout():
    if st.sidebar.button("Log Out", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
