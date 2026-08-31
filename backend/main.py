import uvicorn


# Main.py will seperate app.py concern and will not start server on tests.
# This is main file which will start server if `uvicorn main:app` is used.

if __name__ == "__main__":
    uvicorn.run("src.analyst.app:app", host="0.0.0.0",port=8000,reload=True)