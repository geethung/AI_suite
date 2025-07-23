from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .config import settings
from .generate_pdf_sop import router as pdf_router
import uvicorn
import logging

logging.basicConfig(level=logging.DEBUG)
app = FastAPI(
    title=settings.app_title,
    description=settings.app_description
)

# ✅ CORS middleware to allow React requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(pdf_router)

@app.get("/")
def root():
    return {"message": "Welcome to the SOP Generator API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
