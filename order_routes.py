from fastapi import APIRouter, Depends
from schemas import PedidoSchema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from models import Pedido

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

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario = pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return{"mensagem": f"Pedido feito com sucesso. ID do pedido: {novo_pedido.id} "}
