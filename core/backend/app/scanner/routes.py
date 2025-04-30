from fastapi import APIRouter
from app.scanner.utils import realizar_ping

router = APIRouter()

@router.get("/test")
async def test_ping():
    resultado = realizar_ping("8.8.8.8")
    return {"resultado": resultado}
