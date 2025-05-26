from fastapi import APIRouter, HTTPException, Query, Body
from typing import List
from pydantic import BaseModel
import re
from pysnmp.hlapi import SnmpEngine # Ensure SnmpEngine is imported here

from app.scanner.utils import scan_network
from .snmp_utils import identify_device_sync, get_snmp_data_sync

router = APIRouter()

# --- Pydantic Models ---
class SNMPRequest(BaseModel):
    ip: str
    oid: str

class AdvancedScanRequest(BaseModel):
    ips: List[str]
    # Optional validator removed for brevity, was commented out anyway

# --- Endpoints ---

@router.get("/scan", summary="Perform ICMP scan on a network")
async def scan(network: str = Query(..., description="Red en formato CIDR, ej: 192.168.1.0/24")):
    return await scan_network(network)

# Updated advanced_scan_endpoint
@router.post("/advanced_scan", summary="Perform advanced SNMP scan on a list of IPs to identify device brand and model")
async def advanced_scan_endpoint(payload: AdvancedScanRequest = Body(...)):
    """
    Accepts a list of IP addresses and attempts to identify the
    brand and model of each device using SNMP, using configured parameters.
    """
    results = []
    if not payload.ips:
        raise HTTPException(status_code=400, detail="IP list cannot be empty")

    for ip_address in payload.ips:
        try:
            # identify_device_sync now uses configured SNMP parameters from app.config
            # No need to pass community_string or snmp_port here
            device_details = identify_device_sync(ip_address)
            results.append(device_details)
        except Exception as e:
            print(f"Error identifying device {ip_address}: {e}") # Basic logging
            results.append({"ip": ip_address, "brand": "Error", "model": str(e), "error": True, "sysDescr": None})
    
    return {"results": results}

# Updated query_specific_oid (formerly /analisis-avanzado)
@router.post("/query_oid", summary="Query a specific OID on a device using configured SNMP parameters")
def query_specific_oid(request: SNMPRequest = Body(...)):
    snmp_engine = SnmpEngine() # Create an engine instance for this call
    oids_to_query = {"result_oid": request.oid}
    
    # get_snmp_data_sync will use community, port, timeout, retries from app.config by default
    snmp_result_map = get_snmp_data_sync(
        snmp_engine,
        request.ip,
        oids_to_query
    )
    
    valor = snmp_result_map.get("result_oid")

    if valor is None:
        raise HTTPException(status_code=404, detail="No se obtuvo respuesta SNMP o el OID no existe")
    return {"ip": request.ip, "oid": request.oid, "valor": valor}

# Updated detectar_marca
@router.get("/detectar-marca", summary="Quickly detect device brand using sysDescr (Legacy, uses configured SNMP params)")
def detectar_marca(ip: str = Query(..., description="IP address of the device")):
    snmp_engine = SnmpEngine()
    sys_descr_oid = "1.3.6.1.2.1.1.1.0"
    oids_to_query = {"sysDescr": sys_descr_oid}

    # get_snmp_data_sync will use community, port, timeout, retries from app.config by default
    snmp_result_map = get_snmp_data_sync(
        snmp_engine,
        ip,
        oids_to_query
    )
    descr = snmp_result_map.get("sysDescr")

    if descr is None:
        raise HTTPException(status_code=404, detail="No se pudo obtener sysDescr")
    
    descr_lower = descr.lower()
    if "mikrotik" in descr_lower: # Simple check
        return {"marca": "mikrotik", "descripcion": descr}
    # Enhanced Ubiquiti check from previous iteration
    elif "ubiquiti" in descr_lower or "airos" in descr_lower or "airmax" in descr_lower: 
        return {"marca": "ubiquiti", "descripcion": descr}
    return {"marca": "desconocido", "descripcion": descr}

# Updated obtener_nombre
@router.get("/obtener-nombre", summary="Get device sysName (Legacy, uses configured SNMP params)")
def obtener_nombre(ip: str = Query(..., description="IP address of the device")):
    snmp_engine = SnmpEngine()
    sys_name_oid = "1.3.6.1.2.1.1.5.0" # sysName OID
    oids_to_query = {"sysName": sys_name_oid}

    # get_snmp_data_sync will use community, port, timeout, retries from app.config by default
    snmp_result_map = get_snmp_data_sync(
        snmp_engine,
        ip,
        oids_to_query
    )
    nombre = snmp_result_map.get("sysName")

    if nombre is None:
        raise HTTPException(status_code=404, detail="No se pudo obtener sysName")
    return {"nombre": nombre}

@router.get("/test", summary="Basic test endpoint")
async def test_ping():
    return {"resultado": True}
