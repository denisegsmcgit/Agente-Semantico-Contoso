from fastapi import FastAPI
from pydantic import BaseModel
from agente import agente_rag_semantico

app = FastAPI(title="Agente RAG Semântico")


class Pergunta(BaseModel):
    question: str


@app.post("/rag")
def rag_endpoint(data: Pergunta):
    resposta = agente_rag_semantico(data.question)
    return {"answer": resposta}
