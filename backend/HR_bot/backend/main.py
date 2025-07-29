from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from .rag import build_all_vectorstores, get_answer

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(query: str = Form(...)):
    print("Received query:", query)
    answer = get_answer(query)
    return {"answer": answer}

@app.on_event("startup")
def startup_event():
    print("📄 Indexing documents...")
    build_all_vectorstores()
    print("✅ All documents indexed.")