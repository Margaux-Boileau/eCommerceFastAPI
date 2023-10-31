from fastapi import APIRouter
from config.database import products_collection
from api.schemas.schemas import product_entity, products_entity
from api.models.product import Product


router_products = APIRouter()

# GET
# Select all the documents in the Products collection
@router_products.get("/products")
async def get_all_products():
    return products_entity(products_collection.find())

# Finds all products that belong to the category
@router_products.get("/products/category/{category}")
async def get_products_by_category(category: str):
    return products_entity(products_collection.find({"category": category}))


# POST
# Insert a product in the Products collection
@router_products.post("/products")
async def insert_product(product: Product) -> dict:
    product["specs"].append(dict(product["specs"]))
    products_collection.insert_one(dict(product))