# app.py
import streamlit as st
from config import PDF_PATH
from processor import get_book_chunks
from engene import find_best_answer # Renamed for clarity

st.set_page_config(page_title="Bangtan FAQ AI", page_icon="💜")
st.title("💜 Bangtan FAQ AI (Smart Version)")

# app.py sidebar
with st.sidebar:
    st.header("Settings")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    st.write("---")
    st.write("Model: Llama 3.3 (via Groq)")

@st.cache_resource
def load_data():
    # Show progress so you know it's not crashed
    with st.status("Extracting book content (this may take a minute)..."):
        return get_book_chunks(PDF_PATH)

chunks = load_data()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me about the book..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        # We now return TWO things: the smart answer and the raw source
        # Pass the full chat history (st.session_state.messages) to the engine
        smart_answer, source_text = find_best_answer(prompt, chunks, st.session_state.messages)
    with st.chat_message("assistant"):
        st.markdown(smart_answer)
        # Professional touch: show the source in an accordion
        with st.expander("View source context from the book"):
            st.info(source_text)

    st.session_state.messages.append({"role": "assistant", "content": smart_answer})