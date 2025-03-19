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
    tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq", trust_remote_code=True) # Added trust_remote_code=True here
    
    # Note: For testing, 'use_dummy_dataset=True' loads a dummy index.
    # For a real application, you'd configure a real knowledge dataset/index.
    retriever = RagRetriever.from_pretrained(
        "facebook/rag-token-nq",
        index_name="exact",
        use_dummy_dataset=True,
        trust_remote_code=True, # Ensure this is True to allow custom code
        dataset_kwargs={"trust_remote_code": True},  # Also include in dataset_kwargs for extra measure
    )
    
    model = RagTokenForGeneration.from_pretrained(
        "facebook/rag-token-nq",
        retriever=retriever,
        trust_remote_code=True # Added trust_remote_code=True here
    )
    
    return tokenizer, retriever, model

# Load the model outside the main code flow so it's only loaded once
tokenizer, retriever, model = load_model()

# --- 3. Streamlit UI ---
st.title("Mental Health Chatbot (RAG-based)")

user_input = st.text_input("You:", placeholder="How are you feeling today?")

if user_input:
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
    
    # Display the response
    st.write("Chatbot:", response)