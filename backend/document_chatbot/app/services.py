import os
import io
from PyPDF2 import PdfReader
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from .gemini_utils import embedding_model, llm

# ✅ Build FAISS index from text chunks
def build_vector_index(chunks: list[str]):
    docs = [Document(page_content=chunk) for chunk in chunks]
    vector_store = FAISS.from_documents(docs, embedding_model)
    return vector_store

# ✅ Retrieve top-k similar chunks
def search_similar_chunks(vector_store, query: str, k: int = 4):
    return vector_store.similarity_search(query, k=k)

# ✅ Answer question using RAG
def answer_question(vector_store, query: str) -> str:
    docs = search_similar_chunks(vector_store, query)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""You are a helpful assistant answering questions about internal company documents.

Context:
{context}

Question:
{query}

Only answer using the context above. Do not make up facts."""

    try:
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ✅ Extract text from uploaded file (PDF or text)
def extract_text_from_file(filename: str, content: bytes) -> str:
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        reader = PdfReader(io.BytesIO(content))
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return text

    elif ext in [".txt", ".md"]:
        return content.decode("utf-8")

    else:
        raise ValueError("❌ Unsupported file format. Only .pdf, .txt, and .md are supported.")
