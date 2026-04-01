from pydantic import BaseModel,ConfigDict

class ClienteCreate(BaseModel):
    nome: str
    cpf: str
    email: str
    senha: str

class ClienteResponse(BaseModel):
    id_cliente: int
    nome: str

    model_config = ConfigDict(from_attributes=True)

class Login(BaseModel):
    email: str
    senha: str


class PedidoCreate(BaseModel):
    # Cria um pedido vazio para o cliente autenticado
    pass


class ItemCreate(BaseModel):
    id_produto: int
    quantidade: int


class ItemResponse(BaseModel):
    id: int
    id_pedido: int
    id_produto: int
    quantidade: int
    preco: float

    model_config = ConfigDict(from_attributes=True)


class PedidoResponse(BaseModel):
    id_pedido: int
    id_cliente: int
    status: str
    total: float

    model_config = ConfigDict(from_attributes=True)


class ProdutoCreate(BaseModel):
    nome: str
    preco: float


class ProdutoResponse(BaseModel):
    id_produto: int
    nome: str
    preco: float

    model_config = ConfigDict(from_attributes=True)