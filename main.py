from fastapi import FastAPI
from api.routers.product import router_products

app = FastAPI()

app.include_router(router_products)