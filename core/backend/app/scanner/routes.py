from fastapi import APIRouter, Query
from app.scanner.utils import scan_network

router = APIRouter()

@router.get("/test")
async def test_ping():
    return {"resultado": True}

@router.get("/scan")
async def scan(network: str = Query(..., description="Red en formato CIDR, ej: 192.168.1.0/24")):
    return await scan_network(network)
