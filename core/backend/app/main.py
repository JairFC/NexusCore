from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.scanner.routes import router as scanner_router
import os

# Cargar variables de entorno
load_dotenv()

app = FastAPI()

# Configurar CORS
origins = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "").split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from app.auth.routes import router as auth_router
from app.dashboard.routes import router as dashboard_router
from app.test.routes import router as test_router

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
app.include_router(test_router, tags=["test"])
app.include_router(scanner_router, prefix="/scanner", tags=["scanner"])


@app.get("/")
def root():
    return {"status": "NexusCore API operativa"}
