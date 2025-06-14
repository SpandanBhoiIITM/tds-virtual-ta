from fastapi import FastAPI
from pydantic import BaseModel
from deepseek_client import call_deepseek
from rag_utils import get_top_k_relevant_context
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryInput(BaseModel):
    question: str

@app.api_route("/", methods=["GET", "POST"])
def root():
    return {"message": "TDS Virtual TA backend is running."}

@app.post("/ask")
async def ask_qn(input: QueryInput):
    relevant_context = get_top_k_relevant_context(input.question)
    prompt = f"Context:\n{relevant_context}\n\nQuestion: {input.question}\nAnswer:"
    answer = call_deepseek(prompt)
    return {"answer": answer}
