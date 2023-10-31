import bson

def product_entity(product) -> dict:
    return { 
            "_id" : str(product["_id"]),
            "name": product["name"],
            "image": product["image"],
            "category": product["category"],
            "price": product["price"],
            "location": product["location"],
            "specs": product["specs"],
            "stock": product["stock"],
            "times_bought" : product["times_bought"]
        }
  
# A las entities se les puede llamar serials o serializers  

def products_entity(products) -> list:
    return [product_entity(product) for product in products]