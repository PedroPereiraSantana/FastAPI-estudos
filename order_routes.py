from fastapi import APIRouter, Depends, HTTPException
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from models import Pedido, Usuario, ItemPedido
from typing import List

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



@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):

    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item do pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para fazer essa alteração")


    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "mensagem": "Item pedido removido",
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

#finalizar pedido (tipo cancelar, porque está pronto)
@order_router.post("/finalizar-pedido/{id_pedido}")
async def finalizar_pedido( id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=403, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Você não tem permissão para fazer está alteração")

    pedido.status = "FINALIZADO"
    session.commit()

    return{
        "mensagem": "Pedido finalizado com sucesso"
    }

#vizualizar 1 pedido
@order_router.get("/vizualizar-pedido/{id_pedido}")
async def vizualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao)):
    itens_pedido = session.query(ItemPedido).filter(ItemPedido.pedido == id_pedido).all() #esse .all() é necessário se não a consulta não ocorre

    if not itens_pedido:
        raise HTTPException(status_code=403, detail="Esse pedido não foi encotrado")

    return {
        "mensagem" : "os itens desse pedido são:",
        "itens_pedido": itens_pedido
    }
    

#vizualizar todos os pedidos de 1 usuário
@order_router.get("/pedidos-usuario/{id_usuario}", response_model=List[ResponsePedidoSchema]) 
#esse response_model é definido no schema como padrão de resposta na requisição
#o List[] que é um import da bibliote typing é usando para que o response_model não fique limitado a retornar apenas um item, ele retorna uma lista

async def pedido_usuario(id_usuario: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedidos_usuario = session.query(Pedido).filter(Pedido.usuario == id_usuario).all()

    if not pedidos_usuario:
        raise HTTPException(status_code=403, detail="Pedido não encontrado")

    return pedidos_usuario