from fastapi import FastAPI,APIRouter

router = APIRouter()
@router.get("/available")
def list_veh():
    return {"available veh"}