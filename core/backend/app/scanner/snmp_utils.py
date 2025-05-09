from pysnmp.hlapi import *

def consultar_oid(ip, oid, community='public', timeout=1, retries=1):
    try:
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(community, mpModel=0),
            UdpTransportTarget((ip, 161), timeout=timeout, retries=retries),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication or errorStatus:
            return None
        for varBind in varBinds:
            return str(varBind[1])
    except Exception:
        return None
