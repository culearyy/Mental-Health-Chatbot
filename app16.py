import asyncio
import streamlit as st
from datetime import datetime
import random
import re
import json
import time
import torch
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Set up the asyncio loop if not already running
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Download NLTK data (only if not already installed)
@st.cache_data
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')

download_nltk_data()  # Ensure downloads happen only once

# Configure the Streamlit page
st.set_page_config(
    page_title="Mindful Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables (only once)
if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {
            "role": "Assistant",
            "content": "Hello! I'm your Mindful Companion. How are you feeling today?",
            "time": datetime.now().strftime("%H:%M"),
            "type": "greeting"
        }
    ]

if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

if "typing_triggered" not in st.session_state:
    st.session_state.typing_triggered = False

if "current_mood" not in st.session_state:
    st.session_state["current_mood"] = "neutral"  # Stored mood values: great, good, neutral, down, struggling

if "mood_history" not in st.session_state:
    st.session_state["mood_history"] = {}

if "rerun_trigger" not in st.session_state:
    st.session_state["rerun_trigger"] = False

# Define mood color or description mapping if needed elsewhere (not used in tip display)
mood_colors = {
    "default": "Neutral",
    "depression": "Feeling Low",
    "anxiety": "Anxious",
    "crisis": "Urgent Support Needed"
}

# Load dataset from JSON file
with open("combined_dataset.json", "r", encoding="utf-8") as file:
    mental_health_data = json.load(file)

@st.cache_resource
def load_device():
    return "cuda" if torch.cuda.is_available() else "cpu"

device = load_device()  # Cache device setting

# Load or create mental health responses from file
try:
    with open("mental_health_responses.json", "r") as f:
        mental_health_responses = json.load(f)
except FileNotFoundError:
    st.warning("⚠️ mental_health_responses.json file not found! Using default responses.")
    mental_health_responses = {
        "greeting": ["Hello! How can I support you today?", "Hey there! How are you feeling?"],
        "depression": ["I'm here for you. Want to talk about it?", "You're not alone. How can I help?"],
        "anxiety": ["Take a deep breath. What's on your mind?", "I understand. Let's take this one step at a time."],
        "default": ["I'm here to listen. Tell me more."]
    }

# App Styling
st.markdown("""
<style>
    /* Overall App Styling */
    .main {
        background-color: #fafafa;
        padding: 2rem;
    }
    
    /* Header Styling */
    h1 {
        color: #4285F4;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    
    /* Chat Container */
    .chat-container {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        max-height: 500px;
        overflow-y: auto;
    }
    
    /* Chat Bubbles */
    .chat-bubble {
        border-radius: 18px;
        padding: 12px 16px;
        margin-bottom: 12px;
        max-width: 80%;
        word-wrap: break-word;
        position: relative;
        animation: fadeIn 0.3s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-bubble {
        background-color: #E2F2FF;
        color: #1E3A8A;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }
    
    .assistant-bubble {
        background-color: #F0F4F9;
        color: #333;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 0.7rem;
        color: #888;
        margin-top: 4px;
        text-align: right;
    }
    
    /* Input box styling */
    .stTextInput {
        border-radius: 25px;
    }
    
    .stTextInput input {
        border-radius: 25px !important;
        padding: 10px 20px !important;
        border: 1px solid #ddd !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }
    
    .stTextInput input:focus {
        border-color: #4285F4 !important;
        box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2) !important;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 25px;
        background-color: #4285F4;
        color: white;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #3367D6;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #F8F9FA;
    }
    
    /* Resource cards */
    .resource-card {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid #4285F4;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Mood tracker */
    .mood-btn {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 20px;
        padding: 10px;
        margin: 5px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .mood-btn:hover {
        transform: scale(1.05);
        border-color: #4285F4;
    }
    
    .mood-btn.selected {
        background-color: #E2F2FF;
        border-color: #4285F4;
        font-weight: bold;
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        padding: 10px;
    }
    
    .typing-indicator span {
        height: 10px;
        width: 10px;
        margin: 0 2px;
        background-color: #9E9E9E;
        border-radius: 50%;
        opacity: 0.4;
        animation: typing-animation 1.5s infinite;
    }
    
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.3s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.6s;
    }
    
    @keyframes typing-animation {
        0% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.2); }
        100% { opacity: 0.4; transform: scale(1); }
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        background-color: #F8F9FA;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        border-top: 2px solid #4285F4 !important;
        color: #4285F4 !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://hbr.org/resources/images/article_assets/2022/10/A_Oct22_06_mental-health_1058086058.jpg", width=50)
    st.title("Mindful Companion")
    st.sidebar.subheader("🧠 Your Mood Tracker")
    st.sidebar.markdown(f"### {st.session_state.get('current_mood', 'neutral').capitalize()}")
    st.markdown("""
    ## Important Notice
    **This AI chatbot is for educational and support purposes only** and is not a substitute for professional mental health advice, diagnosis, or treatment.
    """)
    st.warning("""
    ### If you need immediate help:
    - **National Suicide Prevention Lifeline**: 988 or 1-800-273-8255
    - **Crisis Text Line**: Text HOME to 741741
    - **Call 911** or go to your nearest emergency room
    """)
    st.info("Always consult with qualified mental health professionals for mental health concerns.")
    
    st.markdown("### 📊 Daily Mood Tracker")
    st.caption("How are you feeling today?")
    
    # Define moods with keys matching the tips
    moods = {
        "😄 Great": "great",
        "🙂 Good": "good",
        "😐 Neutral": "neutral",
        "🙁 Down": "down",
        "😞 Struggling": "struggling"
    }
    
    mood_cols = st.columns(len(moods))
    for idx, (mood_text, mood_value) in enumerate(moods.items()):
        is_selected = st.session_state.current_mood == mood_value
        if mood_cols[idx].button(mood_text, key=f"mood_btn_{mood_value}"):
            st.session_state.current_mood = mood_value
            today = datetime.now().strftime("%Y-%m-%d")
            st.session_state.mood_history[today] = mood_value
    
    if st.session_state.current_mood:
        st.markdown("---")
        st.markdown("### 💡 Self-Care Tip")
        # Updated tips dictionary with keys matching the mood values
        tips = {
            "great": "That's fantastic – keep that energy flowing!",
            "good": "Great to hear you're doing well. Keep taking care of yourself!",
            "neutral": "Stay mindful and take regular breaks.",
            "down": "It might help to talk to a friend or try a small self-care activity.",
            "struggling": "If things feel overwhelming, consider reaching out to someone you trust or a professional."
        }
        st.info(tips.get(st.session_state.current_mood, "Take care and stay mindful!"))

# Main chat container and conversation display
st.markdown("## Conversation")
chat_container = st.container()

with chat_container:
    for msg in st.session_state.conversation:
        if msg["role"] == "User":
            st.markdown(f"""<div class="chat-bubble user-bubble">
                            {msg["content"]}
                            <div class="timestamp">{msg["time"]}</div>
                            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="chat-bubble assistant-bubble">
                            {msg["content"]}
                            <div class="timestamp">{msg["time"]}</div>
                            </div>""", unsafe_allow_html=True)

# Text input for new messages
user_input = st.text_input("Your message:", key="input_text")

# Function to simulate bot response; ensures one response per user message
def generate_bot_response(user_message):
    # For demonstration, choose a random default response.
    response = random.choice(mental_health_responses.get("default", ["I'm here to listen."]))
    return response

if st.button("Send"):
    if user_input.strip() != "":
        # Append user message
        st.session_state.conversation.append({
            "role": "User",
            "content": user_input,
            "time": datetime.now().strftime("%H:%M"),
            "type": "user"
        })
        # Clear input for next message
        st.session_state.input_text = ""
        
        # Generate bot response only if the last message is from the user
        if st.session_state.conversation[-1]["role"] == "User":
            bot_response = generate_bot_response(user_input)
            st.session_state.conversation.append({
                "role": "Assistant",
                "content": bot_response,
                "time": datetime.now().strftime("%H:%M"),
                "type": "response"
            })
        # Rerun to update the UI
        st.experimental_rerun()
