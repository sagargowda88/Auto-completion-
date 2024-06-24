import streamlit as st
from sentence_transformers import SentenceTransformer, util
import torch

# Load a pre-trained Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

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
column_embeddings = model.encode(list(schema.values()), convert_to_tensor=True)

@st.cache_data
def get_column_suggestions(user_input, top_k=5):
    input_embedding = model.encode(user_input, convert_to_tensor=True)
    cos_scores = util.cos_sim(input_embedding, column_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)
    return [list(schema.keys())[i] for i in top_results.indices]

st.title("SQL Query Builder with Auto-Completion")

# Use a container to hold the input and suggestions
input_container = st.container()

with input_container:
    user_input = st.text_input("Start typing your SQL query:", key="user_input")
    
    if user_input:
        suggestions = get_column_suggestions(user_input)
        selected_suggestion = st.selectbox("Suggested columns:", [""] + suggestions, key="suggestion_box")
        
        if selected_suggestion:
            # Insert the selected suggestion at the cursor position
            cursor_pos = len(user_input)
            new_input = user_input[:cursor_pos] + selected_suggestion + " " + user_input[cursor_pos:]
            st.session_state.user_input = new_input

# JavaScript for better auto-completion experience
st.markdown("""
<script>
const inputElement = window.parent.document.querySelector('input[aria-label="Start typing your SQL query:"]');
const selectElement = window.parent.document.querySelector('select[aria-label="Suggested columns:"]');

inputElement.addEventListener('input', function() {
    // Trigger Streamlit rerun on input
    setTimeout(() => {
        const selectBox = window.parent.document.querySelector('select[aria-label="Suggested columns:"]');
        if (selectBox) {
            selectBox.size = 5;  // Show 5 options at a time
            selectBox.style.position = 'absolute';
            selectBox.style.zIndex = 1000;
        }
    }, 100);
});

selectElement.addEventListener('change', function() {
    // Insert selected value and reset select
    const selectedValue = this.value;
    if (selectedValue) {
        const cursorPosition = inputElement.selectionStart;
        inputElement.value = inputElement.value.slice(0, cursorPosition) + selectedValue + ' ' + inputElement.value.slice(cursorPosition);
        inputElement.focus();
        inputElement.setSelectionRange(cursorPosition + selectedValue.length + 1, cursorPosition + selectedValue.length + 1);
        this.value = '';
    }
});

</script>
""", unsafe_allow_html=True)

if st.button("Generate SQL Query"):
    # Here you would typically process the query, perhaps generating SQL
    # For demonstration, we'll just display the input
    st.write("Generated SQL Query:", user_input)
