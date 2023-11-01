from fastapi import FastAPI
from api.routers.product import router_products

app = FastAPI(
    title="REST API with FastAPI and MongoDB for an eCommerce Store",
    description="This is a simple REST API with FastAPI and MongoDB for an eCommerce Store",
    version = "0.0.1",
    openapi_tags=[{
        "name": "Products",
        "description": "CRUD operations with Products"
    }]
)

app.include_router(router_products)