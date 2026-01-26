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

# Custom CSS for Harvest Clarity design philosophy
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background - soft cream white */
    .stApp {
        background-color: #F8F6F3;
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
    [data-testid="stSidebar"] h1 {
        color: #F8F6F3 !important;
        font-weight: 600;
        font-size: 1.5rem;
        letter-spacing: 0.02em;
        margin-bottom: 0.5rem;
    }
    
    /* Sidebar caption */
    [data-testid="stSidebar"] .element-container p {
        color: #B7E4C7 !important;
        font-size: 0.75rem;
        font-weight: 300;
        letter-spacing: 0.05em;
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
    }
    
    [data-testid="stSidebar"] button[kind="primary"]:hover {
        background: linear-gradient(135deg, #40916C 0%, #2D6A4F 100%);
        box-shadow: 0 6px 16px rgba(64, 145, 108, 0.4);
        transform: translateY(-2px);
    }
    
    /* Session history buttons */
    [data-testid="stSidebar"] button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.1);
        color: #F8F6F3 !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
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
        padding: 2rem 3rem;
        max-width: 1200px;
    }
    
    /* Title styling */
    h1 {
        color: #1B4332;
        font-weight: 700;
        font-size: 2.5rem;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        color: #2D6A4F;
        font-weight: 600;
        letter-spacing: 0.01em;
    }
    
    /* Info box - warm amber tones */
    .stAlert {
        background: linear-gradient(135deg, #FFF8E7 0%, #FFE8CC 100%);
        border-left: 4px solid #D4A574;
        border-radius: 12px;
        padding: 1.5rem;
        color: #5C4A3A;
        box-shadow: 0 2px 8px rgba(212, 165, 116, 0.15);
    }
    
    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: white;
        border-radius: 16px;
        padding: 1.25rem;
        margin: 1rem 0;
        box-shadow: 0 2px 12px rgba(27, 67, 50, 0.08);
        border: 1px solid rgba(27, 67, 50, 0.05);
    }
    
    /* User message - soft green tint */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, #E8F5E9 0%, #D7F0DD 100%);
        border-left: 3px solid #52B788;
    }
    
    /* Assistant message - warm cream */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: white;
        border-left: 3px solid #D4A574;
    }
    
    /* Chat input */
    [data-testid="stChatInput"] {
        border-radius: 16px;
        border: 2px solid #D7F0DD;
        background: white;
        padding: 0.75rem;
        box-shadow: 0 4px 16px rgba(27, 67, 50, 0.1);
        transition: all 0.3s ease;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #52B788;
        box-shadow: 0 4px 20px rgba(82, 183, 136, 0.2);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #52B788 !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(27, 67, 50, 0.1);
        margin: 2rem 0;
    }
    
    /* Caption text */
    .caption {
        color: #74A98A;
        font-size: 0.875rem;
        font-weight: 300;
        letter-spacing: 0.03em;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F8F6F3;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #95D5B2;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #74C69D;
    }
    
    /* Card-like containers */
    .element-container {
        transition: all 0.3s ease;
    }
    
    /* Rounded corners everywhere */
    button, input, textarea, select {
        border-radius: 10px !important;
    }
    
    /* Success message */
    .stSuccess {
        background: linear-gradient(135deg, #D7F0DD 0%, #B7E4C7 100%);
        border-left: 4px solid #52B788;
        border-radius: 12px;
        color: #1B4332;
    }
    
    /* Error message */
    .stError {
        background: linear-gradient(135deg, #FFE8E8 0%, #FFD4D4 100%);
        border-left: 4px solid #D4A574;
        border-radius: 12px;
        color: #5C4A3A;
    }
    
    /* Header area */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Smooth transitions */
    * {
        transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
    }
    
    /* Chat message avatars */
    [data-testid="stChatMessageAvatarUser"] {
        background: linear-gradient(135deg, #52B788 0%, #40916C 100%);
    }
    
    [data-testid="stChatMessageAvatarAssistant"] {
        background: linear-gradient(135deg, #D4A574 0%, #B8956A 100%);
    }
    
    /* Input placeholder */
    input::placeholder, textarea::placeholder {
        color: #95D5B2 !important;
        font-weight: 300;
    }
    
    /* Button hover effects */
    button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Markdown in chat */
    [data-testid="stChatMessage"] p {
        line-height: 1.6;
        color: #2D6A4F;
    }
    
    [data-testid="stChatMessage"] strong {
        color: #1B4332;
        font-weight: 600;
    }
    
    /* Info box icons */
    .stAlert [data-testid="stMarkdownContainer"] {
        line-height: 1.7;
    }
    
    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .stSpinner {
        animation: pulse 1.5s ease-in-out infinite;
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
    
    st.markdown("<br>", unsafe_allow_html=True)
    
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
    
    st.markdown("---")
    st.caption("🌾 Powered by AI • Built for Farmers")

# Main chat interface
st.title("🌾 Mandi Saathi")
st.markdown("##### Get Fair Prices for Your Produce")
st.markdown("<br>", unsafe_allow_html=True)

# Display welcome message
if not st.session_state.messages:
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
    with st.chat_message("user"):
        st.markdown(message["user"])
    with st.chat_message("assistant"):
        st.markdown(message["assistant"])

# Chat input
if prompt := st.chat_input("Type your message in any language... (Hindi, English, Hinglish)"):
    # Create new session if needed
    if not st.session_state.session_id:
        st.session_state.session_id = session_manager.generate_session_id()
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Capture full chat history before appending current message
    chat_history = list(st.session_state.messages)

    # Add to messages
    st.session_state.messages.append({"user": prompt, "assistant": ""})

    # Get response from crew
    with st.chat_message("assistant"):
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

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.caption("🌾 Mandi Saathi • Empowering farmers with AI-driven market intelligence")
st.caption("💡 Powered by AI • Built with care for Indian farmers")
