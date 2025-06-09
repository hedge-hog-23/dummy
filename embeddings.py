import google.generativeai as genai
import os
from dotenv import load_dotenv

# environment variables from .env file
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_embedding(text):
    """Get embedding from Google's Gemini model"""
    try:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return result["embedding"]
    except Exception as e:
        raise Exception(f"Failed to get embedding: {e}")