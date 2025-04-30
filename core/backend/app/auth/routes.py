from fastapi import APIRouter, HTTPException
from app.auth.schemas import UserLogin
from app.common.database import connect_to_db
import bcrypt  # ✅ Asegúrate de tenerlo instalado y disponible en Docker

router = APIRouter()

@router.post("/login")
async def login(user: UserLogin):
    conn = await connect_to_db()
    try:
        result = await conn.fetchrow(
            "SELECT * FROM users WHERE username = $1",
            user.username
        )
        if not result:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        # ✅ Verificación de contraseña con bcrypt
        if not bcrypt.checkpw(user.password.encode(), result["password_hash"].encode()):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        return {"message": "Login exitoso", "username": user.username}

    finally:
        await conn.close()
