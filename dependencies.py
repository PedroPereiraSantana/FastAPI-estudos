from models import db
from sqlalchemy.orm import sessionmaker

def pegar_sessao():
    try:
    #usando essa estrutura de teste podemos verificar se a função funcinou como deveria ou não e fazer algo quanto a isso
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
        #o yield funciona como um return, mas o return finaliza a sessão quando é executado, o yield não, então ele vai para o finally
    finally:
    #o finally vai ser executado sempre no final, caso o try der errado ou não o finally sempre vai executar
        session.close()
        #dessa forma finalizamos a sessão de tentativa de conectar no banco de dados através do metodo .close()