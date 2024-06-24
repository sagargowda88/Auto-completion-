import streamlit as st
from sentence_transformers import SentenceTransformer, util
import torch

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

st.title("SQL Query Builder with Auto-Completion")

# Initialize session state for the query input
if 'query_input' not in st.session_state:
    st.session_state.query_input = ""

# Function to update query input
def update_query_input():
    if st.session_state.suggestion != "":
        current_position = len(st.session_state.query_input)
        st.session_state.query_input = (
            st.session_state.query_input[:current_position] + 
            st.session_state.suggestion + " " + 
            st.session_state.query_input[current_position:]
        )
    st.session_state.suggestion = ""

# Text input for the query
query_input = st.text_input("Start typing your SQL query:", 
                            key="query_input", 
                            value=st.session_state.query_input)

# Get suggestions based on the current input
if query_input:
    suggestions = get_column_suggestions(query_input)
    
    # Dropdown for suggestions
    st.selectbox("Suggested columns:", 
                 [""] + suggestions, 
                 key="suggestion", 
                 on_change=update_query_input)

if st.button("Generate SQL Query"):
    # Here you would typically process the query, perhaps generating SQL
    # For demonstration, we'll just display the input
    st.write("Generated SQL Query:", st.session_state.query_input)
