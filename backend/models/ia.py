import os
from google import genai #type:ignore
from dotenv import load_dotenv #type: ignore

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))