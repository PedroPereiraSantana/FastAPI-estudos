from fastapi import APIRouter, Depends, HTTPException
from schemas import PedidoSchema, ItemPedidoSchema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Pedido, Usuario, ItemPedido

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
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    #essa rota tem duas dependencias, um delas sendo iniciar sessão no banco e a outra validar o token do usuário que está usando essa rota
    #sem esses dois a rota não pode ser acessada 

    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    #está procurando na tabela pedido o pedido que foi puxado na rota e parando quando acahar o primeiro que tem um ID correspondente

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    #se o pedido não foi encontrado a variavel recebe None, esse if testa se é none se for ele retorna o HTTPException
    
    if not usuario.admin:
        if usuario.id != pedido.usuario:
            raise HTTPException(status_code=401, detail="você não tem permissão para executar está ação")
    #aqui está sendo validado se o usuário tem permissão de admin ou se o pedido é do usuário logado que está tentando acessar essa rota
    #caso não for o if recebe True e retorna o HTTPException
    
    pedido.status = "CANCELADO"

    session.commit()
    return {
        "mensagem": f"Pedido número: {pedido.id} cancelado com sucesso",
        "pedido": pedido
    }


@order_router.get("/listar")
async def listar_pedido(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="você não tem permissão para acessar essa rota")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }


@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicioanar_item_pedido(id_pedido: int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para fazer essa alteração")

    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)


    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "mensagem": "Item criado com sucesso",
        "Item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }