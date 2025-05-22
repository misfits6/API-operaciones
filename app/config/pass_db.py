import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

# Cargar variables de entorno
load_dotenv()

def get_postgres_connection():
    """Establece conexión con PostgreSQL usando variables de entorno"""
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )
    return conn

def fetch_all(query, params=None):
    """Ejecuta una consulta y devuelve todos los resultados como diccionarios"""
    conn = get_postgres_connection()
    # RealDictCursor nos permite obtener los resultados como diccionarios
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, params)
        result = cur.fetchall()
    conn.close()
    return result

def execute_update(query, params=None):
    """Ejecuta una consulta de actualización (UPDATE, INSERT, DELETE) y hace commit de los cambios"""
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            affected_rows = cur.rowcount
        conn.commit()
        return affected_rows
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()