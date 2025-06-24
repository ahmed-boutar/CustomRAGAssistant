# app/main.py
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, inference, upload, sessions
from .database import create_tables

app = FastAPI(title="RAG Chat API", 
              description="Backend API for RAG-based chat application",
              version="1.0.0")

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception(f"Unhandled error: {e}")
        raise

# Create tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(inference.router)
app.include_router(upload.router)
app.include_router(sessions.router)


@app.get("/")
def read_root():
    return {"message": f"RAG Chat API is running!",
            "docs": "/docs"
            }

@app.get("/health")
def health_check():
    return {"status": "healthy"}