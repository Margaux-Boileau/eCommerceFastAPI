
def productEntity(product) -> dict:
    return { 
            "id" : str(product["_id"]),
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

def productsEntity(products) -> list:
    return [productEntity(product) for product in products]

def specsEntity(specs) -> dict:
    return { 
            "cpu" :specs["cpu"],
            "ram": specs["cpu"],
            "storage": specs["storage"],
            "ddos_protect": specs["ddos_protect"]
        }