from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
import os
import torch

if not os.path.exists("agnos_vector_db/index.faiss"):
    raise FileNotFoundError("FAISS index not found. Run vector_store.py to create it first.")

def load_rag_chatbot():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": device}
    )
    vectorstore = FAISS.load_local("agnos_vector_db", embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # Choose an LLM — using Ollama here for example
    llm = ChatOllama(model="llama3")  # or "llama2", "mistral", etc.

    # Create a prompt template
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

    # Create a stuff documents chain
    document_chain = create_stuff_documents_chain(llm, prompt)

    # Create the retrieval chain
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    return retrieval_chain