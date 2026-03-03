import streamlit as st
from config import PDF_PATH, GROQ_MODEL
from processor import get_book_chunks
from engene import find_best_answer

# 1. PAGE CONFIG & THEME
st.set_page_config(page_title="Bangtan FAQ AI", page_icon="💜", layout="centered")

# Custom CSS for Icons and Purple Theme
st.markdown("""
    <style>
    .stApp { background-color: #f5f0ff; }
    /* Chat Bubble Styling */
    .stChatMessage { border-radius: 15px; border: 1px solid #d1b3ff; }
    [data-testid="stChatMessage"]:nth-child(even) { background-color: #ede2ff; }
    
    /* Custom Icons via CSS if needed, but Streamlit 'avatar' parameter is easier */
    </style>
    """, unsafe_allow_html=True)

st.title("💜 Bangtan FAQ AI")

# 2. DATA LOADING
@st.cache_resource
def load_data():
    return get_book_chunks(PDF_PATH)

chunks = load_data()

# 3. SIDEBAR WITH ALL ALBUMS
with st.sidebar:
    st.header("💜 Discography")

    # Complete list from your ocr_cache.txt
    album_list = [
        "Select...", "2 Cool 4 Skool", "O!RUL8,2?", "Skool Luv Affair",
        "Dark&Wild", "The Most Beautiful Moment in Life Pt.1",
        "The Most Beautiful Moment in Life Pt.2", "Young Forever",
        "Wings", "You Never Walk Alone", "Love Yourself 'Her'",
        "Love Yourself 'Tear'", "Love Yourself 'Answer'",
        "Map of the Soul: Persona", "Map of the Soul: 7",
        "Dynamite", "BE", "Butter", "Proof"
    ]

    selected_album = st.selectbox("Quick Tracklist:", album_list)

    if selected_album != "Select...":
        st.session_state.queued_query = f"give me the track list of {selected_album}"

    st.write("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 4. CHAT LOGIC
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history with custom icons
# Use a link to a small image or an emoji for the avatar
for message in st.session_state.messages:
    avatar = "Assets/army-bts-logo-transparent.png" if message["role"] == "user" else "Assets/new-logo-bts-logo.png"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 5. HANDLING INPUT
user_input = st.chat_input("Ask about the BTS biography...")
# Check if a sidebar selection happened
if st.session_state.get("queued_query"):
    current_query = st.session_state.queued_query
    st.session_state.queued_query = None # Clear it
elif user_input:
    current_query = user_input
else:
    current_query = None

if current_query:
    st.session_state.messages.append({"role": "user", "content": current_query})
    with st.chat_message("user", avatar="Assets/army-bts-logo-transparent.png"):
        st.markdown(current_query)


    with st.spinner("Consulting the book..."):
        # find_best_answer uses the album_map to find the right PAGE header
        answer, _ = find_best_answer(current_query, chunks, st.session_state.messages)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant", avatar="Assets/new-logo-bts-logo.png"):
            st.markdown(answer)