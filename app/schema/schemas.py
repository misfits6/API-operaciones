def individual_serial(todo) -> dict:
    """
    Serializes a single todo item into a dictionary.
    """
    return {
        "id": str(todo["_id"]),
        "name": todo["name"],
        "description": todo["description"],
        "completed": todo["completed"],
    }

def list_serial(todos) -> list:
    """
    Serializes a list of todo items into a list of dictionaries.
    """
    return [individual_serial(todo) for todo in todos]

