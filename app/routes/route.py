from fastapi import APIRouter
from ..models.todos import Todo
from ..config.database import collection
from ..config.pass_db import fetch_all
from ..schema.schemas import list_serial, individual_serial
from bson import ObjectId

router = APIRouter()

# Get request method
@router.get("/")
async def get_todos():
    """
    Get all todos from the database.
    """
    todos = list_serial(collection.find())
    return todos

# Post request method
@router.post("/")
async def post_todo(todo: Todo):
    collection.insert_one(dict(todo))


# Put request method
@router.put("/{id}")
async def put_todo(id: str, todo: Todo):
    """
    Update a todo item in the database.
    """
    collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(todo)})
    return individual_serial(collection.find_one({"_id": ObjectId(id)}))

# Delete request method
@router.delete("/{id}")
async def delete_todo(id: str):
    """
    Delete a todo item from the database.
    """
    collection.find_one_and_delete({"_id": ObjectId(id)})
    return {"message": "Todo deleted successfully"}




