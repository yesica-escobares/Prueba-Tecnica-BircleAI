from llama_index.llms.google_genai import GoogleGenAI
from app.config.settings import settings


def get_llm(streaming: bool = False):
    return GoogleGenAI(
        model=settings.GEMINI_LLM_MODEL,
        api_key=settings.GEMINI_API_KEY,
        temperature=0.0,
        streaming=streaming,
    )
