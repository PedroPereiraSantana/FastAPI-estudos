import requests

headers = {
    "Authorization": "Bearer {colocar um token válido aqui}"
}


requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers = headers)

print(requisicao)
print(requisicao.json())