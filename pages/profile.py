import streamlit as st
from database.mongodb import db

# ── Profile Page: Attractive Background ──────────────────────────────────────
st.markdown("""
<style>
/* Animated gradient background for the profile page */
.stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 30%, #0f3460 60%, #533483 100%) !important;
    background-attachment: fixed !important;
}

/* Floating animated blobs */
.stApp::before {
    content: '';
    position: fixed;
    top: -20%;
    left: -10%;
    width: 55%;
    height: 55%;
    background: radial-gradient(circle, rgba(102, 126, 234, 0.25) 0%, transparent 70%);
    border-radius: 50%;
    animation: floatBlob 8s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -15%;
    right: -10%;
    width: 50%;
    height: 50%;
    background: radial-gradient(circle, rgba(118, 75, 162, 0.3) 0%, transparent 70%);
    border-radius: 50%;
    animation: floatBlob 10s ease-in-out infinite alternate-reverse;
    pointer-events: none;
    z-index: 0;
}
@keyframes floatBlob {
    0%   { transform: translate(0, 0) scale(1); }
    100% { transform: translate(40px, 30px) scale(1.1); }
}

/* Make main block container "float" over the gradient */
.block-container {
    background: rgba(255, 255, 255, 0.06) !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5) !important;
    padding: 2.5rem 3rem !important;
    margin-top: 1.5rem !important;
    position: relative;
    z-index: 1;
}

/* Text colours on dark background */
.stApp h1, .stApp h2, .stApp h3,
.stApp .stMarkdown p, .stApp label,
.stApp .stMarkdown strong {
    color: #f0f4ff !important;
}

/* Text area styling */
.stTextArea textarea {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: #000000 !important;
}
.stTextArea textarea::placeholder { color: rgba(200,210,255,0.5) !important; }
.stTextArea textarea:focus {
    border-color: rgba(102,126,234,0.7) !important;
    box-shadow: 0 0 0 3px rgba(102,126,234,0.25) !important;
}

/* Divider */
hr { border-color: rgba(255,255,255,0.15) !important; }

/* Success / Error message overrides */
.stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)
                             
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to view your profile.")
    st.switch_page("pages/login.py")

if st.button("⬅️ Back to Dashboard", key="back_dashboard"):
    st.switch_page("pages/dashboard.py")

user = st.session_state.get('user', {})

# --- Premium Header ---
st.markdown(f"""
    <div class="dashboard-header">
        <div>
            <h1 style="margin:0; font-weight:800; font-size:1.8rem; color: #ffffff;">My Profile</h1>
            <div class="welcome-text" style="color: #ffffff;">View and manage your account details.</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"## {user.get('name', 'Student Name')}")
st.markdown(f"**Email:** {user.get('email', 'N/A')}")
st.markdown(f"**Education Level:** {user.get('education_level', 'N/A')}")



st.markdown("---")

# --- Skills, Interests & Goals Section ---
st.markdown("### 🛠️ Skills, Interests & Goals")

skills_col, interests_col, goals_col = st.columns(3)

with skills_col:
    st.markdown("**My Skills**")
    current_skills = user.get('skills', '')
    skills_input = st.text_area(
        "Skills",
        value=current_skills,
        height=130,
        placeholder="Python, Data Analysis, Communication...",
        label_visibility="collapsed"
    )

with interests_col:
    st.markdown("**My Interests**")
    current_interests = user.get('interests', '')
    interests_input = st.text_area(
        "Interests",
        value=current_interests,
        height=130,
        placeholder="Technology, AI, Music, Sports...",
        label_visibility="collapsed"
    )

with goals_col:
    st.markdown("**My Goals**")
    current_goals = user.get('goals', '')
    goals_input = st.text_area(
        "Goals",
        value=current_goals,
        height=130,
        placeholder="Become a data scientist, Land an internship...",
        label_visibility="collapsed"
    )

if st.button("💾 Save Profile", type="primary"):
    user_id = user.get('_id')
    if user_id:
        success, message = db.update_user_profile(user_id, {
            "skills": skills_input.strip(),
            "interests": interests_input.strip(),
            "goals": goals_input.strip()
        })
        if success:
            st.session_state['user']['skills'] = skills_input.strip()
            st.session_state['user']['interests'] = interests_input.strip()
            st.session_state['user']['goals'] = goals_input.strip()
            st.success("✅ Profile saved successfully!")
        else:
            st.error(f"Failed to save: {message}")
    else:
        st.error("User ID not found. Please log in again.")
