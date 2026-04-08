import streamlit as st
import urllib.parse
from ai.openai_service import ai_service

# Check login state
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to access resource recommendations.")
    st.switch_page("pages/login.py")

user = st.session_state.get('user', {})

if st.button("⬅️ Back to Dashboard", key="back_dashboard"):
    st.switch_page("pages/dashboard.py")

# --- Premium Header ---
st.markdown(f"""
    <div class="dashboard-header">
        <div>
            <h1 style="margin:0; font-weight:800; font-size:1.8rem;">Resource Recommendations</h1>
            <div class="welcome-text">Curated learning materials to accelerate your career path.</div>
        </div>
        <div class="notif-badge">
            🔔
            <div class="notif-dot"></div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.info("💡 **Note:** Recommendations are AI-curated. While we strive for accuracy, please verify links if they don't lead directly to the specific resource.")

# --- AI Recommendation Input ---
st.markdown("### 🔍 Personalized Learning")
col_input, col_btn = st.columns([4, 1])

with col_input:
    topic = st.text_input("Enter a topic you want to learn (e.g., Python, UI/UX, Data Science)", placeholder="What are you interested in today?")

with col_btn:
    st.write("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    generate_btn = st.button("Generate ✨", use_container_width=True)

# Initialize or get recommendations from session state
if 'resource_results' not in st.session_state:
    st.session_state.resource_results = None

if generate_btn and topic:
    with st.spinner(f"Curating resources for '{topic}'..."):
        results = ai_service.get_resource_recommendations(topic)
        if results:
            st.session_state.resource_results = results
            st.success(f"New recommendations generated for {topic}!")
        else:
            st.error("Failed to generate recommendations. Please try again.")

# Helper to filter categories
def get_items(category):
    if st.session_state.resource_results:
        return [item for item in st.session_state.resource_results if item.get('category') == category]
    return []

def get_valid_url(item, category):
    url = item.get('url', '').strip()
    title = item.get('title', '')
    platform = item.get('platform', '') or item.get('author', '') or item.get('channel', '') or item.get('provider', '')
    
    # Ensure platform is a string to prevent concatenation errors
    platform = str(platform) if platform else ""
    
    # Validate the URL: must be a proper http/https link with a domain
    is_valid_url = (url.startswith('http://') or url.startswith('https://')) and '.' in url and ' ' not in url and 'example' not in url
    
    if is_valid_url:
        return url
        
    # If the URL is broken, missing, or hallucinated, formulate a foolproof search query
    query = f"{title} {platform}".strip()
    if category in ["YouTube Tutorials", "YouTube"]:
        return f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    else:
        return f"https://www.google.com/search?q={urllib.parse.quote(query + ' course registration')}"

# Tabs for different categories
tab1, tab2, tab3, tab4 = st.tabs(["🎓 Courses", "📺 YouTube Tutorials", "📖 Books", "📜 Certifications"])

with tab1:
    st.markdown("### Courses")
    items = get_items("Courses")
    if items:
        cols = st.columns(2)
        for idx, item in enumerate(items):
            with cols[idx % 2]:
                valid_url = get_valid_url(item, "Courses")
                st.markdown(f"""
                <div class="custom-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="font-size: 0.75rem; color: #000000; font-weight: 700; text-transform: uppercase;">{item.get('platform', 'Online')}</div>
                        <a href="{valid_url}" target="_blank" style="text-decoration: none; font-size: 1.1rem;">🔗</a>
                    </div>
                    <h4 style="margin: 0.4rem 0; font-size: 1rem;">{item.get('title')}</h4>
                    <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.8rem;">{item.get('desc')}</p>
                    <a href="{valid_url}" target="_blank" class="badge" style="text-decoration: none; color: white !important;">Enroll Now →</a>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Enter a topic above to explore detailed course recommendations.")

with tab2:
    st.markdown("### YouTube Tutorials")
    items = get_items("YouTube")
    if items:
        cols = st.columns(2)
        for idx, item in enumerate(items):
            with cols[idx % 2]:
                valid_url = get_valid_url(item, "YouTube Tutorials")
                st.markdown(f"""
                <div class="custom-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="font-size: 0.75rem; color: #ef4444; font-weight: 700; text-transform: uppercase;">{item.get('channel', 'YouTube')}</div>
                        <a href="{valid_url}" target="_blank" style="text-decoration: none; font-size: 1.1rem;">📺</a>
                    </div>
                    <h4 style="margin: 0.4rem 0; font-size: 1rem;">{item.get('title')}</h4>
                    <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.8rem;">{item.get('desc')}</p>
                    <a href="{valid_url}" target="_blank" style="color: #ef4444; font-weight: 600; font-size: 0.85rem; text-decoration: none;">Watch Video →</a>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Enter a topic above to see specific YouTube recommendations.")

with tab3:
    st.markdown("### Books")
    items = get_items("Books")
    if items:
        cols = st.columns(2)
        for idx, item in enumerate(items):
            with cols[idx % 2]:
                valid_url = get_valid_url(item, "Books")
                st.markdown(f"""
                <div class="custom-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="font-size: 0.75rem; color: #10b981; font-weight: 700; text-transform: uppercase;">Book</div>
                        <a href="{valid_url}" target="_blank" style="text-decoration: none; font-size: 1.1rem;">📖</a>
                    </div>
                    <h4 style="margin: 0.4rem 0; font-size: 1rem;">{item.get('title')}</h4>
                    <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.5rem;"><strong>By:</strong> {item.get('author')}</p>
                    <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.8rem;">{item.get('desc')}</p>
                    <a href="{valid_url}" target="_blank" style="color: #10b981; font-weight: 600; font-size: 0.85rem; text-decoration: none;">View Details →</a>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Enter a topic above to see specific Book recommendations.")

with tab4:
    st.markdown("### Certifications")
    items = get_items("Certifications")
    if items:
        cols = st.columns(2)
        for idx, item in enumerate(items):
            with cols[idx % 2]:
                valid_url = get_valid_url(item, "Certifications")
                st.markdown(f"""
                <div class="custom-card" style="border-left: 4px solid #f59e0b;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="font-size: 0.75rem; color: #f59e0b; font-weight: 700; text-transform: uppercase;">{item.get('provider', 'Industry')}</div>
                        <a href="{valid_url}" target="_blank" style="text-decoration: none; font-size: 1.1rem;">📜</a>
                    </div>
                    <h4 style="margin: 0.4rem 0; font-size: 1rem;">{item.get('title')}</h4>
                    <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.8rem;">{item.get('desc')}</p>
                    <a href="{valid_url}" target="_blank" style="color: #f59e0b; font-weight: 600; font-size: 0.85rem; text-decoration: none;">Certification Details →</a>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Enter a topic above to see specific Certification recommendations.")
