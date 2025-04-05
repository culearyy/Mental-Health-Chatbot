import streamlit as st
from datetime import datetime
st.set_page_config(
    page_title="Mindful Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


if "conversation" not in st.session_state:
    st.session_state.conversation = [{
        "role": "Assistant",
        "content": "Hello! I'm your Mindful Companion, here to listen and support you. How are you feeling today?",
        "time": datetime.now().strftime("%H:%M"),
        "type": "greeting"
    }]

if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

if "current_mood" not in st.session_state:
    st.session_state["current_mood"] = "🟢 Neutral"

if "rerun_trigger" not in st.session_state:
    st.session_state["rerun_trigger"] = False

if "mood_history" not in st.session_state:
    st.session_state.mood_history = {}  

    
mood_colors = {
    "default": "Neutral",
    "depression": "Feeling Low",
    "anxiety": "Anxious",
    "crisis": "Urgent Support Needed"
}

if "current_mood" not in st.session_state:
    st.session_state["current_mood"] = "Neutral"  

import random

import re










import time
import torch
@st.cache_resource
def load_device():
    import torch
    return "cuda" if torch.cuda.is_available() else "cpu"

device = load_device()  
def update_topic_tracking(user_input):
    """Analyzes user input and categorizes conversation topics."""
    if "topics" not in st.session_state.metrics:
        st.session_state.metrics["topics"] = {}

    topic_keywords = {
        "anxiety": ["anxiety", "worried", "panic", "nervous"],
        "depression": ["depressed", "hopeless", "empty", "down"],
        "loneliness": ["alone", "lonely", "isolated"],
        "stress": ["stressed", "overwhelmed", "pressure"],
        "self-esteem": ["worthless", "useless", "hate myself"],
        "crisis": ["suicide", "self-harm", "end my life"],
        "abuse": ["abuse", "hurt", "violence"]
    }

    detected_topic = "general"
    for topic, keywords in topic_keywords.items():
        if any(word in user_input.lower() for word in keywords):
            detected_topic = topic
            break

    if detected_topic != "general":
        st.session_state.metrics["topics"].setdefault(detected_topic, 0)
        st.session_state.metrics["topics"][detected_topic] += 1



def update_mood_tracker(mood):
    """Updates the mood tracker based on detected sentiment."""
    mood_map = {
        "happy": "😊 Happy",
        "sad": "😢 Sad",
        "lonely": "😔 Lonely",
        "stressed": "😟 Stressed",
        "abused": "💔 Abused",
        "urgent": "🚨 Urgent Help Required",
        "neutral": "😐 Neutral"
    }
    
   
    st.session_state["current_mood"] = mood_map.get(mood, "😐 Neutral")











mood_colors = {
    "default": "🟢 Neutral",
    "depression": "🔴 Feeling Low",
    "anxiety": "🟡 Anxious",
    "crisis": "⚠️ Urgent Support Needed"
}



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
st.sidebar.header("🧠 Mood Tracker")
st.sidebar.write(f"**Current Mood:** {st.session_state['current_mood']}")

with st.sidebar:
    st.image("https://hbr.org/resources/images/article_assets/2022/10/A_Oct22_06_mental-health_1058086058.jpg", width=50)  # Placeholder for a logo
    st.title("Mindful Companion")
   
    st.sidebar.subheader("🧠 Your Mood Tracker")
    st.sidebar.markdown(f"### {st.session_state.get('current_mood', '🟢 Neutral')}")  


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
    
    
import streamlit as st
from datetime import datetime

st.sidebar.markdown("## 📊 Daily Mood Tracker")
st.sidebar.caption("How are you feeling today?")


mood_map = {
    "happy": "😊 Happy",
    "sad": "😢 Sad",
    "lonely": "😔 Lonely",
    "stressed": "😟 Stressed",
    "abused": "💔 Abused",
    "urgent": "🚨 Urgent Help Required",
    "neutral": "😐 Neutral"
}


st.markdown("""
    <style>
    div.stButton > button {
        font-size: 14px;
        padding: 8px 12px;
        border-radius: 10px;
        background-color: #4A90E2;
        color: white;
        border: none;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)


cols = st.sidebar.columns(3)  
for i, (mood_value, mood_text) in enumerate(mood_map.items()):
    with cols[i % 3]:  
        if st.button(mood_text, key=f"mood_btn_{mood_value}"):
            st.session_state.current_mood = mood_value
            today = datetime.now().strftime("%Y-%m-%d")
            if "mood_history" not in st.session_state:
                st.session_state.mood_history = {}
            st.session_state.mood_history[today] = mood_text


if "current_mood" in st.session_state:
    current_mood_display = mood_map.get(st.session_state.current_mood, "😐 Neutral")
    st.sidebar.markdown(f"### Your Current Mood: {current_mood_display}")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Self-Care Tip")

    tips = {
        "happy": "That's wonderful! 😊 Keep enjoying your day and spread some joy.",
        "sad": "I'm sorry you're feeling this way. 💛 Talking to someone may help.",
        "lonely": "Consider reaching out to a friend or journaling your thoughts. 🫂",
        "stressed": "Try taking a short break, practice mindfulness, or go for a walk. 🌿",
        "abused": "It's brave to acknowledge this. 💔 Please consider seeking support.",
        "urgent": "Reach out for immediate support. You're not alone. 🚨",
        "neutral": "Enjoy the calm. Consider doing something relaxing or creative. 🌼"
    }

    current_mood_tip = tips.get(st.session_state.current_mood, "Take care of yourself and remember that your feelings are valid. 💙")
    st.sidebar.info(current_mood_tip)


    






@st.cache_data
def preprocess_text(text):
    """Preprocess text with tokenization and lemmatization."""
    text = text.lower()
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(lemmatized)
















if "context_memory" not in st.session_state:
    st.session_state.context_memory = []


if "current_mood" not in st.session_state:
    st.session_state["current_mood"] = "Neutral"


mood_map = {
    "sadness": "😢 Sad",
    "stress": "😟 Stressed",
    "self-esteem": "😞 Low Confidence",
    "loneliness": "😔 Lonely",
    "suicide": "🚨 Crisis",
    "abuse": "💔 Hurt",
    "happy": "😊 Happy",
}

import random


import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)  

def find_best_response(user_input):
    """Uses Google Gemini API to generate a response and detect sentiment."""
    
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest") 
        response = model.generate_content([user_input])  
        bot_response = response.text.strip()
        
       
        sentiment_model = genai.GenerativeModel("gemini-1.5-flash-latest")  
        sentiment_analysis = sentiment_model.generate_content([
    f"Analyze the sentiment of this text: '{user_input}'. "
    "Return only one word from this list: happy, sad, lonely, stressed, abused, urgent, neutral."
])

        detected_mood = sentiment_analysis.text.strip().lower()

        return bot_response, detected_mood  

    except Exception as e:
        print("Error:", e)
        return "I'm here to support you. Can you tell me more about how you're feeling?", "neutral"



















   
    st.session_state.context_memory.append(user_input)
    if len(st.session_state.context_memory) > 3:
        st.session_state.context_memory.pop(0)

   
    if detected_tag and detected_tag in mood_map:
        st.session_state["current_mood"] = mood_map[detected_tag]

    return response










def generate_mental_health_response(user_input):
    """Generate chatbot response using Google Gemini API."""
    response, detected_mood = find_best_response(user_input)  
    update_mood_tracker(detected_mood)  
    return response if response else "I'm here to listen. How can I support you?"










import streamlit as st
from datetime import datetime

def on_send():
    user_msg = st.session_state.get("input_text", "").strip()

    if user_msg:
        timestamp = datetime.now().strftime("%H:%M")

       
        st.session_state["conversation"].append({
            "role": "User",
            "content": user_msg,
            "time": timestamp
        })

        
        if not is_relevant(user_msg):
            st.session_state["conversation"].append({
                "role": "Assistant",
                "content": "I'm here to talk about mental health, self-care, and emotional well-being. Let me know how I can support you.",
                "time": datetime.now().strftime("%H:%M")
            })
            st.session_state["input_text"] = ""  
            return

       
        if "metrics" not in st.session_state:
            st.session_state["metrics"] = {
                "total_messages": 0,
                "user_messages": 0,
                "bot_responses": 0,
                "topics": {}
            }

        
        st.session_state["metrics"]["user_messages"] += 1
        st.session_state["metrics"]["total_messages"] += 1

       
        update_topic_tracking(user_msg)

       
        simulate_bot_typing()

        
        st.session_state["input_text"] = ""










import threading

import time

def simulate_bot_typing():
    """Simulate chatbot typing, consider past messages, and generate responses."""
    user_messages = [msg["content"] for msg in st.session_state.conversation if msg["role"] == "User"]

    if user_messages:
        last_user_msg = user_messages[-1]
        st.session_state.is_typing = True
        time.sleep(1)  

        bot_msg = generate_mental_health_response(last_user_msg)

        st.session_state.conversation.append({
            "role": "Assistant",
            "content": bot_msg,
            "time": datetime.now().strftime("%H:%M")
        })

        
        st.session_state.metrics["bot_responses"] += 1

        st.session_state.is_typing = False







 






if "rerun_trigger" in st.session_state and st.session_state["rerun_trigger"]:
    st.session_state["rerun_trigger"] = False  











st.title("🧠 Mindful Companion")
st.caption("A supportive AI companion for mental wellness conversations")

tab_chat, tab_resources, tab_insights = st.tabs(["💬 Chat", "📚 Resources", "📊 Insights"])


with tab_chat:
    
    
    if "input_text" not in st.session_state:
        st.session_state["input_text"] = ""
    
    if "is_typing" not in st.session_state:
        st.session_state.is_typing = False
    
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.conversation:
        bubble_class = "assistant-bubble" if msg["role"] == "Assistant" else "user-bubble"
        st.markdown(
            f"""
            <div class="chat-bubble {bubble_class}">
                <p>{msg["content"]}</p>
                <div class="timestamp">{msg["time"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
   
    if st.session_state.is_typing:
     st.markdown(
        """
        <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
        """,
        unsafe_allow_html=True
    )
    if "typing_triggered" not in st.session_state or not st.session_state.typing_triggered:
        st.session_state.typing_triggered = True  
        simulate_bot_typing()  
    
    


    st.markdown('</div>', unsafe_allow_html=True)
    
    
    st.text_input("Type your message here:", key="input_text", on_change=on_send)

    st.button("Send", on_click=on_send)
    

with tab_resources:
    st.subheader("Helpful Mental Health Resources")
    st.markdown("""
    - [National Institute of Mental Health](https://www.nimh.nih.gov/health)
    - [MentalHealth.gov](https://www.mentalhealth.gov/)
    - [Psychology Today - Find a Therapist](https://www.psychologytoday.com/us/therapists)
    - [Mindful.org - Mindfulness Resources](https://www.mindful.org/)
    - [Anxiety and Depression Association of America](https://adaa.org/)
    """)

    st.markdown("---")
    st.info("**Always reach out to a trusted mental health professional for personalized support.**")


with tab_insights:
    st.subheader("Conversation Insights")
    
    
    if "metrics" not in st.session_state:
        st.session_state["metrics"] = {
            "total_messages": 0,
            "user_messages": 0,
            "bot_responses": 0,
            "topics": {}
        }

    
    st.session_state["metrics"].setdefault("user_messages", 0)
    st.session_state["metrics"].setdefault("bot_responses", 0)

  
    user_msgs = st.session_state["metrics"]["user_messages"]
    bot_msgs = st.session_state["metrics"]["bot_responses"]

    st.write(f"**Total User Messages:** {user_msgs}")
    st.write(f"**Total Bot Responses:** {bot_msgs}")

    
    topics_data = st.session_state["metrics"].get("topics", {})
    if topics_data:
        st.write("**Topics Discussed:**")
        for topic, count in topics_data.items():
            st.write(f"- {topic}: {count} times")
    else:
        
        if "conversation" in st.session_state and st.session_state["conversation"]:
            recent_msgs = [msg["content"] for msg in st.session_state["conversation"] if msg["role"] == "User"]
            if recent_msgs:
                st.write("No specific topics detected yet, but I noticed you mentioned:")
                for msg in recent_msgs[-3:]:  
                    st.write(f"💬 \"{msg}\"")
                st.write("Feel free to talk about how you're feeling or any concerns you have.")
            else:
                st.write("No conversation data yet. Start a conversation and I'll do my best to support you!")
        else:
            st.write("No conversation data yet. Start a conversation and I'll do my best to support you!")


import re


if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

import re

def is_relevant(user_input):
    """Enhanced relevancy filter with comprehensive keyword coverage and context awareness."""
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    
    st.session_state.conversation_history.append(user_input.lower())
    
    
    context_window = " ".join(st.session_state.conversation_history[-3:])
    
    
    trauma_context = any(word in context_window for word in [
        "rape", "raped", "abuse", "assault", "domestic violence", 
        "harassment", "molested", "trafficking", "victim", "survivor"
    ])
    
    
    emotional_keywords = [
        "angry", "violent", "helpless", "hurt", "lash out", "scared",
        "confused", "frustrated", "guilty", "shame", "regret",
        "is it okay", "what should I do", "am I overreacting", 
        "am I wrong", "I don't know what to do", "help me", "should I"
    ]

    
    relevant_keywords = [
        # 🧠 Mental Health Conditions
        "anxiety", "depression", "stress", "panic", "bipolar", "OCD", 
        "PTSD", "schizophrenia", "mania", "trauma", "grief", "loss", "sad", 
        "empty", "numb", "hopeless", "overwhelmed", "suicidal", "self-harm", 
        "worthless", "insomnia", "nightmares", "flashbacks",

        # 🧘 Self-Care and Coping
        "self-care", "meditation", "yoga", "exercise", "nutrition", 
        "therapy", "journaling", "mindfulness", "relaxation", "breathing", 
        "grounding", "positive thinking", "hobbies", "support group",

        # 💬 Friendly Greetings and Chat
        "hi", "hello", "hey", "how are you", "good morning", "good afternoon", 
        "good evening", "what's up", "how's it going", "long time no see",
        "yo", "sup", "howdy", "nice to meet you", "hope you're well",
        "how have you been", "great to see you", "it's been a while", 
        "happy to chat", "pleasure to meet you", "howdy partner", 
        "lovely to see you", "what's new", "good to hear from you",

        # ❤️ Encouragement and Positivity
        "you're amazing", "thank you", "appreciate it", "great job", "keep it up",
        "stay strong", "you got this", "believe in yourself", "i'm proud of you", 
        "good vibes", "sending love", "positive energy", "you matter", "bless you",
        "you can do it", "hang in there", "stay positive", "take it easy",

        # 🛡️ Criminal and Societal Concerns
        "violence", "crime", "kidnapping", "murder", "robbery", "human trafficking",
        "drug abuse", "extortion", "blackmail", "threat", "witness", "testify",
        "report", "justice", "legal help", "law enforcement", "court", "lawyer",

        # 🧑‍⚖️ Contextual Relevance
        "am I okay", "is it normal", "should I", "is this wrong", 
        "what should I do", "am I overreacting", "I don't know what to do",
        "I feel stuck", "I'm lost", "help me", "I need advice"
    ]

   
    if trauma_context or any(word in user_input.lower() for word in relevant_keywords + emotional_keywords):
        return True

    
    if trauma_context and any(word in user_input.lower() for word in emotional_keywords):
        return True

    
    if len(user_input.split()) > 5 or len(context_window.split()) > 20:
        return True

    return False







