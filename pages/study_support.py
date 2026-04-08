import streamlit as st
import pandas as pd
from ai.openai_service import ai_service

# ── Helpers ───────────────────────────────────────────────────────────────────
def score_color(s):
    if s >= 75: return "#22c55e" # Green
    if s >= 55: return "#f59e0b" # Amber
    return "#ef4444"             # Red

def score_label(s):
    if s >= 75: return "Good Health ✅"
    if s >= 55: return "Room for Improvement ⚠️"
    return "At Risk 🆘"

def render_score_gauge(score):
    color = score_color(score)
    label = score_label(score)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#f8fafc,#f1f5f9); border-radius:16px;
                padding:28px 20px; text-align:center; border:1px solid #e2e8f0; margin-bottom:20px;">
        <div style="width:110px; height:110px; border-radius:50%;
                    background:conic-gradient({color} {score}%, #e2e8f0 {score}%);
                    display:flex; align-items:center; justify-content:center;
                    margin:0 auto 14px; box-shadow:0 4px 16px rgba(0,0,0,0.08);">
            <div style="width:80px; height:80px; border-radius:50%; background:#fff;
                        display:flex; align-items:center; justify-content:center;
                        font-size:1.6rem; font-weight:800; color:{color};">{score}</div>
        </div>
        <div style="font-size:1rem; font-weight:700; color:#1e293b;">{label}</div>
        <div style="font-size:0.78rem; color:#94a3b8; margin-top:4px;">Academic Health Score / 100</div>
    </div>
    """, unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
if st.button("⬅️ Back to Dashboard", key="back_dashboard"):
    st.switch_page("pages/dashboard.py")

st.markdown(f"""
    <div class="dashboard-header">
        <div>
            <h1 style="margin:0; font-weight:800; font-size:1.8rem;">Study Support</h1>
            <div class="welcome-text">Submit your recent subject marks to identify areas of risk and get an improvement plan.</div>
        </div>
        <div class="notif-badge">
            📈
            <div class="notif-dot"></div>
        </div>
    </div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── Main Layout ───────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📝 Enter Your Marks")
    st.markdown("Add your subjects and their respective marks (out of 100) below.")
    
    if 'marks_data' not in st.session_state:
        st.session_state.marks_data = pd.DataFrame(
            [{"Subject": "Mathematics", "Mark": 45}, 
             {"Subject": "Science", "Mark": 75},
             {"Subject": "History", "Mark": 82},
             {"Subject": "", "Mark": None}]
        )
    
    edited_df = st.data_editor(
        st.session_state.marks_data,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Subject": st.column_config.TextColumn("Subject Name", required=True),
            "Mark": st.column_config.NumberColumn("Mark (0-100)", min_value=0, max_value=100, required=True)
        }
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🚀 Analyze Academic Health", type="primary", use_container_width=True)

with col2:
    st.markdown("### 📊 Analysis & Action Plan")
    
    if analyze_btn:
        valid_data = edited_df.dropna(subset=['Subject', 'Mark'])
        valid_data = valid_data[valid_data['Subject'].str.strip() != '']
        
        if valid_data.empty:
            st.warning("Please enter at least one valid subject and mark.")
        else:
            subjects_dict = dict(zip(valid_data['Subject'], valid_data['Mark']))
            
            with st.spinner("Analyzing your academic performance..."):
                result = ai_service.get_academic_advice(subjects_dict)
                
            if "error" in result:
                st.error(f"Error analyzing marks: {result['error']}")
            else:
                # ── Visual Score Gauge ──
                avg_score = int(valid_data['Mark'].mean())
                render_score_gauge(avg_score)

                # ── Insights ──
                if assessment := result.get('overall_assessment'):
                    st.markdown(f"""
                    <div style="background:#f0f9ff; border-left:4px solid #0ea5e9; border-radius:8px; 
                                padding:14px 16px; margin-bottom:16px; color:#0c4a6e; font-size:0.9rem; line-height:1.5;">
                        <b>Insight:</b> {assessment}
                    </div>
                    """, unsafe_allow_html=True)
                
                risk_subjects = result.get('risk_subjects', [])
                if not risk_subjects:
                    st.success("🎉 Great job! The AI didn't identify any immediate high-risk subjects.")
                else:
                    st.markdown("<h4 style='font-size:1rem; font-weight:700; color:#1e293b; margin-bottom:12px;'>Risk Subjects & Mitigation</h4>", unsafe_allow_html=True)
                    for p in risk_subjects:
                        subject_name = p.get('subject', 'Unknown Subject')
                        mark = p.get('current_mark', 'N/A')
                        st.markdown(f"""
                        <div style="background:#fff; border:1px solid #f1f5f9; border-left:4px solid #ef4444; 
                                    border-radius:12px; padding:18px; margin-bottom:16px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                                <h4 style="margin:0; color:#1e293b; font-weight:700; font-size:1rem;">{subject_name}</h4>
                                <span style="background:#fef2f2; color:#ef4444; padding:2px 10px; border-radius:30px; font-size:0.75rem; font-weight:800;">{mark}/100</span>
                            </div>
                            <p style="color:#64748b; font-size:0.85rem; margin-bottom:12px;"><b>Analysis:</b> {p.get('analysis', '')}</p>
                            <div style="background:#f8fafc; border-radius:8px; padding:12px; border:1px solid #edf2f7;">
                                <div style="font-size:0.65rem; font-weight:800; color:#475569; text-transform:uppercase; margin-bottom:6px; letter-spacing:0.05em;">Action Plan</div>
                                <ul style="color:#334155; font-size:0.85rem; margin:0; padding-left:18px; line-height:1.4;">
                                    {''.join([f"<li>{item}</li>" for item in p.get('action_plan', [])])}
                                </ul>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if advice := result.get('general_advice'):
                    st.markdown(f"""
                        <div style="text-align:center; padding:10px; border-top:1px solid #f1f5f9; margin-top:10px;">
                            <span style="font-size:0.85rem; color:#94a3b8; font-style:italic;">💡 {advice}</span>
                        </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div style="padding: 80px 20px; text-align: center; border: 2px dashed #f1f5f9; border-radius: 20px; color: #64748b; background:rgba(241,245,249,0.3);">
                <p style="font-size: 3rem; margin-bottom: 20px;">🎒</p>
                <h3 style="color:#475569; margin-bottom:10px;">Ready for Analysis</h3>
                <p style="font-size: 0.9rem; max-width:300px; margin:0 auto;">Fill out your subject marks on the left and click <b>Analyze Marks</b> to get your personalized action plan.</p>
            </div>
            """, unsafe_allow_html=True
        )
