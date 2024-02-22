from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import dotenv_values

secrets = dotenv_values(".env")

uri = f"mongodb+srv://{secrets['DB_USER']}:{secrets['DB_PASS']}@ecommercecluster.ubewfnb.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
# Select the eCommerceStore database
ecommerce_db = client.eCommerceStore
# List all the collections in the eCommerceStore database
collections = ecommerce_db.list_collection_names()
# Select the Products collection
products_collection = ecommerce_db.Products