from fastapi import APIRouter, Response, status
from config.database import products_collection
from api.schemas.schemas import productEntity, productsEntity
from api.models.product import Product
from bson import ObjectId
from starlette import status


router_products = APIRouter()

# GET
# Select all the documents in the Products collection
@router_products.get("/products", response_model=list[Product], tags=["Products"])
async def get_all_products():
    return productsEntity(products_collection.find())

# Finds all products that belong to the category and case insensitive
@router_products.get("/products/category/{category}", response_model=list[Product], tags=["Products"])
async def get_products_by_category(category: str):
    return productsEntity(products_collection.find({"category":{ "$regex": category, "$options" : "i"}}))

# Finds all products that contain the name in the name field and case insensitive
@router_products.get("/products/name/{name}", response_model=list[Product], tags=["Products"])
async def find_by_name(name: str):
    products_by_name = products_collection.find({"name": {"$regex" : name, "$options" : "i"}})
    return productsEntity(products_by_name)

# Finds a product by it's id
@router_products.get("/products/{id}", response_model=Product, tags=["Products"])
async def get_product_by_id(id: str):
    return productEntity(products_collection.find_one({"_id": ObjectId(id)}))


# POST
# Insert a product in the Products collection
@router_products.post("/products", response_model=Product, tags=["Products"])
async def insert_product(product: Product) -> dict:
    new_product = products_collection.insert_one(dict(product))
    return productEntity(new_product)

# PUT
# Update a product in the Products collection
@router_products.put("/products/{id}", response_model=Product, tags=["Products"])
async def update_product(id: str, product: Product) -> dict:
    # Update the product that matches the id
     products_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(product)})
     # Return the updated product
     return productEntity(products_collection.find_one({"_id": ObjectId(id)}))

# DELETE

# Finds a product by it's id
@router_products.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Products"])
async def delete_product_by_id(id: str):
    productEntity(products_collection.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

