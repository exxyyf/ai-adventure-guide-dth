from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from src.rag_pipeline import TravelRAG
import base64

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


@app.post("/answer-image", response_model=AnswerResponse)
async def answer_image(file: UploadFile = File(...)):
    contents = await file.read()
    # Конвертируем в base64
    pic_b64 = base64.b64encode(contents).decode("utf-8")
    answer = rag.answer_image(pic_b64)

    return {"answer": answer}