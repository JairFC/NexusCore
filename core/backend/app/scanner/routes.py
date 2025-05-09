from fastapi import APIRouter, HTTPException, Query, Body
from app.scanner.utils import scan_network
from app.scanner.snmp_utils import consultar_oid
from pydantic import BaseModel

router = APIRouter()

# Models para solicitudes
class SNMPRequest(BaseModel):
    ip: str
    oid: str

# Endpoint principal para escaneo ICMP (Etapa 1)
@router.get("/scan")
async def scan(network: str = Query(..., description="Red en formato CIDR, ej: 192.168.1.0/24")):
    return await scan_network(network)

# Endpoint SNMP general para probar cualquier OID (Etapa 2 básica)
@router.post("/analisis-avanzado")
def analizar_snmp(request: SNMPRequest = Body(...)):
    valor = consultar_oid(request.ip, request.oid)
    if valor is None:
        raise HTTPException(status_code=404, detail="No se obtuvo respuesta SNMP")
    return {"valor": valor}

# Endpoint para detectar la marca (ubiquiti/mikrotik/desconocido) usando sysDescr.0
@router.get("/detectar-marca")
def detectar_marca(ip: str):
    descr = consultar_oid(ip, "1.3.6.1.2.1.1.1.0")  # sysDescr
    if descr is None:
        raise HTTPException(status_code=404, detail="No se pudo obtener sysDescr")
    if "mikrotik" in descr.lower():
        return {"marca": "mikrotik", "descripcion": descr}
    elif "ubiquiti" in descr.lower() or "air" in descr.lower():
        return {"marca": "ubiquiti", "descripcion": descr}
    return {"marca": "desconocido", "descripcion": descr}

# Endpoint para obtener el nombre del dispositivo (sysName)
@router.get("/obtener-nombre")
def obtener_nombre(ip: str):
    nombre = consultar_oid(ip, "1.3.6.1.2.1.1.5.0")  # sysName
    if nombre is None:
        raise HTTPException(status_code=404, detail="No se pudo obtener sysName")
    return {"nombre": nombre}

# Test básico
@router.get("/test")
async def test_ping():
    return {"resultado": True}
