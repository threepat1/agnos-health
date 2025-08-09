from langchain.llms import Ollama
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
import os

if not os.path.exists("agnos_vector_db/index.faiss"):
    raise FileNotFoundError("FAISS index not found. Run vector_store.py to create it first.")

def load_rag_chatbot():
    # Load vector DB
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local("agnos_vector_db", embeddings, allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Choose an LLM — using Ollama here for example
    llm = Ollama(model="llama3")  # or "llama2", "mistral", etc.

    # Create a RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )
    return qa_chain