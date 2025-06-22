# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import auth
from .database import create_tables

app = FastAPI(title="RAG Chat API", 
              description="Backend API for RAG-based chat application",
              version="1.0.0")

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

@app.get("/")
def read_root():
    return {"message": f"RAG Chat API is running!",
            "docs": "/docs"
            }

@app.get("/health")
def health_check():
    return {"status": "healthy"}