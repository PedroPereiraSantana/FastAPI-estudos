from fastapi import APIRouter, Depends
from models import Usuario
from dependencies import pegar_sessao

#isso define um prefixo, então toda rota que for criada nesse arquivo vai partir do caminho '/auth'
auth_router = APIRouter(
        prefix="/auth", 
        tags=["autenticacao"]
    ) 

@auth_router.get("/")
async def autenticar():
    """
        Essa é a rota padrão de autenticação do sistema
    """
    return {
        "mensagem": "Você acessou a rota de autenticação",
        "autenticado": False
    }

@auth_router.post("/criar_conta")
async def criar_conta(email: str, senha: str, nome: str, session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        # isso valida se o email que foi mandando para a criação da conta já existe dentro do banco de dados
        return {"mensagem": "já existe um usuário com esse email cadastrado"}
    else:
        novo_usuario = Usuario(nome, email, senha)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "usuário cadastrado com sucesso"}
