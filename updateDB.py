from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_database():
    CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
    if not CONNECTION_STRING:
        print("Connection string not found in .env file.")
        return None
    try:
        client = MongoClient(CONNECTION_STRING)
        db = client['inventory']
        if 'hannaford' in db.list_collection_names():
            print("Connected to the inventory database and found the 'hannaford' collection successfully!")
            return db['hannaford']
        else:
            print("Connected to the inventory database, but 'hannaford' collection not found.")
            return None
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return None
    
collection = get_database()

if collection is not None:
    documents = collection.find({ "image_links": { "$exists": True } })

    for doc in documents:
        collection.update_one(
            { "_id": doc["_id"] },
            { "$rename": { "image_links": "images_links" } }
        )

    print("Completed renaming 'image_links' to 'images_links' for matching documents.")
else:
    print("Collection not found. Ensure 'hannaford' collection exists in the database.")