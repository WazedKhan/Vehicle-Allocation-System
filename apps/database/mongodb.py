import os

from pymongo import MongoClient


# Environment variable for MongoDB URL, or fallback to localhost
def get_mongo_client():
    mongo_url = os.getenv(
        "MONGO_URL",
        "mongodb+srv://wajed:lTOT32yLyrp7Zev0@cluster0.frdac.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    )
    return MongoClient(mongo_url)


def get_mongo_collection(collection_name: str):
    client = get_mongo_client()
    db = client["vehicle_allocation_db"]
    return db[collection_name]


def check_mongodb_connection():
    # Create a new client and connect to the server
    client = get_mongo_client()

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Connection failed: {e}")
