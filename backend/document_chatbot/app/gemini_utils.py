import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from config import settings
# Load API key
load_dotenv()
#os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Embedding model (768-dim vectors)
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=settings.GEMINI_API_KEY)

# Chat model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # or "gemini-pro"
    temperature=0.3,google_api_key=settings.GEMINI_API_KEY
    )

