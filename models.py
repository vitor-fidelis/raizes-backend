# Importação dos tipos de dados e ferramentas do SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from database import Base


# Entidade que representa o cliente do sistema
class Cliente(Base):
    __tablename__ = "clientes"

    # Identificador único do cliente
    id_cliente = Column(Integer, primary_key=True)
    
    # dados pessoais (necessários para identificação e contato)
    nome = Column(String)
    cpf = Column(String)
    email = Column(String)

    # Senha armazenada em formato hash (para segurança, por isso não o texto puro)
    senha = Column(String)


# Entidade que representa um pedido realizado por um cliente
class Pedido(Base):
    __tablename__ = "pedidos"

    # Identificador único do pedido
    id_pedido = Column(Integer, primary_key=True)

    # Relacionamento com cliente (um cliente pode ter vários pedidos)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    
    # Status do pedido (ex: "aberto", "finalizado", "pago")
    status = Column(String)

    # Valor total acumulado do pedido
    total = Column(Float)

# Entidade que representa produtos disponíveis no sistema
class Produto(Base):
    __tablename__ = "produtos"

    # Identificador do produto
    id_produto = Column(Integer, primary_key=True)

    # Nome e preço do produto 
    nome = Column(String)
    preco = Column(Float)

# Representa os itens dentro de um pedido, associando produtos a pedidos específicos
class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    # Identificador único do item do pedido
    id = Column(Integer, primary_key=True)

    # Relacionamento com pedido (um item pertence a um pedido)
    id_pedido = Column(Integer, ForeignKey("pedidos.id_pedido"))

    # Relacionamento com produto (um item está associado a um produto)
    id_produto = Column(Integer, ForeignKey("produtos.id_produto"))

    # Quantidade do produto no item do pedido
    quantidade = Column(Integer)
    
    # Preço do produto no momento do pedido
    preco = Column(Float)