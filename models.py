from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    email = Column(String)
    senha = Column(String)

class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    status = Column(String)
    total = Column(Float)

class Produto(Base):
    __tablename__ = "produtos"

    id_produto = Column(Integer, primary_key=True)
    nome = Column(String)
    preco = Column(Float)

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True)
    id_pedido = Column(Integer, ForeignKey("pedidos.id_pedido"))
    id_produto = Column(Integer, ForeignKey("produtos.id_produto"))
    quantidade = Column(Integer)
    preco = Column(Float)