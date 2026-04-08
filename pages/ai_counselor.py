import streamlit as st
import uuid
from ai.openai_service import ai_service
from database.mongodb import db

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please log in to chat with the counselor.")
    st.switch_page("pages/login.py")

user_id = st.session_state.get('user', {}).get('_id')

# --- Session Management ---
if 'active_session_id' not in st.session_state:
    st.session_state.active_session_id = str(uuid.uuid4())
    st.session_state.chat_messages = []

# --- Sidebar: Thread History ---
with st.sidebar:
    st.markdown("### 💬 Your Chats")
    
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        st.session_state.active_session_id = str(uuid.uuid4())
        st.session_state.chat_messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("<div style='font-size:0.8rem; font-weight:700; color:#64748b; margin-bottom:10px;'>RECENT CONVERSATIONS</div>", unsafe_allow_html=True)
    
    sessions = db.get_chat_sessions(user_id) if user_id else []
    
    if not sessions:
        st.caption("No past conversations yet.")
    else:
        for session in sessions:
            sid = session.get('_id', 'legacy')
            # Create a short title from the first message
            title = session.get('first_message', 'New Chat')[:25] + "..."
            if sid == st.session_state.active_session_id:
                st.markdown(f"**👉 {title}**")
            else:
                if st.button(title, key=f"btn_{sid}", use_container_width=True):
                    st.session_state.active_session_id = sid
                    st.session_state.chat_messages = db.get_chat_history(user_id, sid)
                    st.rerun()

if st.button("⬅️ Back to Dashboard", key="back_dashboard"):
    st.switch_page("pages/dashboard.py")

# --- No Header (Distraction Free) ---

# --- ChatGPT-like UI Styling ---
st.markdown("""
    <style>
        /* Base page cleanup */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 6rem !important;
            max-width: 100% !important;
        }

        /* Top Bar for Back Button */
        .stButton:has(button[key="back_dashboard"]) {
            margin-bottom: 2rem !important;
        }

        /* Hide the default global background so we can have a clean chat UI */
        .stApp {
            background-color: #ffffff !important; /* Pure white matching ChatGPT */
        }

        /* Chat Message Area - Centered & Width-Restricted */
        [data-testid="stChatMessage"] {
            padding: 1.2rem 0;
            background: transparent;
            max-width: 800px !important;
            margin: 0 auto !important;
        }
        
        /* Chat Input Container - Centered & Width-Restricted */
        .stChatInputContainer {
            width: 100% !important;
            padding-bottom: 0 !important;
            background-color: transparent !important;
            border: none !important;
        }
        
        /* The inner input area within the fixed bottom container */
        .stChatInputContainer > div {
            max-width: 800px !important;
            margin: 0 auto !important;
            bottom: 2rem !important;
        }

        /* Target the actual input box to match the screenshot */
        [data-testid="stChatInput"] {
            background-color: #f4f4f4 !important; /* Classic ChatGPT light gray input */
            border-radius: 20px !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;
            padding: 8px 12px !important;
        }
        
        /* Input text area styling */
        [data-testid="stChatInput"] textarea {
            color: #475569 !important;
            font-size: 1rem !important;
        }
        
        [data-testid="stChatInput"] textarea::placeholder {
            color: #94a3b8 !important;
        }

        /* The Submit Arrow Button */
        [data-testid="stChatInput"] button {
            background-color: #212121 !important; /* ChatGPT dark button */
            color: #ffffff !important;
            border-radius: 50% !important;
            height: 32px !important;
            width: 32px !important;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 4px;
            margin-top: 2px;
            transition: all 0.2s ease;
        }
        
        [data-testid="stChatInput"] button:hover {
            background-color: #000000 !important; 
            transform: scale(1.05);
        }
        
        /* Message Bubbles layout adjustments */
        [data-testid="chatAvatarIcon-user"] {
            background-color: #e2e8f0;
        }
        [data-testid="chatAvatarIcon-assistant"] {
            background-color: #000000;
        }
    </style>
""", unsafe_allow_html=True)

# --- Initialization of Active Chat ---
if not st.session_state.chat_messages:
    # Try loading from DB first if we switched to a session and it's empty (though handled in btn above)
    history = db.get_chat_history(user_id, st.session_state.active_session_id)
    if history:
        st.session_state.chat_messages = history
    else:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Hello! 👋 I'm your AI Counselor. How can I assist you with your studies or career planning today?"}
        ]

# --- No Empty State ---

# --- Display Chat ---
for message in st.session_state.chat_messages:
    avatar = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- User Input ---
if prompt := st.chat_input("Message your AI Counselor..."):
    st.chat_message("user", avatar="user").markdown(prompt)
    
    # Save user message
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    if user_id:
        db.save_chat_message(user_id, "user", prompt, st.session_state.active_session_id)

    # Get bot response
    with st.chat_message("assistant", avatar="assistant"):
        with st.spinner("Thinking..."):
            recent_history = st.session_state.chat_messages[-10:]
            response = ai_service.chat_with_counselor(recent_history)
            st.markdown(response)
    
    # Save bot response
    st.session_state.chat_messages.append({"role": "assistant", "content": response})
    if user_id:
        db.save_chat_message(user_id, "assistant", response, st.session_state.active_session_id)
    
    # Rerun to update sidebar title if it's the first message
    if len(st.session_state.chat_messages) <= 3:
        st.rerun()
