from fastapi import APIRouter, HTTPException
from ..config.database import collection
from ..config.pass_db import fetch_all
from ..services.operation_service import OperationService
# from bson import ObjectId


router = APIRouter()


# PASS - OP

# Endpoint para leer datos de una tabla en PostgreSQL
@router.get("/usuarios/")
async def get_usuarios(limit: int = 10, offset: int = 0):
    """
    Obtiene una lista de usuarios desde la base de datos PostgreSQL
    """
    query = """
        SELECT * FROM "Ticket" 
        LIMIT %s OFFSET %s
    """
    
    result = fetch_all(query, (limit, offset))
    return result




# Route operations endpoint
@router.post("/")
async def create_operation():
    """
    Crea una nueva operación según información de PASS DB.
    
    El flujo completo incluye:
    1. Consulta de datos en PASS DB
    2. Simulación de la ruta
    3. Guardado de resultados en MongoDB
    4. Actualización del estado en PASS DB
    """
    
    try:
        # Utilizamos el servicio orquestador para manejar todo el flujo
        result = await OperationService.create_operation()
        return result
    except ValueError as e:
        # Error de validación
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Cualquier otro error
        raise HTTPException(status_code=500, detail=f"Error al crear la operación: {str(e)}")











