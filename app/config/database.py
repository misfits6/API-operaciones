from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = ""


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.todo_db
collection = db.todo_collection


