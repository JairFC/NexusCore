
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def dashboard_info():
    return {"info": "Dashboard base"}
