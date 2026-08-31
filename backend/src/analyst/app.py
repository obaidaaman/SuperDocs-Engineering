"""
FastAPI application factory.

Creates the app with middleware (CORS, rate limiting),
registers all routers, and sets up lifespan (DB pool startup/shutdown).
"""

from fastapi import FastAPI
from .routers import auth,collections
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print("Starting Analyst API")


    yield

 
    print("Shutting down Analyst API")





def create_app() -> FastAPI:

    app = FastAPI(debug=True,title="Super Docs Engineering File", lifespan=lifespan)



    app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


    return app



app = create_app()




