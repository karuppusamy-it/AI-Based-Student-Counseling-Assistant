import streamlit as st
import io
from ai.openai_service import ai_service

# --- PDF text extraction ---
def extract_text_from_pdf(uploaded_file):
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except ImportError:
        pass
    try:
        from pdfminer.high_level import extract_text as pdfminer_extract
        return pdfminer_extract(io.BytesIO(uploaded_file.read())).strip()
    except ImportError:
        return None

if st.button("⬅️ Back to Dashboard", key="back_dashboard"):
    st.switch_page("pages/dashboard.py")

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
    <div class="dashboard-header">
        <div>
            <h1 style="margin:0; font-weight:800; font-size:1.8rem;">Resume Analyser</h1>
            <div class="welcome-text">Upload your resume and enter a target role to get an AI-powered match report and interview prep questions.</div>
        </div>
        <div class="notif-badge">📄<div class="notif-dot"></div></div>
    </div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def score_color(s):
    return "#22c55e" if s >= 75 else "#f59e0b" if s >= 50 else "#ef4444"

def score_label(s):
    return "Strong Match ✅" if s >= 75 else "Moderate Match ⚠️" if s >= 50 else "Weak Match ❌"

def render_score_gauge(score):
    color = score_color(score)
    label = score_label(score)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#f8fafc,#f1f5f9);border-radius:16px;
                padding:28px 20px;text-align:center;border:1px solid #e2e8f0;margin-bottom:20px;">
        <div style="width:110px;height:110px;border-radius:50%;
                    background:conic-gradient({color} {score}%,#e2e8f0 {score}%);
                    display:flex;align-items:center;justify-content:center;
                    margin:0 auto 14px;box-shadow:0 4px 16px rgba(0,0,0,0.08);">
            <div style="width:80px;height:80px;border-radius:50%;background:#fff;
                        display:flex;align-items:center;justify-content:center;
                        font-size:1.6rem;font-weight:800;color:{color};">{score}</div>
        </div>
        <div style="font-size:1rem;font-weight:700;color:#1e293b;">{label}</div>
        <div style="font-size:0.78rem;color:#94a3b8;margin-top:4px;">Match Score / 100</div>
    </div>
    """, unsafe_allow_html=True)

def render_card(text, bg, border, text_color):
    st.markdown(f"""
    <div style="background:{bg};border-left:3px solid {border};border-radius:6px;
                padding:10px 14px;margin-bottom:8px;font-size:0.87rem;color:{text_color};">
        {text}
    </div>
    """, unsafe_allow_html=True)

def render_tags(items, bg="#f1f5f9", color="#111827"):
    tags = "".join(
        f'<span style="background:{bg};color:{color};border-radius:20px;'
        f'padding:3px 12px;font-size:0.78rem;font-weight:600;margin:3px 3px 3px 0;display:inline-block;">'
        f'{item}</span>' for item in items
    )
    st.markdown(f'<div style="line-height:2.4;">{tags}</div>', unsafe_allow_html=True)

def render_question_card(num, question, tip, accent):
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #f1f5f9;border-left:4px solid {accent};
                border-radius:10px;padding:14px 18px;margin-bottom:12px;
                box-shadow:0 1px 4px rgba(0,0,0,0.05);">
        <div style="font-size:0.62rem;font-weight:700;color:{accent};letter-spacing:0.08em;
                    text-transform:uppercase;margin-bottom:4px;">Q{num}</div>
        <div style="font-size:0.93rem;font-weight:600;color:#1e293b;margin-bottom:8px;">{question}</div>
        <div style="font-size:0.78rem;color:#64748b;background:#f8fafc;border-radius:6px;
                    padding:6px 10px;">
            💡 <b>Tip:</b> {tip}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Left panel: inputs ────────────────────────────────────────────────────────
col_input, col_result = st.columns([1, 1.3], gap="large")

with col_input:
    st.markdown("### 📄 Upload Resume")
    uploaded_pdf = st.file_uploader(
        "Choose a PDF file", type=["pdf"],
        help="Upload your resume in PDF format (max 10 MB)"
    )
    st.markdown("### 🎯 Target Role")
    role = st.text_input(
        "Job role you're applying for",
        placeholder="e.g. Software Engineer, Data Analyst, Product Manager",
        help="Be specific for better results"
    )
    st.markdown("<br>", unsafe_allow_html=True)

    analyse_btn = st.button(
        "🔍 Analyse Resume",
        type="primary",
        use_container_width=True,
        disabled=(uploaded_pdf is None or not role.strip())
    )

    # Role-only interview questions button (no PDF required)
    interview_btn = st.button(
        "🎤 Get Interview Questions Only",
        use_container_width=True,
        disabled=not role.strip()
    )

    if uploaded_pdf is None:
        st.caption("⬆️ Upload a PDF to enable full analysis.")
    if not role.strip():
        st.caption("✏️ Enter a role to enable interview questions.")

# ── Right panel: results in tabs ──────────────────────────────────────────────
with col_result:
    tab_analysis, tab_questions = st.tabs(["📊 Resume Analysis", "🎤 Interview Questions"])

    # ── Tab 1: Analysis ──────────────────────────────────────────────────────
    with tab_analysis:
        if analyse_btn:
            with st.spinner("Reading your resume…"):
                resume_text = extract_text_from_pdf(uploaded_pdf)

            if resume_text is None:
                st.error("⚠️ Could not read the PDF. Ensure it contains selectable text and PyPDF2 is installed.")
            elif len(resume_text) < 50:
                st.warning("The PDF appears empty or has very little text.")
            else:
                with st.spinner("Asking AI to analyse your resume…"):
                    result = ai_service.analyze_resume(resume_text, role.strip())

                if "error" in result:
                    st.error(f"❌ Analysis failed: {result['error']}")
                else:
                    render_score_gauge(result.get("match_score", 0))

                    if summary := result.get("summary"):
                        st.markdown(f"""
                        <div style="background:#f0f9ff;border-left:4px solid #0ea5e9;border-radius:8px;
                                    padding:14px 16px;margin-bottom:16px;color:#0c4a6e;font-size:0.9rem;">
                            {summary}
                        </div>
                        """, unsafe_allow_html=True)

                    if strengths := result.get("strengths"):
                        st.markdown("**✅ Strengths**")
                        for s in strengths:
                            render_card(s, "#f0fdf4", "#22c55e", "#14532d")

                    if gaps := result.get("skill_gaps"):
                        st.markdown("**⚠️ Skill Gaps**")
                        for g in gaps:
                            render_card(g, "#fff7ed", "#f59e0b", "#78350f")

                    if recs := result.get("recommendations"):
                        st.markdown("**💡 Recommendations**")
                        for i, r in enumerate(recs, 1):
                            render_card(f"<b>{i}.</b> {r}", "#f8fafc", "#000000", "#1e293b")

                    if keywords := result.get("keywords_missing"):
                        st.markdown("**🔑 Missing ATS Keywords**")
                        render_tags(keywords, "#fee2e2", "#991b1b")

                    if ats := result.get("ats_tips"):
                        st.info(f"🤖 **ATS Tip:** {ats}")
        else:
            st.markdown("""
            <div style="padding:40px 20px;text-align:center;border:2px dashed #cbd5e1;
                        border-radius:12px;color:#64748b;margin-top:10px;">
                <p style="font-size:2.5rem;margin-bottom:10px;">📄</p>
                <p style="font-size:0.95rem;">Upload your resume PDF and enter a role,<br>
                then click <b>Analyse Resume</b> to get your personalised match report.</p>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 2: Interview Questions ────────────────────────────────────────────
    with tab_questions:
        # Trigger: either full analyse clicked (role known) or interview-only button
        show_questions = (analyse_btn and role.strip()) or interview_btn

        if show_questions and role.strip():
            with st.spinner(f"Generating interview questions for **{role.strip()}**…"):
                iq = ai_service.get_interview_questions(role.strip())

            if "error" in iq:
                st.error(f"❌ Could not fetch questions: {iq['error']}")
            else:
                if summary := iq.get("role_summary"):
                    st.info(f"**{role.strip()}** — {summary}")

                categories = [
                    ("🔧 Technical",    "technical",    "#6366f1"),
                    ("🤝 Behavioural",  "behavioral",   "#0ea5e9"),
                    ("🎯 Role-Specific","role_specific", "#9333ea"),
                    ("🧩 Situational",  "situational",  "#f59e0b"),
                ]

                for label, key, color in categories:
                    questions = iq.get(key, [])
                    if questions:
                        st.markdown(f"""
                        <div style="font-size:0.75rem;font-weight:800;color:{color};
                                    letter-spacing:0.1em;text-transform:uppercase;
                                    margin:20px 0 10px;border-bottom:2px solid {color};
                                    padding-bottom:4px;">{label}</div>
                        """, unsafe_allow_html=True)
                        for i, q in enumerate(questions, 1):
                            render_question_card(
                                i,
                                q.get("question", ""),
                                q.get("tip", ""),
                                color
                            )
        else:
            st.markdown("""
            <div style="padding:40px 20px;text-align:center;border:2px dashed #cbd5e1;
                        border-radius:12px;color:#64748b;margin-top:10px;">
                <p style="font-size:2.5rem;margin-bottom:10px;">🎤</p>
                <p style="font-size:0.95rem;">
                    Enter a <b>Target Role</b> and click<br>
                    <b>Analyse Resume</b> or <b>Get Interview Questions Only</b><br>
                    to see 20 curated questions for your role.
                </p>
            </div>
            """, unsafe_allow_html=True)
