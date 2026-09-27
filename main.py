# para rodar o código precisa executar no terminal: uvicorn main:app --reload
from fastapi import FastAPI

app = FastAPI()

#esses dois tem que ser importados após a criação do app=fastapi porque essas importações não funcionam sem ela
from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

