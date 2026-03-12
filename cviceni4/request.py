import json
import requests

if __name__ == "__main__":
    data = {"aaa": 1, "bbb": [1,2,3,4]}
    responce = requests.post('http://127.0.0.1:5000/api', json=data)

    if not responce.ok:
        print("Chyba pri posilani requestu")
    else:
        print(f"Responce: {responce.json()}")