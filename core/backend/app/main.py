from fastapi import FastAPI

from app.auth.routes import router as auth_router
from app.dashboard.routes import router as dashboard_router
from app.test.routes import router as test_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
app.include_router(test_router, tags=["test"])

@app.get("/")
def root():
    return {"status": "NexusCore API operativa"}
