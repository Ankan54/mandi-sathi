import streamlit as st
from agents.crew_manager import MandiSaathiCrew
from database.db_manager import DatabaseManager
from database.session_manager import SessionManager

# Page configuration
st.set_page_config(
    page_title="Mandi Saathi - Farmer Negotiation Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for chat interface matching the screenshot design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background - soft cream/beige */
    .stApp {
        background-color: #F5F3F0;
    }
    
    /* Sidebar - Deep forest green */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B4332 0%, #2D6A4F 100%);
        padding: 1.5rem 1rem;
    }
    
    [data-testid="stSidebar"] * {
        color: #F8F6F3 !important;
    }
    
    /* Sidebar header */
    [data-testid="stSidebar"] .sidebar-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    /* New Chat button */
    [data-testid="stSidebar"] button[kind="primary"] {
        background: linear-gradient(135deg, #52B788 0%, #40916C 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        letter-spacing: 0.03em;
        box-shadow: 0 4px 12px rgba(64, 145, 108, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    [data-testid="stSidebar"] button[kind="primary"]:hover {
        background: linear-gradient(135deg, #40916C 0%, #2D6A4F 100%);
        box-shadow: 0 6px 16px rgba(64, 145, 108, 0.4);
        transform: translateY(-2px);
    }
    
    /* Session history buttons */
    [data-testid="stSidebar"] button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.08);
        color: #F8F6F3 !important;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        font-weight: 400;
        text-align: left;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateX(4px);
    }
    
    /* Main content area */
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    /* Chat header */
    .chat-header {
        background: white;
        padding: 1.25rem 2rem;
        border-bottom: 1px solid #E8E6E3;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .chat-header h2 {
        color: #1B4332;
        font-size: 1.125rem;
        font-weight: 600;
        margin: 0;
    }
    
    .chat-header .subtitle {
        color: #6B7280;
        font-size: 0.75rem;
        font-weight: 400;
        margin-top: 0.25rem;
    }
    
    .connected-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #10B981;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .connected-dot {
        width: 8px;
        height: 8px;
        background: #10B981;
        border-radius: 50%;
    }
    
    /* Chat messages container */
    .chat-messages {
        padding: 2rem;
        max-width: 900px;
        margin: 0 auto;
    }
    
    /* Hide default Streamlit chat styling */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 1.5rem 0 !important;
        display: flex !important;
        width: 100% !important;
    }
    
    /* Assistant message - left aligned with avatar on left */
    .stChatMessage:has(> div > [data-testid="stChatMessageAvatarAssistant"]) {
        justify-content: flex-start !important;
    }
    
    .stChatMessage:has(> div > [data-testid="stChatMessageAvatarAssistant"]) > div {
        display: flex !important;
        flex-direction: row !important;
        gap: 1rem !important;
        max-width: 70% !important;
        align-items: flex-start !important;
    }
    
    /* User message - right aligned with avatar on right */
    .stChatMessage:has(> div > [data-testid="stChatMessageAvatarUser"]) {
        justify-content: flex-end !important;
    }
    
    .stChatMessage:has(> div > [data-testid="stChatMessageAvatarUser"]) > div {
        display: flex !important;
        flex-direction: row-reverse !important;
        gap: 1rem !important;
        max-width: 70% !important;
        align-items: flex-start !important;
    }
    
    /* Fallback using nth-child - assistant (odd) left, user (even) right */
    [data-testid="stChatMessage"]:nth-child(odd) {
        justify-content: flex-start !important;
    }
    
    [data-testid="stChatMessage"]:nth-child(even) {
        justify-content: flex-end !important;
    }
    
    [data-testid="stChatMessage"]:nth-child(even) > div {
        flex-direction: row-reverse !important;
    }
    
    /* Avatar styling */
    [data-testid="stChatMessageAvatarAssistant"],
    [data-testid="stChatMessageAvatarUser"] {
        width: 40px !important;
        height: 40px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        flex-shrink: 0 !important;
    }
    
    [data-testid="stChatMessageAvatarAssistant"] {
        background: #2D6A4F !important;
        color: white !important;
    }
    
    [data-testid="stChatMessageAvatarUser"] {
        background: #DC6B4A !important;
        color: white !important;
    }
    
    /* Message content styling */
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        background: white;
        border: 1.5px solid #E5E7EB;
        border-radius: 16px;
        padding: 1.25rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] [data-testid="stMarkdownContainer"] {
        background: #E8F5E9;
        border-color: #C8E6C9;
    }
    
    /* Message text */
    [data-testid="stChatMessage"] p {
        color: #1F2937;
        font-size: 0.9375rem;
        line-height: 1.6;
        margin: 0;
    }
    
    [data-testid="stChatMessage"] strong {
        color: #1B4332;
        font-weight: 600;
    }
    
    /* Highlighted text in messages */
    [data-testid="stChatMessage"] .highlight {
        color: #DC2626;
        font-weight: 600;
    }
    
    /* Chat input container */
    [data-testid="stChatInputContainer"] {
        border-top: 1px solid #E8E6E3;
        background: white;
        padding: 1.5rem 2rem;
    }
    
    /* Chat input */
    [data-testid="stChatInput"] {
        border-radius: 24px !important;
        border: 1.5px solid #E5E7EB !important;
        background: #F9FAFB !important;
        padding: 0.875rem 1.25rem !important;
        box-shadow: none !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #52B788 !important;
        box-shadow: 0 0 0 3px rgba(82, 183, 136, 0.1) !important;
    }
    
    /* Send button */
    [data-testid="stChatInput"] button {
        background: #2D6A4F !important;
        color: white !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(45, 106, 79, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stChatInput"] button:hover {
        background: #1B4332 !important;
        box-shadow: 0 4px 12px rgba(45, 106, 79, 0.4) !important;
        transform: scale(1.05) !important;
    }
    
    /* Info box */
    .stAlert {
        background: linear-gradient(135deg, #FFF8E7 0%, #FFE8CC 100%);
        border-left: 4px solid #D4A574;
        border-radius: 12px;
        padding: 1.5rem;
        color: #5C4A3A;
        box-shadow: 0 2px 8px rgba(212, 165, 116, 0.15);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #52B788 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F5F3F0;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #95D5B2;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #74C69D;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: transparent;
    }
    
    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
    }
    
    /* Input placeholder */
    input::placeholder, textarea::placeholder {
        color: #9CA3AF !important;
        font-weight: 400;
    }

</style>
""", unsafe_allow_html=True)

# Initialize database and session manager
@st.cache_resource
def init_database():
    db_manager = DatabaseManager()
    session_manager = SessionManager(db_manager)
    return db_manager, session_manager

db_manager, session_manager = init_database()

# Initialize crew
@st.cache_resource
def init_crew():
    return MandiSaathiCrew()

crew = init_crew()

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_session_loaded" not in st.session_state:
    st.session_state.current_session_loaded = False

# Sidebar for chat history
with st.sidebar:
    # Logo and title
    st.markdown("### 🌾 Mandi Saathi")
    st.caption("YOUR NEGOTIATION COMPANION")
    # st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("🌾 Powered by AI • Built for Farmers")
    st.markdown("Made with ❤️ by [Ankan](https://github.com/Ankan54)", unsafe_allow_html=True)
    
    # New chat button
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        st.session_state.session_id = None
        st.session_state.messages = []
        st.session_state.current_session_loaded = False
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Load previous sessions
    sessions = session_manager.get_all_sessions()
    
    if sessions:
        st.markdown("#### Recent Chats")
        st.markdown("<br>", unsafe_allow_html=True)
        
        for session in sessions[:10]:  # Show last 10 sessions
            # Create a preview of the first message
            preview = session["first_message"][:40] + "..." if len(session["first_message"]) > 40 else session["first_message"]
            
            # Session button with emoji
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown("💬")
            with col2:
                if st.button(
                    preview,
                    key=f"session_{session['session_id']}",
                    use_container_width=True
                ):
                    # Load this session
                    st.session_state.session_id = session["session_id"]
                    st.session_state.messages = session_manager.retrieve_chat_history(session["session_id"])
                    st.session_state.current_session_loaded = True
                    st.rerun()
            
            # Show session info
            st.caption(f"📅 {session['last_updated'][:16]} • {session['message_count']} msgs")
            st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("💭 No previous conversations yet")

# # Main chat interface
# # Chat header
# st.markdown(f"""
# <div class="chat-header">
#     <div>
#         <h2>🌾 Mandi Saathi</h2>
#         <div class="subtitle">Your Negotiation Companion</div>
#     </div>
#     <div class="connected-badge">
#         <div class="connected-dot"></div>
#         Connected
#     </div>
# </div>
# """, unsafe_allow_html=True)

# Display welcome message
if not st.session_state.messages:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("""
    **👋 Namaste! Welcome to Mandi Saathi**
    
    I'm here to help you negotiate better prices for your crops. Just tell me:
    
    • **What crop** you're selling (tamatar, aalu, pyaz, etc.)  
    • **Where you are** (your state and district)  
    • **What price** the trader is offering
    
    💬 You can write in **Hindi, English, or Hinglish** - whatever feels comfortable!
    
    **Example:** *"Mera 5 quintal tamatar hai, trader 1500 bol raha hai, Ballia mandi mein hoon"*
    """)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message("user", avatar="🧑‍🌾"):
        st.markdown(message["user"])
    with st.chat_message("assistant", avatar="👨‍💼"):
        st.markdown(message["assistant"])

# Chat input
if prompt := st.chat_input("Type your message in any language..."):
    # Create new session if needed
    if not st.session_state.session_id:
        st.session_state.session_id = session_manager.generate_session_id()
    
    # Display user message
    with st.chat_message("user", avatar="🧑‍🌾"):
        st.markdown(prompt)
    
    # Capture full chat history before appending current message
    chat_history = list(st.session_state.messages)

    # Add to messages
    st.session_state.messages.append({"user": prompt, "assistant": ""})

    # Get response from crew
    with st.chat_message("assistant", avatar="👨‍💼"):
        with st.spinner("🌾 Analyzing market prices and preparing your advice..."):
            try:
                response = crew.run(prompt, chat_history)
                st.markdown(response)
                
                # Update the last message with response
                st.session_state.messages[-1]["assistant"] = response
                
                # Store in database
                session_manager.store_chat_history(
                    st.session_state.session_id,
                    prompt,
                    response
                )
                
            except Exception as e:
                error_msg = f"😔 Sorry, I encountered an error: {str(e)}. Please try again."
                st.error(error_msg)
                st.session_state.messages[-1]["assistant"] = error_msg
