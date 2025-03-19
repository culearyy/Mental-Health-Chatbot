import streamlit as st
import random
import re
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import json
import time


try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('wordnet')


st.set_page_config(
    page_title="Mindful Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


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


with st.sidebar:
    st.image("https://hbr.org/resources/images/article_assets/2022/10/A_Oct22_06_mental-health_1058086058.jpg", width=50)  # Placeholder for a logo
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
    
    # Added mood tracker to sidebar
    st.markdown("### 📊 Daily Mood Tracker")
    st.caption("How are you feeling today?")
    
    moods = {
        "😄 Great": "great",
        "🙂 Good": "good",
        "😐 Neutral": "neutral",
        "🙁 Down": "down",
        "😞 Struggling": "struggling"
    }
    
    # Initialized mood in session state if not exists
    if "current_mood" not in st.session_state:
        st.session_state.current_mood = None
        st.session_state.mood_history = {}
    
    # Created mood buttons in a single row
    mood_cols = st.columns(len(moods))
    for idx, (mood_text, mood_value) in enumerate(moods.items()):
        # Check if this mood is selected
        is_selected = st.session_state.current_mood == mood_value
        button_style = "selected" if is_selected else ""
        
        # Instead of clickable markdown, use a button:
        if mood_cols[idx].button(mood_text, key=f"mood_btn_{mood_value}"):
            st.session_state.current_mood = mood_value
            # Record mood with timestamp
            today = datetime.now().strftime("%Y-%m-%d")
            st.session_state.mood_history[today] = mood_value
    
    # Show self-care tip based on mood
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

# ---------------------------------------------------
#  Load or create mental health responses
# ---------------------------------------------------
try:
    with open("mental_health_responses.json", "r") as f:
        mental_health_responses = json.load(f)
except:
    # Fallback if file operations aren't permitted
    mental_health_responses = {
        "greeting": [
            "Hello! I'm your Mindful Companion. How are you feeling today?",
            "Hi there. I'm here to listen and support you. What's on your mind?"
        ],
        "default": [
            "Thank you for sharing that with me. Would you like to tell me more?",
            "I'm here to listen. How has this been affecting you?"
        ]
    }

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# ---------------------------------------------------
#  Preprocessing and Classification
# ---------------------------------------------------
def preprocess_text(text):
    """Preprocess text with tokenization and lemmatization."""
    text = text.lower()
    tokens = word_tokenize(text)
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(lemmatized)

def get_response_type(user_input):
    """Enhanced response classification with regex + scoring."""
    text = preprocess_text(user_input.lower())
    
    # 1. Crisis detection
    crisis_patterns = [
        r"(kill|hurt|harm)\s+(myself|me)",
        r"suicid",
        r"self.?harm",
        r"end\s+(my|this)\s+life",
        r"don't\s+want\s+to\s+(live|be\s+alive)",
        r"want\s+to\s+die",
        r"cut\s+myself",
        r"no\s+reason\s+to\s+live"
    ]
    for pattern in crisis_patterns:
        if re.search(pattern, text):
            return "crisis"
    
    # 2. Scoring system
    category_scores = {
        "greeting": 0,
        "depression": 0,
        "anxiety": 0,
        "stress": 0,
        "sleep": 0,
        "relationships": 0,
        "self_care": 0,
        "positive": 0,
        "mindfulness": 0,
        "trauma": 0,
        "motivation": 0,
        "grief": 0,
        "general_check": 0
    }
    
    patterns = {
        "greeting": [
            (r"^(hi|hello|hey|good\s+morning|good\s+afternoon|good\s+evening)", 2),
            (r"how\s+are\s+you", 1.5)
        ],
        "depression": [
            (r"depress", 2),
            (r"(sad|down|unhappy|blue|hopeless)", 1.5),
            (r"(worthless|empty|numb)", 1.5),
            (r"no\s+energy", 1),
            (r"don't\s+enjoy", 1)
        ],
        "anxiety": [
            (r"anxi", 2),
            (r"(worry|nervous|panic)", 1.5),
            (r"(overwhelm|racing\s+thought|racing\s+mind)", 1.5),
            (r"(fear|afraid|scared)", 1),
            (r"heart\s+racing", 1)
        ],
        "stress": [
            (r"stress", 2),
            (r"(pressure|burden|overwhelm)", 1.5),
            (r"too\s+much", 1),
            (r"(burnout|burning\s+out)", 1.5),
            (r"(cope|coping)", 1)
        ],
        "sleep": [
            (r"sleep", 2),
            (r"(insomnia|can't\s+sleep|trouble\s+sleeping)", 1.5),
            (r"(tired|exhausted|fatigue)", 1),
            (r"(nightmare|bad\s+dream)", 1.5),
            (r"wake\s+up", 1)
        ],
        "relationships": [
            (r"relationship", 2),
            (r"(partner|spouse|husband|wife|boyfriend|girlfriend)", 1.5),
            (r"(friend|family|parent|child)", 1),
            (r"(conflict|argument|fight)", 1.5),
            (r"(boundary|boundaries)", 1.5),
            (r"(divorce|breakup|broke\s+up)", 1.5)
        ],
        "self_care": [
            (r"self.?care", 2),
            (r"(relax|calm|peace)", 1.5),
            (r"(meditat|yoga|exercise)", 1),
            (r"(bath|massage|spa)", 1),
            (r"take\s+care\s+of\s+myself", 1.5)
        ],
        "positive": [
            (r"(thank|thanks|helpful)", 2),
            (r"(better|improving|progress)", 1.5),
            (r"(grateful|thankful|appreciate)", 1.5),
            (r"(hope|hopeful)", 1),
            (r"(good|great|excellent)", 1)
        ],
        "mindfulness": [
            (r"(mindful|meditation|breath)", 2),
            (r"(present|aware|awareness)", 1.5),
            (r"(focus|attention)", 1),
            (r"(ground|grounding)", 1.5),
            (r"(calm|center|balance)", 1)
        ],
        "trauma": [
            (r"trauma", 2),
            (r"(ptsd|flashback|trigger)", 1.5),
            (r"(abuse|assault|attack)", 1.5),
            (r"(wound|hurt|pain)", 1),
            (r"(memory|remember|childhood)", 1)
        ],
        "motivation": [
            (r"motivat", 2),
            (r"(goal|purpose|meaning)", 1.5),
            (r"(stuck|procrastinate|avoid)", 1.5),
            (r"(lazy|can't\s+do|hard\s+to\s+start)", 1),
            (r"(accomplish|achieve|finish)", 1)
        ],
        "grief": [
            (r"(grief|grieve|mourn)", 2),
            (r"(loss|lost|died|death)", 1.5),
            (r"(miss|missing)", 1),
            (r"(gone|passed\s+away)", 1.5),
            (r"(funeral|memorial)", 1.5)
        ]
    }
    
    for category, pattern_list in patterns.items():
        for pattern, weight in pattern_list:
            if re.search(pattern, text):
                category_scores[category] += weight
    
    # General check if very short input
    if len(text.split()) < 5:
        category_scores["general_check"] += 1.5
    
    # Find highest-scoring category
    max_score = 0
    selected_category = "default"
    for cat, score in category_scores.items():
        if score > max_score:
            max_score = score
            selected_category = cat
    
    return selected_category if max_score > 0.5 else "default"

def generate_mental_health_response(user_input):
    """Get a random response from the appropriate category."""
    response_type = get_response_type(user_input)
    possible_responses = mental_health_responses.get(response_type, mental_health_responses["default"])
    return random.choice(possible_responses), response_type

# ---------------------------------------------------
#  Callbacks for Sending + Typing
# ---------------------------------------------------
def on_send():
    """Triggered when the user presses 'Send'."""
    user_msg = st.session_state["input_text"]
    if user_msg.strip():
        # Append user message
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.conversation.append({
            "role": "User",
            "content": user_msg,
            "time": timestamp
        })
        # Indicate the bot is 'typing'
        st.session_state.is_typing = True
        # Clear the input box
        st.session_state["input_text"] = ""

        # Force a rerun to display typing indicator
        st.experimental_rerun()

def simulate_bot_typing():
    """Simulate a short typing delay, then add the bot message."""
    time.sleep(1.5)  # Wait to simulate typing
    # Get the last user message
    last_user_msg = next(
        (msg for msg in reversed(st.session_state.conversation) if msg["role"] == "User"),
        None
    )
    if last_user_msg:
        bot_msg, response_type = generate_mental_health_response(last_user_msg["content"])
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.conversation.append({
            "role": "Assistant",
            "content": bot_msg,
            "time": timestamp,
            "type": response_type
        })
        # Update metrics
        if "metrics" not in st.session_state:
            st.session_state.metrics = {"total_messages": 0, "topics": {}}
        st.session_state.metrics["total_messages"] += 1
        st.session_state.metrics["topics"][response_type] = st.session_state.metrics["topics"].get(response_type, 0) + 1
    
    st.session_state.is_typing = False
    st.experimental_rerun()

# ---------------------------------------------------
#  Tabs for Chat, Resources, Insights
# ---------------------------------------------------
st.title("🧠 Mindful Companion")
st.caption("A supportive AI companion for mental wellness conversations")

tab_chat, tab_resources, tab_insights = st.tabs(["💬 Chat", "📚 Resources", "📊 Insights"])

#  Chat Tab
with tab_chat:
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
        st.session_state.conversation.append({
            "role": "Assistant", 
            "content": "Hello! I'm your Mindful Companion, here to listen and support you. How are you feeling today?",
            "time": datetime.now().strftime("%H:%M"),
            "type": "greeting"
        })
    
    if "input_text" not in st.session_state:
        st.session_state["input_text"] = ""
    
    if "is_typing" not in st.session_state:
        st.session_state.is_typing = False
    
    # Display chat messages
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
    # If the bot is 'typing', show indicator
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
        # Simulate bot typing in the background
        simulate_bot_typing()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # User input + Send button
    st.text_input("Type your message here:", key="input_text", on_change=None)
    st.button("Send", on_click=on_send)
    
#  Resources Tab
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

#  Insights Tab
with tab_insights:
    st.subheader("Conversation Insights")
    if "metrics" not in st.session_state:
        st.session_state.metrics = {"total_messages": 0, "topics": {}}
    
    total_msgs = st.session_state.metrics["total_messages"]
    st.write(f"**Total Bot Responses:** {total_msgs}")
    
    if total_msgs > 0:
        st.write("**Topics Discussed:**")
        for topic, count in st.session_state.metrics["topics"].items():
            st.write(f"- {topic}: {count} times")
    else:
        st.write("No conversation data yet. Ask the chatbot something!")

