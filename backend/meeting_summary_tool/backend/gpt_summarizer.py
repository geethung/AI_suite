import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

prompt_template = PromptTemplate.from_template("""
You are an AI assistant. Please analyze the following meeting transcript and provide:

1. A brief summary of the meeting
2. Key decisions made
3. Action items with assigned persons and deadlines

Transcript:
{transcript}
""")

chain = prompt_template | llm | StrOutputParser()

def summarize_transcript(transcript):
    return chain.invoke({"transcript": transcript})