from fastapi import APIRouter, Response, status, File, UploadFile, Body
from fastapi.responses import FileResponse
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

# Get the image of a product by it's filename
@router_products.get("/products/images/{filename}", tags=["Products"])
async def get_product_image(filename: str):
    return FileResponse(f"api/uploads/images/{filename}")

# POST
# Insert a product in the Products collection
@router_products.post("/products", response_model=Product, tags=["Products"])
async def insert_product(product: Product ) -> dict:
    # Insert the product in the Products collection
    insert = products_collection.insert_one(Product.model_dump(product))
    # Get the new product inserted by it's generated id
    new_product = products_collection.find_one({"_id": insert.inserted_id})
    return productEntity(new_product)

# Upload an image to the uploads/images folder
@router_products.post("/products/images", status_code=status.HTTP_200_OK, tags=["Products"])
async def upload_product_image(file: UploadFile = File(...)):
    
    # Specify the path where the image will be saved
    FILEPATH = "api/uploads/images/"
    filename = file.filename
    
    # Check if the file is an image
    extension = filename.split(".")[-1]
    
    if extension not in ("jpg", "jpeg", "png"):
        return {"error": "File format not allowed"}
    
    # Save the image
    file_content = await file.read()
    
    with open(FILEPATH + filename, "wb") as f:
        f.write(file_content)
        
    return {"success": True, "filename": file.filename, "message": "File uploaded succesfully"}

# PUT
# Update a product in the Products collection
@router_products.put("/products/{id}", response_model=Product, tags=["Products"])
async def update_product(id: str, product: Product) -> dict:
    # Update the product that matches the id
     products_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": Product.model_dump(product)})
     # Return the updated product
     return productEntity(products_collection.find_one({"_id": ObjectId(id)}))

# DELETE

# Finds a product by it's id
@router_products.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Products"])
async def delete_product_by_id(id: str):
    productEntity(products_collection.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

