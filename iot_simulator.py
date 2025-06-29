import requests
import random
import time

while True:
    product_id = random.randint(1, 5)
    new_stock = random.randint(10, 100)
    requests.post('http://localhost:5000/update-stock', json={'product_id': product_id, 'stock_level': new_stock})
    print(f'Updated product {product_id} stock to {new_stock}')
    time.sleep(5)