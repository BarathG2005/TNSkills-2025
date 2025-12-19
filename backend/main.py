from fastapi import FastAPI
from config.database import get_db
app = FastAPI()


   


@app.get("/")
def root():
    return {
        "the server is running"
    }