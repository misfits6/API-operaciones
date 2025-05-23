from .pass_db_service import PassDBService 
from .route_operation_service import RouteOperationService

import json
from pprint import pprint
from datetime import datetime

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
        
        
        # 2. FORMA DETALLADA - Primera reserva completa
        print("\n" + "=" * 80)
        print("PRIMERA RESERVA COMPLETA (Pretty Print)")
        print("=" * 80)
        if pass_db_data:
            pprint(pass_db_data[0], indent=2, width=120)
            print("=" * 80)
            pprint(pass_db_data[-1], indent=2, width=120)
            print("=" * 80)
            print(json.dumps(pass_db_buses, indent=2))
        
        
        
        # 2. Simulacion de la ruta
        simulation_result = await RouteOperationService.asignar_buses_a_reservas(pass_db_data, pass_db_buses)
        RouteOperationService.mostrar_asignaciones_detalladas(pass_db_data, pass_db_buses, simulation_result)
        
        
        
        # # 3. Guardar resultados en MongoDB
        # mongodb_id = await MongoDBService.save_operation(pass_db_data, simulation_result)
        
        
        
        # 4. Actualizar el estado en PASS DB
        buses_asigned = await PassDBService.update_operation_buses(simulation_result)
        print(f"Se han actualizado {buses_asigned} buses en PASS DB")
        
        # Retornar la respuesta con toda la información de la operación creada
        return {"message": f"Se han actualizado {buses_asigned} buses en PASS DB"}
    
        # return {
        #     "message": "Operation created successfully",
        #     "pass_db_data": pass_db_data,
        #     "simulation_result": simulation_result,
        #     "mongodb_id": mongodb_id
        # }





