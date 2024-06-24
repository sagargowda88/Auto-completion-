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

# Initialize session state
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'suggestion' not in st.session_state:
    st.session_state.suggestion = ""

# Function to update query and suggestion
def update_query_and_suggestion():
    current_word = st.session_state.query.split()[-1] if st.session_state.query else ""
    suggestions = get_suggestions(current_word)
    if suggestions:
        st.session_state.suggestion = suggestions[0][len(current_word):]
    else:
        st.session_state.suggestion = ""

# Create a text input for the query
query = st.text_input("Type your SQL query:", 
                      value=st.session_state.query, 
                      key="query_input",
                      on_change=update_query_and_suggestion)

# Update session state
st.session_state.query = query

# Display the current query with suggestion
col1, col2 = st.columns([10, 1])
with col1:
    st.text_input("Current Query with Suggestion:", 
                  value=st.session_state.query + st.session_state.suggestion, 
                  key="display_query", 
                  disabled=True)
with col2:
    if st.button("Use") and st.session_state.suggestion:
        st.session_state.query += st.session_state.suggestion + " "
        st.experimental_rerun()

# Display the finalized query
st.text("Finalized Query:")
st.code(st.session_state.query)
