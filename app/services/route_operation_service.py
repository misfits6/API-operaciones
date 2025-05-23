from collections import defaultdict
from datetime import time
from typing import List, Dict, Any


class RouteOperationService:
    """Servicio para realizar simulaciones de rutas"""
    
    @staticmethod
    async def asignar_buses_a_reservas(reservas, buses):
        """
        Simula una operación de ruta basada en las reservas y buses proporcionados
        
        Args:
            pass_db_data: Datos de reservas desde PASS DB
            pass_db_buses: Datos de los buses desde PASS DB
            
        Returns:
            Resultado de la simulación con asignaciones de buses
        """
        
        
        
        # Verificar que hay buses disponibles
        if not buses:
            raise ValueError("No hay buses disponibles para asignar")
        
        # Crear una lista de IDs de buses para asignación cíclica
        bus_ids = [bus['bus']['id'] for bus in buses]
        
        # print(f"IDs de buses disponibles: {bus_ids}")
        
        # Agrupar reservas por hora de vuelo y tipo de reserva
        grupos = defaultdict(list)
        
        for reserva in reservas:
            # Extraer la hora de salida del vuelo
            hora_salida = reserva['vuelo']['avion']['hora_salida']
            
            # Si la hora es un objeto time, convertirlo a string para usarlo como clave
            if isinstance(hora_salida, time):
                hora_str = hora_salida.strftime("%H:%M:%S")
            else:
                hora_str = str(hora_salida)
            
            # Extraer el tipo de reserva
            tipo_reserva = reserva['reserva']['tipo_reserva']
            
            # Crear una clave única para el grupo
            clave_grupo = f"{hora_str}_{tipo_reserva}"
            
            # Agregar la reserva al grupo correspondiente
            grupos[clave_grupo].append(reserva)
        
        
        
        
        # Diccionario para almacenar las asignaciones finales
        asignacion_buses = {}
        
        # Índice para rastrear qué bus asignar (implementa la asignación cíclica)
        indice_bus_actual = 0
        
        # Procesar cada grupo de reservas
        # Ordenamos las claves para tener un orden consistente
        for clave_grupo in sorted(grupos.keys()):
            reservas_grupo = grupos[clave_grupo]
            
            # Asignar el bus actual a todas las reservas de este grupo
            bus_id_asignado = bus_ids[indice_bus_actual]
            
            for reserva in reservas_grupo:
                reserva_id = reserva['reserva']['id']
                asignacion_buses[reserva_id] = bus_id_asignado
            
            # Mover al siguiente bus para el próximo grupo
            indice_bus_actual = (indice_bus_actual + 1) % len(bus_ids)
        
        return asignacion_buses



    # Función auxiliar para visualizar las asignaciones de manera más clara
    @staticmethod
    def mostrar_asignaciones_detalladas(reservas: List[Dict[str, Any]], 
                                    buses: List[Dict[str, Any]], 
                                    asignaciones: Dict[int, int]) -> None:
        """
        Muestra un resumen detallado de las asignaciones realizadas.
        Útil para verificar que las asignaciones se hicieron correctamente.
        """
        
        # Crear diccionario de buses para búsqueda rápida
        buses_dict = {bus['bus']['id']: bus for bus in buses}
        
        # Agrupar reservas por bus asignado
        reservas_por_bus = defaultdict(list)
        for reserva_id, bus_id in asignaciones.items():
            reservas_por_bus[bus_id].append(reserva_id)
        
        print("=== RESUMEN DE ASIGNACIONES ===\n")
        
        for bus_id in sorted(reservas_por_bus.keys()):
            bus_info = buses_dict[bus_id]
            print(f"Bus {bus_id} - {bus_info['bus']['nombre']} ({bus_info['conductor']['nombre']} {bus_info['conductor']['apellido']})")
            print("-" * 80)
            
            # Buscar las reservas asignadas a este bus
            for reserva in reservas:
                if reserva['reserva']['id'] in reservas_por_bus[bus_id]:
                    hora = reserva['vuelo']['avion']['hora_salida']
                    if isinstance(hora, time):
                        hora_str = hora.strftime("%H:%M:%S")
                    else:
                        hora_str = str(hora)
                    
                    print(f"  Reserva {reserva['reserva']['id']}: "
                        f"{reserva['pasajero']['nombre']} {reserva['pasajero']['apellido']} - "
                        f"Hora: {hora_str} - "
                        f"Tipo: {reserva['reserva']['tipo_reserva']}")
            
            print()

