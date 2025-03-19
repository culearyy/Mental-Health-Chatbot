import streamlit as st
import torch
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration

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
    Loads the tokenizer, retriever, and model for a Retrieval-Augmented Generation approach.
    """
    # Download or load from cache the pretrained RAG model
    tokenizer = RagTokenizer.from_pretrained(
        "facebook/rag-token-nq", 
        trust_remote_code=True
    )
    
    # Configure the retriever with trust_remote_code=True
    retriever = RagRetriever.from_pretrained(
        "facebook/rag-token-nq",
        index_name="exact",
        use_dummy_dataset=True,
        trust_remote_code=True,
        dataset="wiki_dpr",
        dataset_kwargs={"trust_remote_code": True}
    )
    
    model = RagTokenForGeneration.from_pretrained(
        "facebook/rag-token-nq",
        retriever=retriever,
        trust_remote_code=True
    )
    
    return tokenizer, retriever, model

# --- 3. Streamlit UI ---
st.title("Mental Health Chatbot (RAG-based)")

# Initialize session state for conversation history if it doesn't exist
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Load the model (this will use the cached version after the first run)
try:
    tokenizer, retriever, model = load_model()
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
            # Prepare input for the model
            inputs = tokenizer(user_input, return_tensors="pt")
            
            # Generate the output
            outputs = model.generate(
                inputs["input_ids"],
                num_beams=4,
                max_length=100,
                early_stopping=True
            )
            
            # Decode the model's output
            response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
            
            # Add to conversation history
            st.session_state.conversation.append((user_input, response))
            
            # Display the most recent response
            st.markdown(f"**You:** {user_input}")
            st.markdown(f"**Chatbot:** {response}")
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")