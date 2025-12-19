from fastapi import FastAPI
from config.database import get_db
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(availableVehicle)
@app.get("/")
def root():
    return {
        "the server is running"
    }

