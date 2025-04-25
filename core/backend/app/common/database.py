import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "database": os.getenv("POSTGRES_DB"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
}

async def connect_to_db():
    try:
        conn = await asyncpg.connect(**DB_CONFIG)
        print(" Conexión a PostgreSQL establecida.")
        await conn.close()
    except Exception as e:
        print(f" Error al conectar a PostgreSQL: {e}")
