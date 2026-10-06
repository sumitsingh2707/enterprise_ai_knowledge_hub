from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.user import router as user_router
from app.api.documents import router as documents_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.search import router as search_router
from app.api.chat import router as chat_router
from contextlib import asynccontextmanager

from app.graph.checkpointer import checkpointer_manager
from app.graph.workflow import create_workflow
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Enterprise AI Copilot...")
    checkpointer = checkpointer_manager.startup()
    app.state.rag_graph = create_workflow(checkpointer)
    print("PostgreSQL checkpointer initialized.")
    try:
        yield
    finally:
        print("Shutting down Enterprise AI Copilot...")
        checkpointer_manager.shutdown()
        print("PostgreSQL checkpointer closed.")

app = FastAPI(
    title="Enterprise AI Copilot",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
