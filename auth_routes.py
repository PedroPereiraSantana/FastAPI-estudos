from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session


#isso define um prefixo, então toda rota que for criada nesse arquivo vai partir do caminho '/auth'
auth_router = APIRouter(
        prefix="/auth", 
        tags=["autenticacao"]
    ) 

def criar_token(id):
    token = f"sefgs865fefse974{id}"
    return token


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
async def criar_conta(usuario_schemas: UsuarioSchema, session: Session = Depends(pegar_sessao)):
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


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    else:
        access_token = criar_token(usuario.id)
        # JWT Bearer - headers = {"Access-Token": "Bearer token"}
        return{
            "access_token": access_token,
            "token_type": "Bearer"
        }
