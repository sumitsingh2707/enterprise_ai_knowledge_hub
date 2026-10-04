from langchain_openai import OpenAIEmbeddings

from app.core.config import settings


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=settings.openai_api_key,
)