from .pass_db_service import PassDBService 
from .route_operation_service import RouteOperationService

import json



class OperationService:
    """Servicio orquestador para el flujo completo de la operación"""
    
    @staticmethod
    async def create_operation():
        """
        Orquesta el flujo completo de creación de una operación:
        1. Consulta datos en PASS DB
        2. Realiza la simulación de la ruta
        3. Guarda los resultados en MongoDB
        4. Actualiza el estado en PASS DB
        
        Args:
            None
        Returns:
            Respuesta con toda la información de la operación creada
        """
        
        # 1. Consulta datos en PASS DB
        pass_db_data = await PassDBService.get_reserves_data()
        pass_db_buses = await PassDBService.get_buses_data()
        
        print(json.dumps(pass_db_data, indent=2))
        print(json.dumps(pass_db_buses, indent=2))
        
        
        
        # 2. Simulacion de la ruta
        simulation_result = await RouteOperationService.simulate_route(pass_db_data)
        
        # mock de resultado de simulación
        asignacion_buses = {
            1: 1,
            2: 1,
            # ... más asignaciones
        }
        
        
        
        
        # # 3. Guardar resultados en MongoDB
        # mongodb_id = await MongoDBService.save_operation(pass_db_data, simulation_result)
        
        
        
        # 4. Actualizar el estado en PASS DB
        buses_asigned = await PassDBService.update_operation_buses(asignacion_buses)
        print(f"Se han actualizado {buses_asigned} buses en PASS DB")
        
        # Retornar la respuesta con toda la información de la operación creada
        return {"message": "Operation created successfully"}
    
        # return {
        #     "message": "Operation created successfully",
        #     "pass_db_data": pass_db_data,
        #     "simulation_result": simulation_result,
        #     "mongodb_id": mongodb_id
        # }





