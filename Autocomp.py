 import streamlit as st
from sentence_transformers import SentenceTransformer, util
import torch
import time

# Load a pre-trained Sentence Transformer model
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# Schema with column names and descriptions
schema = {
    'user_id': 'Unique identifier for each user',
    'username': 'Name chosen by the user for their account',
    'email': 'Email address of the user',
    'age': 'Age of the user in years',
    'location': 'Geographic location of the user',
    'signup_date': 'Date when the user created their account'
}

# Precompute embeddings for schema items
@st.cache_data
def get_column_embeddings():
    return model.encode(list(schema.values()), convert_to_tensor=True)

column_embeddings = get_column_embeddings()

@st.cache_data
def get_column_suggestions(user_input, top_k=5):
    input_embedding = model.encode(user_input, convert_to_tensor=True)
    cos_scores = util.cos_sim(input_embedding, column_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)
    return [list(schema.keys())[i] for i in top_results.indices]

st.title("Real-time SQL Query Auto-Completion")

# Initialize session state
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = []

# Create a text input for the query
query_input = st.empty()

# Create a space for suggestions
suggestion_space = st.empty()

while True:
    # Update the query input
    current_query = query_input.text_input("Type your SQL query:", value=st.session_state.query)
    
    # If the query has changed, update suggestions
    if current_query != st.session_state.query:
        st.session_state.query = current_query
        if current_query:
            st.session_state.suggestions = get_column_suggestions(current_query)
        else:
            st.session_state.suggestions = []
    
    # Display suggestions
    if st.session_state.suggestions:
        suggestion_text = "Suggestions: " + ", ".join(st.session_state.suggestions)
        suggestion_space.text(suggestion_text)
    else:
        suggestion_space.empty()
    
    # Short sleep to prevent excessive updating
    time.sleep(0.1)

    # Rerun the app
    st.experimental_rerun()
