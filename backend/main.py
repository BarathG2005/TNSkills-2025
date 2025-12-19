from fastapi import FastAPI
from config.database import get_db
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.all_middleware
@app.get("/")
def root():
    return {
        "the server is running"
    }