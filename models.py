from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

#cria a conexão do banco
db = create_engine("sqlite:///banco.db")

#cria a base do banco de dados
Base = declarative_base()

#criar as classes/tabelas do banco
#usuario
#pedido
#itensPedido

#executa a criação dos metadados do seu banco (cria efetivamente o banco de dados)

