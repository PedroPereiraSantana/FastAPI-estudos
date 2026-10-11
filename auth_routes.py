from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


#isso define um prefixo, então toda rota que for criada nesse arquivo vai partir do caminho '/auth'
auth_router = APIRouter(
        prefix="/auth", 
        tags=["autenticacao"]
    ) 

def criar_token(id_usuario):
    data_expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #definindo o tempo que o token vai durar, usando o tempo atual que o token é criado + o tempo definido no .env

    dic_info = {
        "sub": id_usuario,
        "exp": data_expiracao
    }
    #definindo o dicionário de informações para a criação do token

    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    #está definindo a criação do token, colocando como parâmetro o dicionário, secret key e o algoritimo que está usando

    return jwt_codificado

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario




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
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        # JWT Bearer - headers = {"Access-Token": "Bearer token"}
        return{
            "access_token": access_token,
            "token_type": "Bearer"
        }


#rota de deletar usuário
@auth_router.delete("/usuario/{usuario_id}")
def deletar_usuario(
    usuario_id: int,
    db: Session = Depends(pegar_sessao)
):
    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario não encontrado"
        )

    db.delete(usuario)
    db.commit()
