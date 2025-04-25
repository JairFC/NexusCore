from fastapi import APIRouter
from app.common.database import connect_to_db

router = APIRouter()

@router.get("/test-db")
async def test_db_connection():
    try:
        await connect_to_db()
        return {"status": " Conexión exitosa a PostgreSQL"}
    except Exception as e:
        return {"status": " Error de conexión", "detail": str(e)}
