from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from forum_scraper import scrape_forum

def create_vector_db():
    texts = scrape_forum()
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts, embedding=embeddings)
    vectorstore.save_local("agnos_vector_db")
    print("FAISS vector store saved to agnos_vector_db/")

if __name__ == "__main__":
    create_vector_db()

