from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema

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
async def criar_conta(usuario_schemas: UsuarioSchema, session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schemas.email).first()
    if usuario:
        # isso valida se o email que foi mandando para a criação da conta já existe dentro do banco de dados
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
        #raise funciona como um return mas para erros, então ele vai retornar o status code do resultado e não 200 porque a resposta do return foi enviada
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schemas.senha)
        novo_usuario = Usuario(usuario_schemas.nome, usuario_schemas.email, senha_criptografada, usuario_schemas.ativo, usuario_schemas.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "usuário cadastrado com sucesso"}
