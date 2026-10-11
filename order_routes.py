from fastapi import APIRouter, Depends, HTTPException
from schemas import PedidoSchema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Pedido

order_router = APIRouter(
        prefix="/pedidos", 
        tags=["pedidos"],
        dependencies=[Depends(verificar_token)]
    )

#decorator é esse código a seguir identificado por esse @ na frente
#nele você pega o prefixo, colocado o metodo que você quer usar, nesse caso foi get, e define a rota nele do parentese
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

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido número: {id_pedido} cancelado com sucesso",
        "pedido": pedido
    }

