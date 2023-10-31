from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import json
import pprint
from bson import ObjectId
from typing import Any



uri = "mongodb+srv://ecommerceitb:ecommerceitb@ecommercecluster.ubewfnb.mongodb.net/?retryWrites=true&w=majority"

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


printer = pprint.PrettyPrinter()


class Product():
    def __init__(self, name, image, category, price, location, specs, stock, times_bought):
        self.name = name
        self.image = image
        self.category = category
        self.price = price
        self.location = location
        self.specs = specs
        self.stock = stock
        self.times_bought = times_bought

    def __str__(self):
        return f'{self.name} {self.price}'
    
    def toDict(self):
        return {
        "name": self.name,
        "image": self.image,
        "category": self.category,
        "price": self.price,
        "location": self.location,
        "specs": self.specs.toDict(),
        "stock": self.stock,
        "times_bought" : self.times_bought
        }
        
from typing import Optional
class Specs():
    def __init__(self, cpu: Optional[str] = "Not specified", ram: Optional[str] = "Not specified", storage: Optional[str] = "Not specified", ddos_protect: Optional[bool] = "Not specified") :
        self.cpu = cpu
        self.ram = ram
        self.storage = storage 
        self.ddos_protect = ddos_protect 
        
    def __str__(self):
        return f'{self.cpu} {self.ram} {self.storage} {self.ddos_protect}'
        
    def toDict(self):
        return {
        "cpu": self.cpu,
        "ram": self.ram,
        "storage": self.storage,
        "ddos_protect": self.ddos_protect
        }


# Select all the documents in the Products collection
def find_all():
    products_documents = products_collection.find()
    for products in products_documents:
        printer.pprint(products)

# Finds all products that belong to the category
def find_by_category(category: str):
    products_by_category = products_collection.find({"category": category})
    for products in products_by_category:
        printer.pprint(products)

# Finds all products that contain the name in the name field and case insensitive
def find_by_name(name: str):
    query = {"name": {"$regex" : name, "$options" : "i"}}
    products_by_name = products_collection.find(query)
    for products in products_by_name:
        printer.pprint(products)
        
# Find a product by its id
def find_by_id(id_product: str) -> object:
    _id_product = ObjectId(id_product)
    return products_collection.find_one({"_id": _id_product})


# Insert a product into the database
def insert_product():
    product1 = Product("Valorant Server", "placeholder.png", "Game", 2.99, "Spain", Specs("I5-8500 4,10 GHz", "DDR4 3200MHz", "SSD", True), 4, 1)
    product2 = Product("Optional", "placeholder.png", "Game", 1.99, "Finland", Specs(), 4, 0)

    products_collection.insert_one(product2.toDict())
    print("Product inserted")

# Delete product by its id
def delete_single_product(id_product: str):
    _id_product = ObjectId(id_product)
    products_collection.delete_one({"_id": _id_product})
    print("Product deleted")
    
# Delete many products by filter
def delete_many_products(filter: str, value: str):
    # If the filter is by id, convert the value to ObjectId
    if filter == "_id":
        value = ObjectId(value)
    # Count the number of products that will be deleted
    deleted_products = products_collection.count_documents({filter : value})
    # Delete the products
    products_collection.delete_many({filter : value})
    print(f"Deleted {deleted_products} products")
    
# Update a product by its id and a field
def update_product(id: str, field: str, value: Any):
    _id = ObjectId(id)
    products_collection.update_one({"_id": _id}, {"$set": {field: value if field != "specs" else value.toDict() }})
    print("Product updated")

# Update a product by its id and multiple fields
def update_product_fields(id: str, fields: dict):
    _id = ObjectId(id)
    products_collection.update_one({"_id": _id}, {"$set": fields})
    print("Product updated")

updated_fields = {"name": "Overwatch Server",
                  "price": 3.99,
                  "specs": Specs("I5-8500 4,10 GHz", "DDR4 3200MHz", "SSD", True).toDict(),
                  "stock": 5,
                  "times_bought": 2}


# ID de prueba 65413a1b65eb4dde32d0e528

#update_product_fields("65413a1b65eb4dde32d0e528", updated_fields)
#printer.pprint(find_by_id("65413a1b65eb4dde32d0e528"))

client.close()