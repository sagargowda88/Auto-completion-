import streamlit as st

# Schema with column names
schema = [
    'user_id', 'username', 'email', 'age', 'location', 'signup_date',
    'last_login', 'account_status', 'profile_picture', 'bio',
    'friends_count', 'posts_count', 'likes_received', 'comments_made',
    'total_time_spent', 'preferred_language', 'notification_settings'
]

def get_suggestions(prefix):
    return [col for col in schema if col.startswith(prefix.lower())]

st.title("Real-time SQL Query Auto-Completion")

# Initialize session state for query and cursor position
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'cursor_pos' not in st.session_state:
    st.session_state.cursor_pos = 0

def on_change():
    # Get the current word being typed
    current_word = st.session_state.query[:st.session_state.cursor_pos].split()[-1] if st.session_state.query else ""
    
    # Get suggestions for the current word
    suggestions = get_suggestions(current_word)
    
    # Update suggestions in session state
    st.session_state.suggestions = suggestions

# Create a text input for the query
query = st.text_input("Type your SQL query:", 
                      value=st.session_state.query, 
                      key="query_input",
                      on_change=on_change)

# Update cursor position
st.session_state.cursor_pos = len(query)

# Display suggestions
if 'suggestions' in st.session_state and st.session_state.suggestions:
    selected_suggestion = st.selectbox("Suggestions:", st.session_state.suggestions)
    if st.button("Use Suggestion"):
        # Replace the current word with the selected suggestion
        words = st.session_state.query.split()
        if words:
            words[-1] = selected_suggestion
        else:
            words = [selected_suggestion]
        st.session_state.query = " ".join(words) + " "
        st.experimental_rerun()

# Display the current query
st.text("Current Query:")
st.code(st.session_state.query)
