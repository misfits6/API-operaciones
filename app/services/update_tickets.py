import psycopg2



# Datos de asignación
asignacion_buses = {
    # reserva_id: bus_id
    1: 1,
    2: 1,
    # ... más asignaciones
}

# conn = psycopg2.connect(
#     database="tu_base_de_datos",
#     user="tu_usuario",
#     password="tu_contraseña",
#     host="localhost"
# )
# cursor = conn.cursor()

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
print(query)


# # Ejecutar la consulta
# cursor.execute(query)
# conn.commit()
# conn.close()

