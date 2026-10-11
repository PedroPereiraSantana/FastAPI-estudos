from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from jose import jwt, JWTError

def pegar_sessao():
#uma função para abrir o banco de dados sempre que for preciso para criar algo, deletar ou apenas consultar
    try:
    #usando essa estrutura de teste podemos verificar se a função funcinou como deveria ou não e fazer algo quanto a isso
        Session = sessionmaker(bind=db)
        #Função sessionmaker server para abrir uma sessão, o bind fala onde vai pegar essa sessão, no caso na variavel DB que está no models.py armazenando o banco
        session = Session()
        yield session
        #o yield funciona como um return, mas o return finaliza a sessão quando é executado, o yield não, então ele vai para o finally
    finally:
    #o finally vai ser executado sempre no final, caso o try der errado ou não o finally sempre vai executar
        session.close()
        #dessa forma finalizamos a sessão de tentativa de conectar no banco de dados através do metodo .close()




def verificar_token(token:str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    """
    a função recebe um token do tipo string , essa dependecia OAuth2 serve para pegar o token do cabeçalho
    e o session é para começar uma sessão no banco de dados
    """
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        """
        O jwt.decode serve para pegar o token e tirar as credenciais que estão nesse token, nesse caso ID e data de expiração do token,
        as informações só conseguem ser tiradas do token por causa da SECRET_KEY e ALGORITHM que falam as configurações usadas para criar
        o token de forma criptografada
        """
        id_usuario = int(dic_info.get("sub"))
        """
        aqui ele da várivel que está as credenciais descriptografadas apenas o ID do usuário
        """

    except JWTError:
    #uma excessão para erro usando com exemplo de erro um erro direto da biblioteca do JWT
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")
    

    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    """
    Aqui é iniciaddo uma sessão com a tabela Usuario, filtrando dentro da tabela o ID do usuário que foi extraido do token anteriormente
    e procurando se ele existe dentro do banco
    """

    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Invalido")

    return usuario