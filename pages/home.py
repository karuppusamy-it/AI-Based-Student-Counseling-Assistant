import streamlit as st

def render_home():
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">AI-Based Student Counseling Assistant</h1>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Display some features
        st.markdown("### ✨ Key Features")
        st.markdown("""
        - 🤖 **AI Chat Counselor**: Get immediate academic and motivational support.
        - 🎯 **Career Recommendations**: Discover fields that match your unique skills and interests.
        - 📚 **Course Suggestions**: Find top-rated courses to upskill yourself.
        """)
        
        st.write("")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Log In", use_container_width=True, type="primary"):
                st.switch_page("pages/login.py")
        with c2:
            if st.button("Register", use_container_width=True):
                st.switch_page("pages/register.py")

if __name__ == "__main__":
    render_home()
