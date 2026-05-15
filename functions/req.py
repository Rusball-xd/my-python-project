import requests
async def add_i(b):
    g = requests.post('http://10.9.0.1:5000/add', json=b)
    return g

