import streamlit as st
import random
import re
from datetime import datetime

# ---------------------------------------------------
# 1. Set Page Config FIRST
# ---------------------------------------------------
st.set_page_config(page_title="Mental Health Chatbot", layout="centered")

# ---------------------------------------------------
# 2. Comprehensive Mental Health Disclaimer (Sidebar)
# ---------------------------------------------------
st.sidebar.markdown(
    """
    ## Important Notice
    **This chatbot is for educational purposes only** and is not a substitute for professional mental health advice, diagnosis, or treatment.
    
    ### If you need immediate help:
    - National Suicide Prevention Lifeline: 988 or 1-800-273-8255
    - Crisis Text Line: Text HOME to 741741
    - Call 911 or go to your nearest emergency room
    
    Always consult with qualified mental health professionals regarding mental health concerns.
    """
)

# ---------------------------------------------------
# 3. Define the conversation patterns and responses
# ---------------------------------------------------
mental_health_responses = {
    # Greetings
    "greeting": [
        "Hello! I'm here to provide support. How are you feeling today?",
        "Hi there. I'm your mental health companion. How can I help you today?",
        "Welcome. I'm here to listen and support you. What's on your mind?",
        "Greetings! How are you doing today? I'm here to chat."
    ],
    
    # General mental health check-ins
    "general_check": [
        "How have you been managing your mental health lately?",
        "On a scale of 1-10, how would you rate your mood today?",
        "Have you been practicing any self-care activities recently?",
        "What's been on your mind lately that you'd like to discuss?"
    ],
    
    # Depression-related responses
    "depression": [
        "I'm sorry to hear you're feeling down. Depression can be really challenging. Have you spoken with a mental health professional about these feelings?",
        "It's important to know that depression is a common condition and help is available. Would you like to discuss some coping strategies?",
        "When we're feeling depressed, even small tasks can feel overwhelming. Have you been able to maintain your daily routines?",
        "Depression often makes us feel isolated. Do you have support people in your life you can reach out to?"
    ],
    
    # Anxiety-related responses
    "anxiety": [
        "Anxiety can be really difficult to manage. Deep breathing exercises can sometimes help in the moment. Would you like to try one?",
        "When we're anxious, our thoughts often race to worst-case scenarios. Is there a specific worry that's on your mind right now?",
        "Anxiety is your body's natural response to stress. Have you noticed any specific triggers for your anxiety?",
        "Grounding techniques can be helpful for anxiety. Have you tried any methods like the 5-4-3-2-1 technique?"
    ],
    
    # Stress management
    "stress": [
        "Managing stress is important for our overall wellbeing. What usually helps you relax when you're feeling stressed?",
        "Stress can build up over time. Have you been able to take breaks and practice self-care?",
        "Sometimes breaking down big tasks into smaller steps can help reduce stress. Would you like to discuss some stress management techniques?",
        "Regular exercise, good sleep, and healthy eating can all help manage stress. Have you been able to maintain these habits?"
    ],
    
    # Sleep issues
    "sleep": [
        "Sleep problems can significantly impact our mental health. Have you established a regular sleep routine?",
        "Falling asleep can be difficult when our minds are racing. Have you tried any relaxation techniques before bed?",
        "Screen time before bed can interfere with sleep. Do you typically use electronic devices right before sleeping?",
        "Creating a comfortable sleep environment can help. Is your bedroom conducive to good sleep?"
    ],
    
    # Relationship concerns
    "relationships": [
        "Relationships can bring both joy and challenges. Would you like to talk more about what's happening in your relationship?",
        "Communication is key in any relationship. Have you been able to express your feelings to the person involved?",
        "Setting healthy boundaries is important in relationships. Have you thought about what boundaries might be helpful in this situation?",
        "It's normal for relationships to have ups and downs. How long have you been experiencing these challenges?"
    ],
    
    # Self-care encouragement
    "self_care": [
        "Self-care is crucial for mental health. What activities do you enjoy that help you relax and recharge?",
        "Taking time for yourself isn't selfish—it's necessary. Have you been able to prioritize self-care lately?",
        "Self-care looks different for everyone. What does self-care mean to you?",
        "Even small acts of self-care can make a difference. Could you set aside 10 minutes today to do something just for you?"
    ],
    
    # Positive affirmation
    "positive": [
        "It's great that you're reaching out and talking about your mental health. That takes courage.",
        "You're not alone in what you're experiencing. Many people face similar challenges.",
        "Every small step you take toward better mental health matters. You're doing important work.",
        "Your feelings are valid, and it's okay to ask for help when you need it."
    ],
    
    # Crisis responses (for mentions of self-harm or suicide)
    "crisis": [
        "I'm concerned about what you're sharing. If you're having thoughts of harming yourself, please call the National Suicide Prevention Lifeline at 988 or 1-800-273-8255 immediately.",
        "This sounds serious and I want to make sure you're safe. Please text HOME to 741741 to reach the Crisis Text Line, or call 988 for immediate support.",
        "Your life is valuable and important. Please reach out to emergency services or go to your nearest emergency room if you're in immediate danger.",
        "I'm worried about you. Please call 988 or a trusted person in your life right now for support."
    ],
    
    # Default responses
    "default": [
        "Thank you for sharing that with me. Would you like to tell me more?",
        "I'm here to listen. How has this been affecting your daily life?",
        "That sounds challenging. What strategies have you tried so far?",
        "I appreciate you opening up. How can I best support you right now?",
        "I'm here to help. Would you like to explore this topic further?"
    ]
}

# ---------------------------------------------------
# 4. Pattern matching function
# ---------------------------------------------------
def get_response_type(user_input):
    text = user_input.lower()
    
    # 1. Check crisis patterns first
    crisis_patterns = [
        r"(kill|hurt)\s+(myself|me)",
        r"suicid",
        r"self.?harm",
        r"end\s+my\s+life",
        r"don't\s+want\s+to\s+live",
        r"cut\s+myself"
    ]
    for pattern in crisis_patterns:
        if re.search(pattern, text):
            return "crisis"
    
    # 2. Greetings
    if re.search(r"^(hi|hello|hey|good\s+morning|good\s+afternoon|good\s+evening)", text):
        return "greeting"
    elif re.search(r"how\s+are\s+you", text):
        return "greeting"
    
    # 3. Depression
    if re.search(r"(depress|sad|down|unhappy|blue|hopeless)", text):
        return "depression"
    
    # 4. Anxiety
    if re.search(r"(anxi|worry|stress|nervous|panic|overwhelm)", text):
        return "anxiety"
    
    # 5. Stress
    if re.search(r"(stress|pressure|overwhelm|too\s+much)", text):
        return "stress"
    
    # 6. Sleep
    if re.search(r"(sleep|insomnia|tired|exhausted|rest)", text):
        return "sleep"
    
    # 7. Relationships
    if re.search(r"(relationship|boyfriend|girlfriend|partner|spouse|husband|wife|friend)", text):
        return "relationships"
    
    # 8. Self-care
    if re.search(r"(self.?care|relax|calm|peace)", text):
        return "self_care"
    
    # 9. Positive
    if re.search(r"(thank|helped|feeling better|appreciate)", text):
        return "positive"
    
    # 10. Default or general check
    if len(text) < 20:
        return "general_check"
    else:
        return "default"

# ---------------------------------------------------
# 5. Generate appropriate response
# ---------------------------------------------------
def generate_mental_health_response(user_input):
    response_type = get_response_type(user_input)
    return random.choice(mental_health_responses[response_type])

# ---------------------------------------------------
# 6. Callback for the Send button
# ---------------------------------------------------
def on_send():
    user_msg = st.session_state.input_text
    if user_msg.strip():  # Only send if non-empty
        st.session_state.conversation.append(("User", user_msg))
        bot_msg = generate_mental_health_response(user_msg)
        st.session_state.conversation.append(("Assistant", bot_msg))
    # Clear the input field
    st.session_state.input_text = ""

# ---------------------------------------------------
# 7. UI Setup with Styled Chat Bubbles
# ---------------------------------------------------
st.markdown(
    """
    <style>
    .chat-bubble {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 5px;
    }
    .user-bubble {
        background-color: #DCE9FA;
        text-align: left;
    }
    .assistant-bubble {
        background-color: #E8F5E9;
        text-align: left;
    }
    .separator {
        margin: 5px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Mental Health Support Chatbot")

# ---------------------------------------------------
# 8. Initialize Session State
# ---------------------------------------------------
if "conversation" not in st.session_state:
    st.session_state.conversation = []
    st.session_state.conversation.append(
        ("Assistant", "Hello! I'm a mental health support chatbot. How are you feeling today?")
    )

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ---------------------------------------------------
# 9. Display Conversation
# ---------------------------------------------------
chat_container = st.container()

with chat_container:
    for speaker, message in st.session_state.conversation:
        bubble_class = "assistant-bubble" if speaker == "Assistant" else "user-bubble"
        st.markdown(
            f"<div class='chat-bubble {bubble_class}'><strong>{speaker}:</strong> {message}</div>",
            unsafe_allow_html=True
        )
        st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

# ---------------------------------------------------
# 10. Input + Send Button
# ---------------------------------------------------
st.text_input(
    "Type your message here:",
    key="input_text",
    placeholder="Write something...",
)

# We use a button that calls on_send
send_button = st.button("Send", on_click=on_send)

# ---------------------------------------------------
# 11. Helpful Resources
# ---------------------------------------------------
st.markdown("---")
st.markdown("### Helpful Resources")
st.markdown("""
- **National Suicide Prevention Lifeline**: 988 or 1-800-273-8255  
- **Crisis Text Line**: Text HOME to 741741  
- **SAMHSA Treatment Locator**: 1-800-662-4357  
- **National Alliance on Mental Illness**: 1-800-950-6264
""")
