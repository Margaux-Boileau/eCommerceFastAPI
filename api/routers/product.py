from fastapi import APIRouter, Response, status, File, UploadFile, Query
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
    """
    Retrieves all products from the database.

    Returns:
       list[Product]: List of all products found in the database.
    """
    return productsEntity(products_collection.find())

# GET
# Finds all products that belong to the category and case insensitive
@router_products.get("/products/category/{category}", response_model=list[Product], tags=["Products"])
async def get_products_by_category(category: str):
    """
    Retrieves products based on the specified category.

    Args:
        category (str): The category to filter the products by.

    Returns:
       list[Product]: List of products matching the category specified.
    """
    return productsEntity(products_collection.find({"category":{ "$regex": category, "$options" : "i"}}))
# GET
# Finds all products that contain the name in the name field and case insensitive
@router_products.get("/products/name/{name}", response_model=list[Product], tags=["Products"])
async def find_by_name(name: str):
    """
    Finds products by name using a case-insensitive regex search.

    Args:
        name (str): The name to search for.

    Returns:
      list[Product]: List of products containing the query in their name.
    """
    products_by_name = products_collection.find({"name": {"$regex" : name, "$options" : "i"}})
    return productsEntity(products_by_name)

# GET
# Finds a product by it's id
@router_products.get("/products/{id}", response_model=Product, tags=["Products"])
async def get_product_by_id(id: str):
    """
    Retrieves a product from the database by its ID.

    Args:
        id (str): The ID of the product.

    Returns:
        dict: The product retrieved.

    """
    return productEntity(products_collection.find_one({"_id": ObjectId(id)}))

# GET
# Finds all the products that match the id's in the list of id's
@router_products.get("/products/cart/", response_model=list[Product], tags=["Products"])
async def get_products_from_cart(idList: list[str] = Query(...)):
    """
    Retrieves a list of products from the cart based on the provided list of IDs.

    Args:
        idList (list[str]): A list of product IDs.

    Returns:
       list[Product]: List of products matching the provided IDs.
    """
    productList = []
    for id in idList:
        # Checks if the ID is a valid ObjectId
        if ObjectId.is_valid(id):
            product = products_collection.find_one({"_id": ObjectId(id)})
            if product:
                productList.append(product)
    return productsEntity(productList)

# GET
# Get the image of a product by it's filename
@router_products.get("/products/images/{filename}", tags=["Products"])
async def get_product_image(filename: str):
    """
    Retrieves the image file for a given product.

    Args:
        filename (str): The name of the image file.

    Returns:
        FileResponse: The response containing the image file.

    """
    return FileResponse(f"api/uploads/images/{filename}")

# POST
# Insert a product in the Products collection
@router_products.post("/products", response_model=Product, tags=["Products"])
async def insert_product(product: Product) -> dict:
    """
    Inserts a new product into the Products collection.

    Args:
        product (Product): The product to be inserted.

    Returns:
        dict: The inserted product as a dictionary.

    """
    insert = products_collection.insert_one(Product.model_dump(product))
    new_product = products_collection.find_one({"_id": insert.inserted_id})
    return productEntity(new_product)

# POST
# Upload an image to the uploads/images folder
@router_products.post("/products/images", status_code=status.HTTP_200_OK, tags=["Products"])
async def upload_product_image(file: UploadFile = File(...)):
    """
    Uploads an image of a product to the path specified.

    Args:
        file (UploadFile): The image file to be uploaded.

    Returns:
        dict: A dictionary containing the upload status and information.
            - success (bool): True if the file was uploaded successfully.
            - filename (str): The name of the uploaded file.
            - message (str): A message indicating the status of the upload.
            - error (str, optional): An error message if the file format is not allowed.
    """  
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
        
    return {"success": True, "filename": file.filename, "message": "File uploaded successfully"}

# PUT
# Update a product in the Products collection
@router_products.put("/products/{id}", response_model=Product, tags=["Products"])
async def update_product(id: str, product: Product) -> dict:
    """
    Update a product into the products collection.

    Args:
        id (str): The ID of the product to update.
        product (Product): The updated product data.

    Returns:
        dict: The updated product.
    """
    products_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": Product.model_dump(product)})
    return productEntity(products_collection.find_one({"_id": ObjectId(id)}))

# PATCH
# Update the times a product have been bought in the Products collection
@router_products.patch("/products/updatecounter/", response_model=list[Product], tags=["Products"])
async def update_product_times_bought(idList: list[str] = Query(...)) -> dict:
    """
    Updates the 'times_bought' field of the products with the given IDs provided on the provided list.

    Args:
        idList (list[str]): List of product IDs to update.

    Returns:
        dict: Updated product list.

    """
    # Update the product that matches the id
    productList = []
    for id in idList:
        # Checks if the ID is a valid ObjectId
        if ObjectId.is_valid(id):
            product = products_collection.find_one({"_id": ObjectId(id)})
            if product:
                products_collection.update_one({"_id": ObjectId(id)}, {"$set": {"times_bought": product.get("times_bought") + 1}})
                productList.append(products_collection.find_one({"_id": ObjectId(id)}))
     # Return the updated product list
    return productsEntity(productList)

# DELETE
# Finds a product by it's id
@router_products.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Products"])
async def delete_product_by_id(id: str):
    """
    Deletes a product by its ID.

    Args:
        id (str): The ID of the product to be deleted.

    Returns:
        Response: The HTTP response indicating the success of the deletion (204).
    """
    productEntity(products_collection.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

