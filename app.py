import streamlit as st
import os

# Must be the first streamlit command
st.set_page_config(
    page_title="AI Student Counseling",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    try:
        with open("assets/styles.css", "r") as f:
            css_content = f.read()
            # If not logged in, append CSS to hide sidebar elements
            if not st.session_state.get('logged_in', False):
                css_content += """
                [data-testid="stSidebar"], 
                [data-testid="stSidebarNav"],
                .st-emotion-cache-nzvw1d,
                [data-testid="stSidebarCollapsedControl"],
                [data-testid="stHeader"] {
                    display: none !important;
                }
                .stMain {
                    margin-left: 0 !important;
                }
                """
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# Import auth modules after page config
from auth.login import render_login, render_logout
from auth.register import render_registration

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None

# --- Page Definitions ---

# --- Page Definitions ---

# Navigation Pages
is_logged_in = st.session_state.get('logged_in', False)
landing = st.Page("pages/home.py", title="Home", icon="🏠", url_path="home", default=not is_logged_in)
login_page = st.Page("pages/login.py", title="Log In", icon="🔑", url_path="login")
register_page = st.Page("pages/register.py", title="Register", icon="📝", url_path="register")
dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon="📊", url_path="dashboard", default=is_logged_in)
academic = st.Page("pages/study_support.py", title="Study Support", icon="📉", url_path="study-support")
career = st.Page("pages/career_guidance.py", title="Career Guidance", icon="🧭", url_path="career-guidance")
chat = st.Page("pages/ai_counselor.py", title="AI Counselor", icon="💬", url_path="ai-counselor")
resources = st.Page("pages/resources.py", title="Resources", icon="📚", url_path="resources")
resume = st.Page("pages/resume_analyser.py", title="Resume Analyser", icon="📄", url_path="resume-analyser")
profile = st.Page("pages/profile.py", title="My Profile", icon="👤", url_path="profile")

# --- Navigation Setup ---

if not st.session_state['logged_in']:
    # Include all pages here so routing works even if logged out (prevents "Page not found" on refresh)
    # The authenticated pages will redirect to login via their own auth guards
    pg = st.navigation([landing, login_page, register_page, dashboard, academic, career, chat, resources, resume, profile], position="hidden")
    pg.run()
else:
    user = st.session_state.get('user', {})
    user_name = user.get('name', 'Student')
    
    st.markdown(f"""
        <style>
            [data-testid="stSidebarNav"]::before {{
                content: "Welcome back, {user_name}";
                display: block;
                padding: 1.5rem 1rem 1rem 0.8rem;
                font-size: 1.25rem;
                font-weight: 700;
                color: #1e40af;
                margin-top: -10px;
            }}
            [data-testid="stSidebarNav"] ul li {{
                margin-bottom: 0.6rem;
            }}
            [data-testid="stSidebarDivider"] {{
                margin-top: 0;
            }}
        </style>
    """, unsafe_allow_html=True)

    
    # --- Main Navigation ---
    # Tool pages in unnamed group — routable but hidden from sidebar via CSS
    pg = st.navigation({
        "Dashboard": [dashboard],
        " ": [academic, career, chat, resources, resume],   # space key = no visible header
        "Account": [profile]
    }, position="sidebar")

    # Detect current page from the navigation object to conditionally hide sidebar nav
    # Only show the sidebar navigation sections (Dashboard, Account) when at the Dashboard hub
    is_on_home = pg.url_path in ["", "dashboard"]

    # Hide global sections (Dashboard, Account, Welcome message) on tool pages
    if not is_on_home:
        st.markdown("""
            <style>
                [data-testid="stSidebarNav"] {
                    display: none !important;
                }
            </style>
        """, unsafe_allow_html=True)
    
    # Hide AI tool links and the blank section divider from the sidebar when on Home/Dashboard
    st.markdown("""
        <style>
            /* Hide tool page nav links (use *=contains so absolute/relative hrefs both match) */
            [data-testid="stSidebarNav"] a[href*="study-support"],
            [data-testid="stSidebarNav"] a[href*="career-guidance"],
            [data-testid="stSidebarNav"] a[href*="ai-counselor"],
            [data-testid="stSidebarNav"] a[href*="resources"],
            [data-testid="stSidebarNav"] a[href*="resume-analyser"] {
                display: none !important;
                height: 0 !important;
                overflow: hidden !important;
                visibility: hidden !important;
            }
            /* Hide the parent li wrapper of each hidden link */
            [data-testid="stSidebarNav"] li:has(a[href*="study-support"]),
            [data-testid="stSidebarNav"] li:has(a[href*="career-guidance"]),
            [data-testid="stSidebarNav"] li:has(a[href*="ai-counselor"]),
            [data-testid="stSidebarNav"] li:has(a[href*="resources"]),
            [data-testid="stSidebarNav"] li:has(a[href*="resume-analyser"]) {
                display: none !important;
            }
            /* Hide the blank section divider left by the empty-name group */
            [data-testid="stSidebarNavSeparator"]:has(~ li a[href*="study-support"]),
            [data-testid="stSidebarNavSeparator"]:empty {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # --- Sidebar Footer (Logout) ---
    with st.sidebar:
        if st.button("Log Out", icon="🚪", use_container_width=True):
            st.session_state['logged_in'] = False
            st.session_state['user'] = None
            st.rerun()
            
    pg.run()
