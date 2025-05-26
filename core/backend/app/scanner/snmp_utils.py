import json
from pathlib import Path
from pysnmp.hlapi import (
    getCmd, SnmpEngine, CommunityData, UdpTransportTarget,
    ContextData, ObjectType, ObjectIdentity
)
import re

# Import configuration for SNMP parameters
from app.config import SNMP_COMMUNITY_STRING, SNMP_PORT, SNMP_TIMEOUT, SNMP_RETRIES

# Path to the device_oids.json file
BASE_DIR = Path(__file__).resolve().parent
DEVICE_OIDS_FILE = BASE_DIR / "data" / "device_oids.json"

def load_device_oids():
    """Loads device OID information from the JSON file."""
    try:
        with open(DEVICE_OIDS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # print(f"Error: OID file not found at {DEVICE_OIDS_FILE}")
        return None
    except json.JSONDecodeError:
        # print(f"Error: Could not decode JSON from {DEVICE_OIDS_FILE}")
        return None

# Modified get_snmp_data_sync to implement SNMPv2c -> SNMPv1 fallback
def get_snmp_data_sync(snmp_engine, host, oids, 
                       community_string=SNMP_COMMUNITY_STRING, 
                       port=SNMP_PORT, 
                       timeout=SNMP_TIMEOUT, 
                       retries=SNMP_RETRIES):
    """
    Synchronously fetches data for a list of OIDs from an SNMP agent.
    Tries SNMPv2c first, then falls back to SNMPv1 if v2c fails for any OID.
    Returns a dictionary of OID -> value.
    """
    final_results = {oid_name: None for oid_name in oids} # Initialize all OIDs to None

    snmp_versions_to_try = [
        {'name': 'v2c', 'mpModel': 1},
        {'name': 'v1', 'mpModel': 0}
    ]

    for version_info in snmp_versions_to_try:
        # print(f"Attempting SNMP {version_info['name']} for {host} OIDs: {list(oids.keys())}")
        current_version_results = {}
        version_completely_successful = True

        for oid_name, oid_value in oids.items():
            iterator = getCmd(
                snmp_engine,
                CommunityData(community_string, mpModel=version_info['mpModel']),
                UdpTransportTarget((host, port), timeout=timeout, retries=retries),
                ContextData(),
                ObjectType(ObjectIdentity(oid_value))
            )
            
            error_indication, error_status, error_index, var_binds = next(iterator)

            if error_indication:
                # print(f"SNMP {version_info['name']} errorIndication for {oid_name} on {host}: {error_indication}")
                version_completely_successful = False
                break # Error with this OID, this version attempt fails for all OIDs
            elif error_status:
                # print(f"SNMP {version_info['name']} errorStatus for {oid_name} on {host}: {error_status.prettyPrint()}")
                version_completely_successful = False
                break # Error with this OID, this version attempt fails for all OIDs
            else:
                for var_bind in var_binds: # Should be only one var_bind for a GET
                    current_version_results[oid_name] = str(var_bind[1])
        
        if version_completely_successful:
            # print(f"SNMP {version_info['name']} completely successful for all OIDs on {host}")
            final_results = current_version_results
            # Ensure all requested oids have a key, even if successfully fetched value is None (should not happen with current logic)
            for oid_name in oids.keys():
                if oid_name not in final_results:
                    final_results[oid_name] = None # Should already be covered by var_binds or caught by error
            break # Successfully fetched all OIDs with this version, no need to try other versions
        else:
            # print(f"SNMP {version_info['name']} failed for one or more OIDs on {host}.")
            if version_info['name'] == 'v2c':
                # print("Will attempt SNMPv1.")
                final_results = {oid_name: None for oid_name in oids} # Reset results before trying v1
                continue # Try next version (SNMPv1)
            else: # SNMPv1 also failed or was the only one attempted and failed
                # print("SNMPv1 failed. Returning results from this attempt (may be incomplete).")
                # For v1, we return whatever was fetched, even if partial.
                # final_results should already be initialized with Nones, update with what v1 got.
                for oid_name_key, value in current_version_results.items():
                    final_results[oid_name_key] = value
                # Ensure any OIDs not even attempted in v1 (due to early break on another OID) are None
                for oid_name_key in oids.keys():
                    if oid_name_key not in final_results:
                        final_results[oid_name_key] = None
                break # Stop trying versions

    return final_results


# No changes needed for identify_device_sync itself.
def identify_device_sync(host_ip):
    """
    Identifies the brand and model of a device using SNMP, using configured parameters.
    Returns a dictionary with 'ip', 'brand', 'model', 'sysDescr', and any other fetched OID data.
    """
    device_info = {"ip": host_ip, "brand": "Unknown", "model": "Unknown", "sysDescr": None}
    device_oids_data = load_device_oids()

    if not device_oids_data:
        return device_info 

    snmp_engine = SnmpEngine() 

    sys_descr_oid_str = "1.3.6.1.2.1.1.1.0"
    sys_descr_data = get_snmp_data_sync(
        snmp_engine, host_ip, {"sysDescr": sys_descr_oid_str}
    )
    
    sys_descr = sys_descr_data.get("sysDescr")
    device_info["sysDescr"] = sys_descr

    if not sys_descr:
        return device_info 

    found_specific_model = False
    for manufacturer in device_oids_data.get("manufacturers", []):
        man_name = manufacturer.get("name")
        for model_spec in manufacturer.get("models", []):
            pattern = model_spec.get("sysDescr_pattern")
            if pattern and re.search(pattern, sys_descr, re.IGNORECASE):
                device_info["brand"] = man_name
                device_info["model"] = model_spec.get("model_name", "Unknown")
                
                specific_model_oids = model_spec.get("oids", {})
                if specific_model_oids:
                    model_details = get_snmp_data_sync(
                        snmp_engine, host_ip, specific_model_oids
                    )
                    for k, v in model_details.items():
                        if v is not None and k not in ["ip", "brand", "model", "sysDescr"]:
                             device_info[k] = v
                    
                    if man_name == "MikroTik" and model_details.get("board_name"):
                        device_info["model"] = model_details["board_name"]
                
                found_specific_model = True
                break 
        if found_specific_model:
            break 

    if not found_specific_model and device_info["brand"] == "Unknown":
        for manufacturer in device_oids_data.get("manufacturers", []):
            man_name = manufacturer.get("name")
            if re.search(r'\b' + re.escape(man_name) + r'\b', sys_descr, re.IGNORECASE):
                device_info["brand"] = man_name
                break
    
    if device_info["brand"] != "Unknown":
        for manufacturer_data in device_oids_data.get("manufacturers", []):
            if manufacturer_data.get("name") == device_info["brand"]:
                general_brand_oids = manufacturer_data.get("general_oids", {})
                if general_brand_oids:
                    general_details = get_snmp_data_sync(
                        snmp_engine, host_ip, general_brand_oids
                    )
                    for k, v in general_details.items():
                        if v is not None and k not in device_info: 
                           device_info[k] = v
                break
                
    return device_info

# Example usage block (commented out)
# if __name__ == '__main__':
#     # ... (testing code would go here) ...
#     print("SNMPv2c/v1 fallback test finished.")
