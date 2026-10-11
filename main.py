# para rodar o código precisa executar no terminal: uvicorn main:app --reload
from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()
#essa função procura o arquivo .env no arquivo

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
#os.getenv() procura no arquivo .env essa váriavel e armazena o valor dela, nesse caso armazenamos o que ele achou em SECRET_KEY


app = FastAPI()
#Cria a instancia principal da aplicação, a partir dela você registra rotas, configura funcionalidades e disponibiliza os endpoints da API

bcrypt_context = CryptContext(
    schemes=["bcrypt"], 
    #schemes informa qual o hash de senha você pretende utilizar
    deprecated="auto"
)
"""
    está armazenando a função de criptorgrafia do CryptContext na variavel bcrypt_context, 
    ela vai ser usada quando for necessário criptgrafar algo ou validar algo que está criptografado
    como validar uma senha, está função básicamente está armazenando nossa configurações de criptografia
"""

from auth_routes import auth_router
from order_routes import order_router
#esses dois tem que ser importados após a criação do app=fastapi porque essas importações não funcionam sem ela

app.include_router(auth_router)
app.include_router(order_router)
#aqui você está informando na pasta main.py as outras configurçaões de rotas que tem na sua aplicação

