from fastapi import FastAPI
from pydantic import BaseModel
from src.rag_pipeline import TravelRAG

app = FastAPI(title="Travel RAG API")

rag = TravelRAG()  # инициализируется один раз


class QuestionRequest(BaseModel):
    text: str


class AnswerResponse(BaseModel):
    answer: str


@app.post("/answer", response_model=AnswerResponse)
def answer_question(req: QuestionRequest):
    answer = rag.answer(req.text)
    return {"answer": answer}
