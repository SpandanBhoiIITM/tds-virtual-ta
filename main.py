from fastapi import FastAPI
from pydantic import BaseModel
from deepseek_client import call_deepseek
from rag_utils import get_top_k_relevant_context

app = FastAPI()

class QueryInput(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "TDS Virtual TA backend is running."}

@app.post("/ask")
async def ask_qn(input: QueryInput):
    relevant_context = get_top_k_relevant_context(input.question)
    prompt = f"Context:\n{relevant_context}\n\nQuestion: {input.question}\nAnswer:"
    answer = call_deepseek(prompt)
    return {"answer": answer}
