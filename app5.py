import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# --- 1. Streamlit Disclaimer (optional but recommended) ---
st.sidebar.markdown(
    "**Disclaimer:** This chatbot is for informational purposes only "
    "and is not a substitute for professional mental health advice. "
    "If you are in crisis, please contact your local emergency services immediately."
)

# --- 2. Cache the Model Loading ---
@st.cache_resource
def load_model():
    """
    Loads a simpler transformer model for text generation.
    """
    try:
        # Load a smaller and easier to use model (DialoGPT)
        model_name = "microsoft/DialoGPT-medium"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        raise e

# --- 3. Function to generate responses ---
def generate_response(input_text, chat_history_ids=None):
    # Encode the input text
    input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors="pt")
    
    # If we have chat history, append it
    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1)
    else:
        bot_input_ids = input_ids
    
    # Generate a response
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7
    )
    
    # Decode the response
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    return response, chat_history_ids

# --- 4. Streamlit UI ---
st.title("Mental Health Chatbot")

# Initialize session state for conversation history if it doesn't exist
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

if 'chat_history_ids' not in st.session_state:
    st.session_state.chat_history_ids = None

# Load the model (this will use the cached version after the first run)
try:
    tokenizer, model = load_model()
    model_loaded = True
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    model_loaded = False

# Display conversation history
for i, (user_msg, bot_msg) in enumerate(st.session_state.conversation):
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**Chatbot:** {bot_msg}")
    st.markdown("---")

# User input
user_input = st.text_input("You:", placeholder="How are you feeling today?")

if user_input and model_loaded:
    # Add a loading indicator
    with st.spinner("Thinking..."):
        try:
            # Generate response
            response, st.session_state.chat_history_ids = generate_response(
                user_input, 
                st.session_state.chat_history_ids
            )
            
            # Add to conversation history
            st.session_state.conversation.append((user_input, response))
            
            # Display the most recent response
            st.markdown(f"**You:** {user_input}")
            st.markdown(f"**Chatbot:** {response}")
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")