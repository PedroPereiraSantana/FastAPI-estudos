from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
#orm = Object-Relational Mapping, ou seja, Mapeamento de Objeto-Relacional
from sqlalchemy_utils.types import ChoiceType


#cria a conexão do banco
db = create_engine("sqlite:///banco.db")

#cria a base do banco de dados
Base = declarative_base()

#criar as classes/tabelas do banco
#classes iguais a do POO, com funções que se chamam metodos 

#Classe usuário para ter um molde da crianção da tabela para reutilizar sempre que chamada
class Usuario(Base):
    #Cria o nome da tabela
    __tablename__ = "usuarios"

    #Cria as colunas da tabela
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    #a função com __init__ faz com que para criar as informações na tabela é necessário ter essas informações, por isso ID não está ai, porque é definido automaticamente, não pelo usuário
    def __init__(self, nome, email, senha, ativo = True, admin = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

#pedido
class Pedido(Base):
    __tablename__ = "pedidos"

    #Criando os status que podem ser atribuidos ao pedido (precisa intalar e importar a biblioteca sqlalchemy_utils)
    STATUS_PEDIDOS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO")
    )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) #Está puxando a tupla de STATUS_PEDIDO declarado mais acima, o valor da coluna não pode ser outro além do definidos
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco

#itensPedido
class ItemPedido(Base):
    __tablename__ = "itens_pedidos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quatidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido


#executa a criação dos metadados do seu banco (cria efetivamente o banco de dados)

