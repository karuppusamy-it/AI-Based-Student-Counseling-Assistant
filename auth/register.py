import streamlit as st
import time
from database.mongodb import db

def render_registration():
    st.markdown("""
        <style>
            .stApp, [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #f3e8ff 0%, #d8b4fe 100%) !important;
            }
        </style>
    """, unsafe_allow_html=True)

    if st.button("←", key="back_register"):
        st.switch_page("pages/home.py")
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.markdown("<h2 style='text-align: center; color: #2C3E50; margin-top: -2rem;'>Student Registration</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #7F8C8D;'>Join the AI Counseling Platform</p>", unsafe_allow_html=True)
        
        with st.form("registration_form"):
            name = st.text_input("Full Name", placeholder="e.g. John Doe")
            email = st.text_input("Email", placeholder="student@example.com")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            education_level = st.selectbox(
                "Current Education Level",
                ["High School", "Undergraduate", "Postgraduate", "Other"]
            )
            interests = st.text_area("What are your interests? (e.g. AI, Music, Sports)", placeholder="Type your interests here...")
            
            submit_button = st.form_submit_button("Register", type="primary", use_container_width=True)
            
            st.markdown("<p style='text-align: center; margin-top: 1rem; margin-bottom: 0;'>Already have an account?</p>", unsafe_allow_html=True)
            login_button = st.form_submit_button("login", use_container_width=True)
            
        if login_button:
            st.switch_page("pages/login.py")
    
        if submit_button:
            if not name or not email or not password:
                st.error("Please fill in all required fields (Name, Email, Password).")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long.")
            else:
                with st.spinner("Creating your account..."):
                    success, message_or_id = db.create_user(
                        name=name,
                        email=email,
                        password=password,
                        education_level=education_level,
                        interests=interests
                    )
                    
                if success:
                    st.success("Registration successful! Redirecting to login...")
                    time.sleep(2)
                    st.switch_page("pages/login.py")
                else:
                    st.error(f"Registration failed: {message_or_id}")
