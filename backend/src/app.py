from .analyst.routers import documents
from .auth.route.routes import router as auth_router
from fastapi import FastAPI


app = FastAPI(
    title="SuperDocs Analyst API",
    description="Backend API for document ingestion and parsing",
    version="0.1.0"
)

app.include_router(auth_router)
app.include_router(documents.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}


