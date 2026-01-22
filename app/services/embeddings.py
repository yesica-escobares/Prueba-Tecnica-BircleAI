from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from app.config.settings import settings


def get_embedding_model():
    return GoogleGenAIEmbedding(
        model_name=settings.GEMINI_EMBEDDING_MODEL,
        api_key=settings.GEMINI_API_KEY,
    )
