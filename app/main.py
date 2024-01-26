from fastapi import FastAPI
from api.routers.product import router_products
from fastapi.staticfiles import StaticFiles


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
app.mount("/api/uploads", StaticFiles(directory="api/uploads"), name="uploads")