import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from .utils import pdf_to_text
from dotenv import load_dotenv

load_dotenv()

embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

vectorstore_path =  os.path.join(os.path.dirname(__file__), "vectorstore")
doc_folder =  os.path.join(os.path.dirname(__file__), "documents")
os.makedirs(vectorstore_path, exist_ok=True)
print("Vectorstore path:", vectorstore_path)
prompt_template = """
You are an AI assistant for a company. Use the following extracted context from HR and policy documents to answer the employee's question accurately, concisely, and politely.

Context:
{context}

Question:
{question}

Answer in a professional tone:
"""

QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template,
)

def build_vectorstore(text, filename):
    doc = Document(page_content=text, metadata={"source": filename})
    vs = FAISS.from_documents([doc], embedding)
    base_name = os.path.splitext(filename)[0]
    vs.save_local(os.path.join(vectorstore_path, base_name))
    #vs.save_local(os.path.join(vectorstore_path, filename.replace(".pdf", "")))

def build_all_vectorstores():
    for filename in os.listdir(doc_folder):
        if filename.endswith(".pdf"):
            path = os.path.join(doc_folder, filename)
            text = pdf_to_text(path)
            build_vectorstore(text, filename)

def load_vectorstore():
    stores = []
    print("dir", os.listdir(vectorstore_path))
    for dir_name in os.listdir(vectorstore_path):
        store_path = os.path.join(vectorstore_path, dir_name)
        print("Loading vectorstore from:", store_path)
        if os.path.isdir(store_path) and "index.faiss" in os.listdir(store_path):
            store = FAISS.load_local(store_path, embedding, allow_dangerous_deserialization=True)
            stores.append(store)
            print("✅ Loaded:", store_path)
        else:
            print("❌ Skipped:", store_path)
    return stores

def get_answer(query: str):
    print("Query:", query)
    stores = load_vectorstore()
    print("stores",stores)
    if not stores:
        return "No documents are indexed. Please check the /documents folder."
    merged = stores[0]
    for s in stores[1:]:
        merged.merge_from(s)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=merged.as_retriever(),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    return qa.run(query)