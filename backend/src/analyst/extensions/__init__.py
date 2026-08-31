"""
Extensions — cross-cutting concerns wired into the FastAPI app.

Things that apply to ALL requests: error handling, rate limiting,
logging middleware, CORS. Configured once in app.py, used everywhere.
"""
