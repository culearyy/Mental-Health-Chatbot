import streamlit as st
import random
import re
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import json
import time

# Ensure required NLTK resources are downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('wordnet')

# Streamlit page configuration
st.set_page_config(
    page_title="Mindful Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar setup
with st.sidebar:
    st.image("https://hbr.org/resources/images/article_assets/2022/10/A_Oct22_06_mental-health_1058086058.jpg", width=50)
    st.title("Mindful Companion")
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

    # Mood tracker in the sidebar
    st.markdown("### 📊 Daily Mood Tracker")
    st.caption("How are you feeling today?")
    moods = {
        "😄 Great": "great",
        "🙂 Good": "good",
        "😐 Neutral": "neutral",
        "🙁 Down": "down",
        "😞 Struggling": "struggling"
    }

    if "current_mood" not in st.session_state:
        st.session_state.current_mood = None
        st.session_state.mood_history = {}

    mood_cols = st.columns(len(moods))
    for idx, (mood_text, mood_value) in enumerate(moods.items()):
        if mood_cols[idx].button(mood_text, key=f"mood_btn_{mood_value}"):
            st.session_state.current_mood = mood_value
            today = datetime.now().strftime("%Y-%m-%d")
            st.session_state.mood_history[today] = mood_value

    if st.session_state.current_mood:
        st.markdown("---")
        st.markdown("### 💡 Self-Care Tip")
        tips = {
            "great": "Wonderful! Celebrate your positive state by sharing your energy with someone who might need it today.",
            "good": "That's good to hear! Consider journaling about what's working well so you can reference it in the future.",
            "neutral": "Take a moment for a quick mindfulness exercise—focus on your breath for just 30 seconds.",
            "down": "It's okay to feel down sometimes. Consider going for a short walk—nature and movement can help shift your mood.",
            "struggling": "I'm sorry you're struggling. Remember feelings are temporary. Consider reaching out to someone you trust today."
        }
        st.info(tips[st.session_state.current_mood])

# Load or create mental health responses
try:
    with open("mental_health_responses.json", "r") as f:
        mental_health_responses = json.load(f)
except FileNotFoundError:
    mental_health_responses = {
        "greeting": ["Hello! I'm your Mindful Companion. How are you feeling today?"],
        "default": ["I'm here to listen. Can you tell me more about that?"]
    }

lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(lemmatized)

def get_response_type(user_input):
    text = preprocess_text(user_input.lower())
    
    crisis_patterns = [
        r"(kill|hurt|harm)\s+(myself|me)", r"suicid", r"self.?harm", 
        r"end\s+(my|this)\s+life", r"don't\s+want\s+to\s+(live|be\s+alive)"
    ]
    
    for pattern in crisis_patterns:
        if re.search(pattern, text):
            return "crisis"
    
    patterns = {
        "greeting": [r"^(hi|hello|hey)", r"how\s+are\s+you"],
        "depression": [r"depress", r"(sad|unhappy)", r"hopeless"],
        # Add more categories here...
    }
    
    for category, regex_list in patterns.items():
        for regex in regex_list:
            if re.search(regex, text):
                return category

    return "default"

def generate_mental_health_response(user_input):
    response_type = get_response_type(user_input)
    possible_responses = mental_health_responses.get(response_type, mental_health_responses["default"])
    return random.choice(possible_responses), response_type

def on_send():
    user_msg = st.session_state["input_text"].strip()
    
    if not user_msg:
        st.warning("Please enter a valid message.")
        return
    
    timestamp = datetime.now().strftime("%H:%M")
    
    st.session_state.conversation.append({
        "role": "User",
        "content": user_msg,
        "time": timestamp
    })
    
    st.session_state.is_typing = True
    st.session_state["input_text"] = ""
    
def simulate_bot_typing():
    time.sleep(1.5)
    
    last_user_msg = next((msg for msg in reversed(st.session_state.conversation) if msg["role"] == "User"), None)
    
    if last_user_msg:
        bot_msg, response_type = generate_mental_health_response(last_user_msg["content"])
        
        timestamp = datetime.now().strftime("%H:%M")
        
        st.session_state.conversation.append({
            "role": "Assistant",
            "content": bot_msg,
            "time": timestamp,
            "type": response_type
        })
        
st.title("🧠 Mindful Companion")
st.caption("A supportive AI companion for mental wellness conversations")

tab_chat, tab_resources, tab_insights = st.tabs(["💬 Chat", "📚 Resources", "📊 Insights"])

with tab_chat:
    if "conversation" not in st.session_state:
        st.session_state.conversation = [{
            "role": "Assistant",
            "content": mental_health_responses["greeting"][0],
            "time": datetime.now().strftime("%H:%M"),
            "type": "greeting"
        }]
    
    if not ("input_text" in st.session_state):
        st.session_state["input_text"] = ""