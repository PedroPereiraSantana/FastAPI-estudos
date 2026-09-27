from fastapi import APIRouter

order_router = APIRouter(
        prefix="/pedidos", 
        tags=["pedidos"]
    )

#decorator é esse código a seguir identificado por esse @ na frente
#nele você pega o prefico, colocado o metodo que você quer usar, nesse caso foi get, e define a rota nele do parentese
@order_router.get("/")
#essa função asincrona é executada quando a rota é acessada
async def pedidos():
    return {"mensagem": "você acessou a rota de pedidos"}
