from fastapi import FastAPI
from .routers import documents

app = FastAPI(
    title="SuperDocs Analyst API",
    description="Backend API for document ingestion and parsing",
    version="0.1.0"
)

app.include_router(documents.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
