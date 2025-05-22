from ..config.pass_db import fetch_all, execute_update

from typing import List, Dict, Any

class PassDBService:
    """Servicio para interactuar con PASS DB"""
    
    @staticmethod
    async def get_reserves_data() -> List[Dict[str, Any]]:
        """Consulta datos de la operacion en PASS DB
        Args:
            None
        
        Returns:
            dict: datos de reservas, pasajeros, vuelos y hospedajes
        """
        
        query = """
            SELECT 
                r.id AS reserva_id,
                r.fecha_emision AS fecha_reserva,
                r.num_pasajeros,
                
                -- Datos del pasajero
                p.id AS pasajero_id,
                p.nombre AS nombre_pasajero,
                p.apellido AS apellido_pasajero,
                p.telf AS telefono_pasajero,
                p.correo,
                
                -- Datos del vuelo
                v.id AS vuelo_id,
                v.codigo_vuelo,
                v.aerolinea,
                v.aeropuerto_salida,
                v.aeropuerto_llegada,
                v.fecha_salida,
                v.hora_salida,
                
                -- Datos del hospedaje
                h.id AS hospedaje_id,
                h.codigo_reserva,
                h.nombre AS nombre_hospedaje,
                h.direccion,
                h.fecha_entrada,
                h.fecha_salida,
                h.num_habitacion,
                h.lat,
                h.lon
                
            FROM 
                "Reserva" r
                INNER JOIN "Pasajero" p ON r.pasajero_id = p.id
                INNER JOIN "Vuelo" v ON r.vuelo_id = v.id
                INNER JOIN "Hospedaje" h ON r.hospedaje_id = h.id;
            """
        
        reservas = PassDBService._reserves_data_to_dict(fetch_all(query))
        return reservas
    
    @staticmethod
    async def get_buses_data() -> List[Dict[str, Any]]:
        """Consulta datos de los buses en PASS DB
        Args:
            None
        
        Returns:
            dict: datos de buses y conductores
        """
        # TODO: organizar bien la consulta con los datos que son
        query = """
            SELECT 
                -- Datos del bus
                b.id AS bus_id,
                b.codigo,
                b.nombre AS nombre_bus,
                b.tipo_servicio,
                b.num_pasajeros,
                b.modelo,
                
                -- Datos del conductor
                c.id AS conductor_id,
                c.nombre AS nombre_conductor,
                c.apellido AS apellido_conductor,
                c.activo AS estado_conductor
                
            FROM 
                "Buses" b
                INNER JOIN "Conductor" c ON b.conductor_id = c.id;
            """
        
        buses = PassDBService._bus_data_to_dict(fetch_all(query))
        return buses
    
    
    
    
    @staticmethod
    async def update_operation_buses(asignacion_buses):
        """Actualiza el estado de la operación en PASS DB.
            indicando que los buses han sido asignados y actualizar en tickets.
        Args:
            None
        
        Returns:
            None
        """
        
        # Construir la consulta SQL con CASE WHEN
        query = """
        UPDATE "Ticket" 
        SET bus_id = CASE reserva_id 
        """

        # Agregar cada caso
        for reserva_id, bus_id in asignacion_buses.items():
            query += f"WHEN {reserva_id} THEN {bus_id} "

        # Completar la consulta
        query += "END WHERE reserva_id IN (" + ",".join(str(id) for id in asignacion_buses.keys()) + ")"
        
        return  execute_update(query)
    
    
    
    @staticmethod
    def _reserves_data_to_dict(data_db):
        """Convierte los datos de la operación a un diccionario
        Args:
            data: datos de la operación
        
        Returns:
            dict: datos de la operación en formato diccionario
        """
        reservas_organizadas = []
    
        for dato in data_db:
            # Convertir RealDictRow a diccionario normal
            dato_dict = dict(dato)
            
            # Función auxiliar para formatear fechas
            def format_date(date_obj):
                return date_obj.strftime("%Y-%m-%d") if date_obj else None
            
            # Crear estructura organizada
            reserva = {
                "reserva": {
                    "id": dato_dict["reserva_id"],
                    "fecha": format_date(dato_dict["fecha_reserva"]),
                    "num_pasajeros": dato_dict["num_pasajeros"]
                },
                "pasajero": {
                    "id": dato_dict["pasajero_id"],
                    "nombre": dato_dict["nombre_pasajero"],
                    "apellido": dato_dict["apellido_pasajero"],
                    "telefono": dato_dict["telefono_pasajero"],
                    "correo": dato_dict["correo"]
                },
                "vuelo": {
                    "id": dato_dict["vuelo_id"],
                    "codigo": dato_dict["codigo_vuelo"],
                    "aerolinea": dato_dict["aerolinea"],
                    "aeropuerto_salida": dato_dict["aeropuerto_salida"],
                    "aeropuerto_llegada": dato_dict["aeropuerto_llegada"],
                    "fecha_salida": format_date(dato_dict["fecha_salida"]),
                    "hora_salida": dato_dict["hora_salida"]
                },
                "hospedaje": {
                    "id": dato_dict["hospedaje_id"],
                    "codigo_reserva": dato_dict["codigo_reserva"],
                    "nombre": dato_dict["nombre_hospedaje"],
                    "direccion": dato_dict["direccion"],
                    "fecha_entrada": format_date(dato_dict["fecha_entrada"]),
                    "num_habitacion": dato_dict["num_habitacion"],
                    "ubicacion": {
                        "lat": dato_dict["lat"],
                        "lon": dato_dict["lon"]
                    }
                }
            }
            
            reservas_organizadas.append(reserva)
        
        return reservas_organizadas
    
    
    @staticmethod
    def _bus_data_to_dict(data_db):
        """Convierte los datos de los buses a un diccionario
        Args:
            data: datos de los buses
        
        Returns:
            dict: datos de los buses en formato diccionario
        """
        buses_organizados = []
    
        for dato in data_db:
            # Convertir RealDictRow a diccionario normal
            dato_dict = dict(dato)
            
            # Crear estructura organizada
            # TODO: Organizar los datos de los buses y conductores
            bus = {
                "bus": {
                    "id": dato_dict["bus_id"],
                    "codigo": dato_dict["codigo"],
                    "nombre": dato_dict["nombre_bus"],
                    "tipo_servicio": dato_dict["tipo_servicio"],
                    "num_pasajeros": dato_dict["num_pasajeros"],
                    "modelo": dato_dict["modelo"]
                },
                "conductor": {
                    "id": dato_dict["conductor_id"],
                    "nombre": dato_dict["nombre_conductor"],
                    "apellido": dato_dict["apellido_conductor"],
                    "activo": dato_dict["estado_conductor"]
                }
            }
            
            buses_organizados.append(bus)
        
        return buses_organizados

