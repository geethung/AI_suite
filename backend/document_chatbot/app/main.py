from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from .services import build_vector_index, answer_question, extract_text_from_file  # 👈 Add extract_text_from_file
import io
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 👈 allow your React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



vector_store = None

class QueryInput(BaseModel):
    query: str

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    global vector_store

    # Read and extract text from the file
    contents = await file.read()
    text = extract_text_from_file(file.filename, contents)
    
    chunks = [text]  # You can split text into multiple chunks if needed
    vector_store = build_vector_index(chunks)
    return {"message": f"✅ File '{file.filename}' uploaded and indexed."}

@app.post("/ask")
def ask_question(data: QueryInput):
    if vector_store is None:
        return {"error": "❌ Vector index not built yet. Upload a file first."}
    
    answer = answer_question(vector_store, data.query)
    return {"answer": answer}
