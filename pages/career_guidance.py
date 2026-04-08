import streamlit as st
from ai.openai_service import ai_service
import time
import urllib.parse

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to get career recommendations.")
    st.switch_page("pages/login.py")

user = st.session_state.get('user', {})

if st.button("⬅️ Back to Dashboard", key="back_dashboard"):
    st.switch_page("pages/dashboard.py")

# --- Premium Header ---
st.markdown(f"""
    <div class="dashboard-header">
        <div>
            <h1 style="margin:0; font-weight:800; font-size:1.8rem;">Career Guidance</h1>
            <div class="welcome-text">Analyzing profile for <b>{user.get('name', 'Student')}</b> ({user.get('education_level', 'N/A')})</div>
        </div>
        <div class="notif-badge">
            🔔
            <div class="notif-dot"></div>
        </div>
    </div>
""", unsafe_allow_html=True)

with st.expander("📝 Your Profile Details", expanded=True):
    # Pull directly from the logged-in user profile
    interests_from_profile = user.get("interests", "")
    skills_from_profile = user.get("skills", "")
    goals_from_profile = user.get("goals", "")
    
    st.info("We are using the Skills, Interests, and Goals you saved in your Profile to generate your career path:")
    
    # Display the profile information
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Your Skills:**")
        st.write(skills_from_profile if skills_from_profile else "*(None provided)*")
    with col2:
        st.markdown("**Your Interests:**")
        st.write(interests_from_profile if interests_from_profile else "*(None provided)*")
    with col3:
        st.markdown("**Your Goals:**")
        st.write(goals_from_profile if goals_from_profile else "*(None provided)*")
        
    st.markdown("---")
    
    with st.form("career_form"):
        # Combine interests and goals for the AI prompt since both are relevant
        combined_interests = f"{interests_from_profile} (Goals: {goals_from_profile})" if goals_from_profile else interests_from_profile
        
        preferred_field = st.selectbox("Is there a specific field you are curious about? (Optional)", ["No Preference", "Technology / IT", "Healthcare", "Business / Finance", "Arts / Design", "Engineering", "Sciences"])
        
        submit_button = st.form_submit_button("Generate My Path", type="primary", use_container_width=True)

def get_valid_url(item):
    url = item.get('url', '').strip()
    title = item.get('title', '')
    platform = item.get('platform', '')
    
    # Ensure platform is a string to prevent concatenation errors
    platform = str(platform) if platform else ""
    
    # Validate the URL: must be a proper http/https link with a domain
    is_valid_url = (url.startswith('http://') or url.startswith('https://')) and '.' in url and ' ' not in url and 'example' not in url
    
    if is_valid_url:
        return url
        
    # If the URL is broken, missing, or hallucinated, formulate a foolproof search query
    query = f"{title} {platform} course".strip()
    return f"https://www.google.com/search?q={urllib.parse.quote(query)}"

if submit_button:
    if not skills_from_profile and not interests_from_profile:
        st.error("Please update your Skills and Interests in your Profile page first!")
    else:
        with st.spinner("Analyzing your profile... This might take a few seconds."):
            # Add a slight delay for better UX
            time.sleep(1)
            result = ai_service.get_career_recommendation(combined_interests, skills_from_profile, preferred_field)
            
            if "error" in result:
                st.error(f"Error fetching recommendations: {result['error']}")
            else:
                st.success("Analysis Complete!")
                st.markdown("---")
                
                # Display Careers
                st.subheader("🎯 Career Recommendations")
                recs = result.get("recommendations", [])
                
                for rec in recs:
                    with st.container():
                        st.markdown(f"""
                        <div class="custom-card">
                            <div class="card-title">{rec.get('title', 'Recommended Career')}</div>
                            <div class="card-text">
                                <strong>Why it fits you:</strong><br/>
                                {rec.get('explanation', '')}
                                <br/><br/>
                                <strong>Key Skills to Learn:</strong>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Render skills as tags outside the card for better formatting compatibility with Streamlit
                        skills_html = " ".join([f'<span class="badge">{s}</span>' for s in rec.get('skills_required', [])])
                        st.markdown(skills_html, unsafe_allow_html=True)
                        st.markdown("<br/>", unsafe_allow_html=True)
                
                # Display Courses
                st.subheader("📚 Suggested Courses & Certifications")
                courses = result.get("recommended_courses", [])
                
                for course in courses:
                    valid_url = get_valid_url(course)
                    st.markdown(f"""
                    <div class="custom-card" style="border-left: 4px solid #000000;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div style="font-size: 0.75rem; color: #000000; font-weight: 700; text-transform: uppercase;">{course.get('platform', 'Training')}</div>
                            <a href="{valid_url}" target="_blank" style="text-decoration: none; font-size: 1.1rem;">🔗</a>
                        </div>
                        <h4 style="margin: 0.4rem 0; font-size: 1rem;">{course.get('title', 'Recommended Course')}</h4>
                        <p style="font-size: 0.85rem; color: #4a5568; margin-bottom: 0.8rem;">{course.get('description', '')}</p>
                        <a href="{valid_url}" target="_blank" class="badge" style="text-decoration: none; color: white !important;">Enroll Now →</a>
                    </div>
                    """, unsafe_allow_html=True)

