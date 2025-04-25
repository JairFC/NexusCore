
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

STATIC_USER = {
    "username": "admin",
    "password": "admin123"
}

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    if data.username == STATIC_USER["username"] and data.password == STATIC_USER["password"]:
        return {"message": "Login exitoso", "token": "fake-jwt-token"}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")
