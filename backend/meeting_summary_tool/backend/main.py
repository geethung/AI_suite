from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .whisper_transcriber import transcribe_audio
from .gpt_summarizer import summarize_transcript
from .notion_sender import create_notion_task
import re


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    with open("temp.mp3", "wb") as buffer:
        buffer.write(await file.read())

    transcript = transcribe_audio("temp.mp3")
    summary = summarize_transcript(transcript)

    return {
        "transcript": transcript,
        "summary": summary
    }