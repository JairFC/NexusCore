# core/backend/app/config.py
import os
from dotenv import load_dotenv

# Ensure .env is loaded. This is often done in main.py or at application startup.
# Adding it here provides a fallback if this config module is used standalone.
# If your main application entry point (e.g., main.py) already calls load_dotenv(),
# this specific call might be redundant but is generally safe.
load_dotenv()

UMBRAL_DEFAULT = -67 # Existing config

# SNMP Configuration
# Environment variables are prefixed with NEXUSCORE_ to avoid conflicts.
SNMP_COMMUNITY_STRING = os.getenv("NEXUSCORE_SNMP_COMMUNITY", "public")
SNMP_PORT = int(os.getenv("NEXUSCORE_SNMP_PORT", 161))
SNMP_TIMEOUT = float(os.getenv("NEXUSCORE_SNMP_TIMEOUT", 1.0))
SNMP_RETRIES = int(os.getenv("NEXUSCORE_SNMP_RETRIES", 2))
