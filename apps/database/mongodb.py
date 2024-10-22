import os

from pymongo import MongoClient
from pymongo.collection import Collection

from apps.database.config import DBCollections


# Environment variable for MongoDB URL, or fallback to localhost
def get_mongo_client():
    mongo_url = os.getenv(
        "MONGO_URL",
        "mongodb+srv://wajed:lTOT32yLyrp7Zev0@cluster0.frdac.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    )
    return MongoClient(mongo_url)


def get_mongo_collection(collection_name: DBCollections) -> Collection:
    # Get the MongoDB client and database
    client = get_mongo_client()
    db = client["vehicle_allocation_db"]

    # Check if the collection name is valid
    if collection_name not in DBCollections:
        raise ValueError(f"Invalid collection name: {collection_name}")

    # Accessing the value of the Enum
    return db[collection_name.value]


def check_mongodb_connection():
    # Create a new client and connect to the server
    client = get_mongo_client()

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Connection failed: {e}")
