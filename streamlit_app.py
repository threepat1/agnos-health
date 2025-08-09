import streamlit as st
from chatbot import load_rag_chatbot

st.title("Agnos Health Forum Chatbot")

chatbot = load_rag_chatbot()

question = st.text_input("Ask a health question")

if st.button("Ask"):
    if question.strip():
        try:
            response = chatbot.run(question)
            st.write(response if response else "No answer found.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")