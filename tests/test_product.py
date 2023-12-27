from fastapi.testclient import TestClient
from main import app
from bson import ObjectId

client = TestClient(app)

def test_read_products():
    """
    Test case for reading products.

    This function sends a GET request to the '/products' endpoint
    and asserts that the response status code is 200.
    """
    response = client.get("/products")
    assert response.status_code == 200

def test_read_product_by_id():
    """
    Test case for reading a product by it's id.
    This function sends a GET request to the '/products' endpoint with a valid id
    and asserts that the response status code is 200 and the product specified by the id is returned.
    """
    response = client.get("/products/65413a1b65eb4dde32d0e528")
    assert response.status_code == 200
    assert response.json() == {
    "id": "65413a1b65eb4dde32d0e528",
    "name": "Minecraft Server [Premium]",
    "image": "minecraft.png",
    "category": "Game",
    "price": 3.99,
    "location": "Spain",
    "specs": {
      "cpu": "I5-8500 4,10 GHz",
      "ram": "DDR4 3200MHz",
      "storage": "SSD",
      "ddos_protect": True
    },
    "stock": 5,
    "times_bought": 6
  }
    
def test_read_product_by_its_ids():
    """
    Test case for reading products by their ids.
    This function sends a GET request to the '/products/cart' endpoint with a valid id list
    and asserts that the response status code is 200 and the products specified by the id list are returned.
    """
    response = client.get("/products/cart/?idList=65413a1b65eb4dde32d0e528idList=655a0b43ec59ab4f1db24261")
    assert response.status_code == 200
    assert response.json() == [
   {
    "id": "65413a1b65eb4dde32d0e528",
    "name": "Minecraft Server [Premium]",
    "image": "minecraft.png",
    "category": "Game",
    "price": 3.99,
    "location": "Spain",
    "specs": {
      "cpu": "I5-8500 4,10 GHz",
      "ram": "DDR4 3200MHz",
      "storage": "SSD",
      "ddos_protect": True
    },
    "stock": 5,
    "times_bought": 6
  },
  {
    "id": "655a0b43ec59ab4f1db24261",
    "name": "Music Bot TS3",
    "image": "music.avif",
    "category": "Music",
    "price": 0.99,
    "location": "Spain",
    "specs": {
      "cpu": None,
      "ram": None,
      "storage": "2TB NVMe SSD",
      "ddos_protect": True
    },
    "stock": 10,
    "times_bought": 2
  },
]