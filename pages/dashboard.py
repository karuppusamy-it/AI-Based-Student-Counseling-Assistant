import streamlit as st

# Check login state
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to access your dashboard.")
    st.switch_page("pages/login.py")

user = st.session_state.get('user', {})

# --- Dashboard Header ---
st.markdown(f"""
    <div class="dashboard-header">
        <div>
            <h1 style="margin:0; font-weight:800; font-size:1.8rem;">Student Dashboard</h1>
            <div class="welcome-text">Welcome back, <b>{user.get('name', 'Student')}</b></div>
        </div>
        <div class="notif-badge">
            🔔
            <div class="notif-dot"></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- AI Tools Section ---
st.markdown("""
<style>
/* ── Main container spacing ── */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 0rem !important;
}

/* ── Card container ── */
.ai-tool-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 28px 20px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.06);
    text-align: center;
    border: 1px solid #f1f5f9;
    border-top: 4px solid #000000;
    transition: transform 0.25s cubic-bezier(.4,2,.55,1), box-shadow 0.25s ease;
    cursor: default;
    min-height: 215px;
    padding: 20px 20px 14px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}
.ai-tool-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.1), 0 2px 8px rgba(0,0,0,0.06);
}
/* Icon badge */
.ai-tool-card .tool-icon-wrap {
    width: 60px;
    height: 60px;
    border-radius: 16px;
    background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 14px;
    font-size: 1.8rem;
    transition: transform 0.25s cubic-bezier(.4,2,.55,1);
    flex-shrink: 0;
}
.ai-tool-card:hover .tool-icon-wrap {
    transform: scale(1.1) rotate(-4deg);
}
.ai-tool-card .tool-name {
    font-weight: 700;
    font-size: 1rem;
    color: #1e293b;
    margin-bottom: 8px;
    letter-spacing: -0.01em;
    min-height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.ai-tool-card .tool-desc {
    font-size: 0.8rem;
    color: #94a3b8;
    line-height: 1.5;
    margin-bottom: 10px;
    min-height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
}
/* ── Start button: scoped to main content only, overrides Emotion CSS ── */
section.stMain [data-testid="stPageLink"],
section.stMain [data-testid="stPageLink"] * {
    all: unset;
    box-sizing: border-box;
}
section.stMain [data-testid="stPageLink"] {
    display: block !important;
    margin-top: 0 !important;
}
section.stMain [data-testid="stPageLink"] a {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    padding: 11px 16px !important;
    background: linear-gradient(135deg, #1f2937 0%, #000000 100%) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    text-decoration: none !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25) !important;
    transition: background 0.2s ease, box-shadow 0.2s ease, transform 0.15s ease !important;
    cursor: pointer !important;
}
section.stMain [data-testid="stPageLink"] a:hover {
    background: linear-gradient(135deg, #000000 0%, #1f2937 100%) !important;
    box-shadow: 0 6px 22px rgba(0,0,0,0.3) !important;
    transform: translateY(-2px) !important;
}
section.stMain [data-testid="stPageLink"] a span,
section.stMain [data-testid="stPageLink"] a div,
section.stMain [data-testid="stPageLink"] a p {
    display: inline !important;
    color: #ffffff !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
    padding: 0 !important;
}
</style>
<h3 style='color:#1e293b; font-weight:800; margin-top:1.2rem; font-size:1.25rem; letter-spacing:-0.02em;'>
  🛠️ AI Tools
</h3>
<p style='color:#94a3b8; font-size:0.85rem; margin-top:2px; margin-bottom:1rem;'>
  Pick a tool and get started instantly
</p>
""", unsafe_allow_html=True)

t_col1, t_col2, t_col3, t_col4, t_col5 = st.columns(5, gap="medium")

tools = [
    {"name": "Study Support",    "icon": "📊", "desc": "Analyze your marks & get a personalized study plan",  "page": "pages/study_support.py"},
    {"name": "Career Guidance",  "icon": "🧭", "desc": "Discover your ideal career path with AI",             "page": "pages/career_guidance.py"},
    {"name": "AI Counselor",     "icon": "💬", "desc": "Chat with your personal AI student advisor",          "page": "pages/ai_counselor.py"},
    {"name": "Resources",        "icon": "📚", "desc": "Curated learning materials just for you",             "page": "pages/resources.py"},
    {"name": "Resume Analyser",  "icon": "📄", "desc": "Upload your resume & get an AI match report",         "page": "pages/resume_analyser.py"},
]

for col, tool in zip([t_col1, t_col2, t_col3, t_col4, t_col5], tools):
    with col:
        st.markdown(f"""
            <div class="ai-tool-card">
                <div class="tool-icon-wrap">{tool['icon']}</div>
                <div class="tool-name">{tool['name']}</div>
                <div class="tool-desc">{tool['desc']}</div>
            </div>
        """, unsafe_allow_html=True)
        st.page_link(tool['page'], label="Start →", use_container_width=True)

st.markdown("<br><h3 style='color:#1e293b; font-weight:800;'>Profile Overview</h3>", unsafe_allow_html=True)

# --- Profile Info Cards ---
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(f"""
        <div style="background:#fff; border-radius:14px; padding:24px 28px; box-shadow:0 2px 12px rgba(0,0,0,0.07); margin-bottom:20px;">
            <div style="font-size:0.75rem; font-weight:700; color:#6b7280; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:6px;">👤 Personal Info</div>
            <div style="font-size:1.4rem; font-weight:800; color:#1e293b; margin-bottom:4px;">{user.get('name', 'N/A')}</div>
            <div style="color:#64748b; font-size:0.95rem; margin-bottom:4px;">📧 {user.get('email', 'N/A')}</div>
            <div style="color:#64748b; font-size:0.95rem;">🎓 {user.get('education_level', 'N/A')}</div>
        </div>
    """, unsafe_allow_html=True)

    # Skills
    skills = user.get('skills', '')
    skills_html = ""
    if skills:
        for s in [t.strip() for t in skills.replace(',', '\n').split('\n') if t.strip()]:
            skills_html += f'<span style="display:inline-block; background:#eef2ff; color:#4f46e5; border-radius:20px; padding:4px 12px; font-size:0.82rem; font-weight:600; margin:3px 3px 3px 0;">{s}</span>'
    st.markdown(f"""
        <div style="background:#fff; border-radius:14px; padding:24px 28px; box-shadow:0 2px 12px rgba(0,0,0,0.07);">
            <div style="font-size:0.75rem; font-weight:700; color:#6b7280; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:10px;">🛠️ Skills</div>
            <div>{skills_html if skills_html else '<span style="color:#9ca3af; font-size:0.9rem;">No skills added yet.</span>'}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Interests
    interests = user.get('interests', '')
    interests_html = ""
    if interests:
        for i in [t.strip() for t in interests.replace(',', '\n').split('\n') if t.strip()]:
            interests_html += f'<span style="display:inline-block; background:#f0fdf4; color:#16a34a; border-radius:20px; padding:4px 12px; font-size:0.82rem; font-weight:600; margin:3px 3px 3px 0;">{i}</span>'
    st.markdown(f"""
        <div style="background:#fff; border-radius:14px; padding:24px 28px; box-shadow:0 2px 12px rgba(0,0,0,0.07); margin-bottom:20px;">
            <div style="font-size:0.75rem; font-weight:700; color:#6b7280; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:10px;">💡 Interests</div>
            <div>{interests_html if interests_html else '<span style="color:#9ca3af; font-size:0.9rem;">No interests added yet.</span>'}</div>
        </div>
    """, unsafe_allow_html=True)

    # Goals
    goals = user.get('goals', '')
    goals_html = ""
    if goals:
        for g in [t.strip() for t in goals.replace(',', '\n').split('\n') if t.strip()]:
            goals_html += f'<div style="display:flex; align-items:flex-start; gap:8px; margin-bottom:8px;"><span style="color:#f59e0b; font-size:1rem; margin-top:1px;">🎯</span><span style="color:#374151; font-size:0.92rem;">{g}</span></div>'
    st.markdown(f"""
        <div style="background:#fff; border-radius:14px; padding:24px 28px; box-shadow:0 2px 12px rgba(0,0,0,0.07);">
            <div style="font-size:0.75rem; font-weight:700; color:#6b7280; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:10px;">🎯 Goals</div>
            <div>{goals_html if goals_html else '<span style="color:#9ca3af; font-size:0.9rem;">No goals added yet.</span>'}</div>
        </div>
    """, unsafe_allow_html=True)
