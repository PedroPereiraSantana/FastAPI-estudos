from pydantic import BaseModel
#usamos para criar schemas com validação de dados
from typing import Optional
#indica que um valor pode ser de determinado tipo ou None

#o parametro BaseModel serve para validar o tipo dos dados com base nos tipos do pydantic
class UsuarioSchema(BaseModel):
    """
        aqui criamos um modelo de como deve ser recebido um usuário,
        podendo definir os tipos de cada dado, fazendo dessa forma
        invés de no modelo da função de usuário receber 5 parametros
        separados, vai enviar apenas um, e a partir desse um você pode 
        consultar todas as informações que estão dentro dele, Ex: 
            def criar_usuario(usuario: UsuarioSchema)
                print(usuario.nome)
        foi mandado apenas um pacote invés de:
            def criar_usuario(nome, email, senha, ativo, admin)
    """
    nome:str
    email:str
    senha:str
    ativo: Optional[bool]
    admin: Optional[bool]


    class Config:
        from_attributes = True
    """
        Essa função permite que o pydantic pegue os dados a partir dos 
        atributor de um objeto invés de exigir que venham de um dicionário,
        dessa forma você pode pegar um usuário direto do DB "usuario_db.nome"
        e criar um schema a partir desse objeto, Ex:
            usuario_schema = UsuarioSchema.model_validate(usuario_db)
    """


class PedidoSchema(BaseModel):
    usuario: int

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True
        