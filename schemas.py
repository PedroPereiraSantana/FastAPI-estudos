from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome:str
    email:str
    senha:str
    ativo: Optional[bool]
    admin: Optional[bool]
    #isso faz com que invés de enviarmos 5 parametros para uma função de criar usuário, mandamos apenas um objeto que tem todos essas informações dentro dele
    #isso deixa o código mais patrinizado

    class Config:
        from_attributes = True
    #por causa do ORM com essa classe você consegue definir um tipo Obrigatório a suas instancias dessa classe 
    #atribuindo ao atribuido da classe o UsuarioSchema -> UsuarioSchema.nome (agora o nome é obrigado a seguir a tipagem)

class PedidoSchema(BaseModel):
    usuario: int

    class Config:
        from_attributes = True