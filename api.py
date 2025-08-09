from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import load_rag_chatbot

app = FastAPI()
rag = load_rag_chatbot()

class Query(BaseModel):
    question: str

@app.post("/chat")
def chat(query: Query):
    answer = rag.run(query.question)
    return {"answer": answer}