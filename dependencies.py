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
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))

    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")

    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Invalido")

    return usuario