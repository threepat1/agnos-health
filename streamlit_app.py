import streamlit as st
from chatbot import load_rag_chatbot

st.title("Agnos Health Forum Chatbot")

chatbot = load_rag_chatbot()

question = st.text_input("Ask a health question")

if st.button("Ask"):
    if question.strip():
        with st.spinner("Thinking..."):
            try:
                response = chatbot.invoke({"input": question})
                st.write(response.get("answer", "No answer found."))
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")