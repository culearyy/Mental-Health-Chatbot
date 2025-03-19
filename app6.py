import streamlit as st
import re
import random
import datetime

# --- 1. Streamlit Disclaimer (needed for a mental health application) ---
st.sidebar.markdown(
    """
    **Disclaimer:** This chatbot is for informational purposes only 
    and is not a substitute for professional mental health advice. 
    If you are in crisis, please contact your local emergency services immediately.
    
    **Emergency Resources:**
    - National Suicide Prevention Lifeline: 988 or 1-800-273-8255
    - Crisis Text Line: Text HOME to 741741
    """
)

# --- 2. Define comprehensive response patterns ---
responses = {
    # Depression-related patterns
    r"(?i).*feel(?:ing)?\s+(?:sad|down|depressed|unhappy|blue|low).*": [
        "I'm sorry to hear you're feeling down. Would you like to talk about what's causing these feelings?",
        "It's normal to feel sad sometimes. Can you tell me more about what's going on?",
        "I'm here to listen. What do you think might be contributing to these feelings?",
        "Depression can be really challenging. Have you considered talking to a mental health professional about these feelings?"
    ],
    
    # Anxiety-related patterns
    r"(?i).*feel(?:ing)?\s+(?:anxious|nervous|worried|stressed|overwhelmed|panic).*": [
        "Anxiety can be challenging. What's on your mind right now?",
        "I understand feeling anxious can be difficult. Is there something specific that's causing you worry?",
        "Take a deep breath. Would it help to talk about what's making you feel anxious?",
        "When you're feeling anxious, sometimes grounding techniques can help. Have you tried any relaxation methods?"
    ],
    
    # Sleep issues
    r"(?i).*(can't\s+sleep|insomnia|trouble\s+sleeping|sleep\s+problem).*": [
        "Sleep troubles can be frustrating. Have you tried establishing a regular sleep routine?",
        "I'm sorry to hear you're having trouble sleeping. How long has this been going on?",
        "Sleep is important for mental health. Have you considered talking to a healthcare provider about this?",
        "Sometimes limiting screen time before bed can help. Would you like some tips for better sleep hygiene?"
    ],
    
    # Loneliness
    r"(?i).*(lonely|alone|isolated|no\s+friends).*": [
        "Feeling lonely can be really hard. Would you like to talk about ways to connect with others?",
        "I'm sorry you're feeling lonely. Are there people in your life you could reach out to?",
        "Loneliness is a common human experience. What kinds of social connections would you like to have?",
        "Many people feel lonely sometimes. Have you considered joining groups with similar interests to yours?"
    ],
    
    # Seeking help
    r"(?i).*(need|want|seeking|looking\s+for)\s+help.*": [
        "I'm here to listen and chat, but for professional help, consider talking to a mental health professional.",
        "What kind of help are you looking for? I can try to point you in the right direction.",
        "I'm happy to chat, but remember I'm just a bot. For real support, consider reaching out to a counselor or therapist.",
        "It takes courage to seek help. Have you thought about what kind of support would be most helpful for you?"
    ],
    
    # Self-harm or suicidal thoughts (urgent responses)
    r"(?i).*(kill|hurt)\s+(myself|me)|(suicid|self.?harm|cut\s+myself).*": [
        "I'm concerned about what you're sharing. Please reach out to the National Suicide Prevention Lifeline at 988 or 1-800-273-8255 right away.",
        "This sounds serious, and you deserve immediate support. Please text HOME to 741741 to reach the Crisis Text Line.",
        "Your life matters. Please call 988 or go to your nearest emergency room for immediate help.",
        "I'm worried about you. Please reach out to someone you trust or call 988 for immediate support."
    ],
    
    # Gratitude
    r"(?i).*(thank|thanks)\s+(you|for).*": [
        "You're welcome! I'm here anytime you want to chat.",
        "I'm glad I could help. Feel free to come back anytime.",
        "Of course! Taking care of your mental health is important.",
        "No problem at all. I'm here to support you."
    ],
    
    # Greetings
    r"(?i)^(hi|hello|hey|howdy|hiya).*": [
        "Hello! How are you feeling today?",
        "Hi there! What's on your mind?",
        "Hey! How can I support you today?",
        f"Hello! It's {datetime.datetime.now().strftime('%A')}. How are you doing?"
    ],
    
    # Asking how the bot is
    r"(?i).*how\s+are\s+you.*": [
        "I'm here and ready to listen. More importantly, how are you doing?",
        "Thanks for asking! I'm here to focus on you. How are you feeling today?",
        "I'm functioning well, but I'd rather hear about you. How are things going?",
        "I appreciate your question! I'm here to support you. What's on your mind?"
    ],
    
    # Anger
    r"(?i).*(angry|mad|frustrated|pissed).*": [
        "It sounds like you're feeling frustrated. Would you like to talk more about what's causing these feelings?",
        "Anger is a normal emotion. What do you think triggered these feelings?",
        "When you're feeling angry, it can help to take a few deep breaths. Would you like to explore some coping strategies?",
        "I understand feeling angry can be intense. Is there something specific that happened?"
    ],
    
    # Relationship issues
    r"(?i).*(boyfriend|girlfriend|partner|spouse|husband|wife|relationship).*problem.*": [
        "Relationship challenges can be difficult. Would you like to share more about what's happening?",
        "I'm sorry to hear you're having relationship difficulties. What aspects are most concerning to you?",
        "Relationships require work and communication. Have you been able to discuss these issues with your partner?",
        "That sounds challenging. How long have these problems been going on?"
    ]
}

# Default responses for when no pattern matches
default_responses = [
    "I'm here to listen. Could you tell me more about that?",
    "How long have you been feeling this way?",
    "Thank you for sharing that with me. Would you like to explore this further?",
    "I'm interested in understanding more about your experience. Could you elaborate?",
    "That sounds challenging. How have you been coping with this?",
    "I appreciate you opening up. What do you think would help in this situation?",
    "I'm here to support you. What else is on your mind?",
    "Sometimes talking things through can help. Is there anything specific you'd like to focus on?"
]

# --- 3. Function to generate responses ---
def get_response(user_input):
    # Check for crisis keywords first (highest priority)
    crisis_pattern = r"(?i).*(kill|hurt)\s+(myself|me)|(suicid|self.?harm|cut\s+myself).*"
    if re.search(crisis_pattern, user_input):
        return ("I'm concerned about what you're sharing. If you're in immediate danger, please call 988 or go to your nearest emergency room. "
                "The National Suicide Prevention Lifeline (988) and Crisis Text Line (text HOME to 741741) are available 24/7.")
    
    # Check if user input matches any other patterns
    for pattern, response_list in responses.items():
        if re.search(pattern, user_input):
            return random.choice(response_list)
    
    # If no pattern matches, use default response
    return random.choice(default_responses)

# --- 4. Streamlit UI ---
st.title("Mental Health Chatbot")

# Initialize session state for conversation history if it doesn't exist
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Display conversation history
st.container(height=400)
for i, (user_msg, bot_msg) in enumerate(st.session_state.conversation):
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**Chatbot:** {bot_msg}")
    st.markdown("---")

# User input
user_input = st.text_input("You:", placeholder="How are you feeling today?")

if user_input:
    # Generate response
    response = get_response(user_input)
    
    # Add to conversation history
    st.session_state.conversation.append((user_input, response))
    
    # Force the UI to rerun and show the new message
    st.experimental_rerun()