from fastapi import FastAPI
from document_chatbot.app.main import app as document_chatbot_app
from HR_bot.backend.main import app as hr_bot_app
from meeting_summary_tool.backend.main import app as meeting_summary_app
from sop_generator.app.main import app as sop_generator_app
from fastapi.middleware.cors import CORSMiddleware


main_app = FastAPI()
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount each sub-app under a different path
main_app.mount("/document-chatbot", document_chatbot_app)
main_app.mount("/hr-bot", hr_bot_app)
main_app.mount("/meeting-summary", meeting_summary_app)
main_app.mount("/sop-generator", sop_generator_app)

# Optionally, add a root endpoint
@main_app.get("/")
def read_root():
    return {"message": "Welcome to the AI Suite API Gateway"}
