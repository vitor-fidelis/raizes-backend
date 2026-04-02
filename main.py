"""
API de gerenciamento de pedidos desenvolvida com FastAPI.

Implementa autenticação JWT, controle de acesso por usuário
e fluxo completo de pedidos (criação, itens, finalização e pagamento).
"""

# Inicialização da API e importaçao das dependencias
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas
from auth import (
    hash_senha,
    verificar_senha,
    criar_token,
    verificar_token
)

# Criação de tabelas no banco (para desenvolvimento, em produção usar migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependencia para controle de sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/clientes")
def criar_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):

    # Cria cliente armazenando senha com hash (bcrypt) e truncando para 72 caracteres (limitação do bcrypt)
    novo = models.Cliente(
        nome=cliente.nome,
        cpf=cliente.cpf,
        email=cliente.email,
        senha=hash_senha(cliente.senha)
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {"msg": "Cliente criado"}

@app.get("/clientes")
def listar_clientes(
    user=Depends(verificar_token),
    db: Session = Depends(get_db)
):
    # Retorna lista de clientes 
    return db.query(models.Cliente).all()

@app.post("/login")

# Busca cliente pelo email
def login(dados: schemas.Login, db: Session = Depends(get_db)):

    cliente = db.query(models.Cliente).filter(
        models.Cliente.email == dados.email
    ).first()

    if not cliente:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    # Verifica senha usando hash(bcrypt)
    if not verificar_senha(dados.senha, cliente.senha):
        raise HTTPException(status_code=400, detail="Senha inválida")

    # Gera token JWT contendo identificação do usuário (email nesse caso)
    token = criar_token({"sub": cliente.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/pedidos")
def listar_pedidos(
    user=Depends(verificar_token),
    db: Session = Depends(get_db)
):
    return db.query(models.Pedido).all() 


@app.post("/produtos")
def criar_produto(
    produto: schemas.ProdutoCreate,
    user=Depends(verificar_token),
    db: Session = Depends(get_db)
):
    # validações simples
    if produto.preco is None or produto.preco <= 0:
        raise HTTPException(status_code=400, detail="Preço deve ser maior que zero")

    novo = models.Produto(
        nome=produto.nome,
        preco=produto.preco
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {"msg": "Produto criado", "id_produto": novo.id_produto}


@app.get("/produtos")
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(models.Produto).all()

@app.post("/pedidos")
def criar_pedido(
    pedido: schemas.PedidoCreate,
    user=Depends(verificar_token),
    db: Session = Depends(get_db)
):
    # Recupera usuário autenticado via token (JWT)
    email = user.get("sub")
    cliente = db.query(models.Cliente).filter(models.Cliente.email == email).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Cria pedido inicial com total zero (itens serão adicionados depois)
    novo = models.Pedido(
        id_cliente=cliente.id_cliente,
        status="aberto",
        total=0.0,
        canal=pedido.canal
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {"msg": "Pedido criado", "id_pedido": novo.id_pedido}

@app.post("/pedidos/{id_pedido}/itens")
def adicionar_item(         
    id_pedido: int,
    item: schemas.ItemCreate,
    user=Depends(verificar_token),
    db: Session = Depends(get_db)
):
    # Garante que o pedido pertence ao usuário autenticado
    email = user.get("sub")
    cliente = db.query(models.Cliente).filter(models.Cliente.email == email).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    pedido = db.query(models.Pedido).filter(models.Pedido.id_pedido == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if pedido.id_cliente != cliente.id_cliente:
        raise HTTPException(status_code=403, detail="Pedido não pertence ao usuário")

    if pedido.status != "aberto":
        raise HTTPException(status_code=400, detail="Somente pedidos abertos podem receber itens")

    produto = db.query(models.Produto).filter(models.Produto.id_produto == item.id_produto).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    preco_unitario = produto.preco
    item_total = preco_unitario * item.quantidade

    # Cria item vinculado ao pedido
    novo_item = models.ItemPedido(
        id_pedido=id_pedido,
        id_produto=item.id_produto,
        quantidade=item.quantidade,
        preco=preco_unitario
    )

    db.add(novo_item)

    # Atualiza total do pedido
    pedido.total = (pedido.total or 0) + item_total

    db.commit()
    db.refresh(novo_item)
    db.refresh(pedido)

    return {"msg": "Item adicionado", "item": schemas.ItemResponse.model_validate(novo_item), "total_pedido": pedido.total}

@app.post("/pedidos/{id_pedido}/finalizar")
def finalizar_pedido( 
    id_pedido: int,
    user=Depends(verificar_token),
    db: Session = Depends(get_db)
):
    # Apenas o dono do pedido pode finalizar
    email = user.get("sub")
    cliente = db.query(models.Cliente).filter(models.Cliente.email == email).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    pedido = db.query(models.Pedido).filter(models.Pedido.id_pedido == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if pedido.id_cliente != cliente.id_cliente:
        raise HTTPException(status_code=403, detail="Pedido não pertence ao usuário")

    if pedido.status != "aberto":
        raise HTTPException(status_code=400, detail="Pedido já finalizado")

    # Marca como finalizado (pronto para pagamento)
    pedido.status = "finalizado"
    db.commit()
    db.refresh(pedido)

    return {"msg": "Pedido finalizado", "id_pedido": pedido.id_pedido, "total": pedido.total}

@app.post("/pagamentos/{id_pedido}")
def pagar_pedido(
    id_pedido: int,
    user=Depends(verificar_token),
    db: Session = Depends(get_db)
):
    pedido = db.query(models.Pedido).filter(
        models.Pedido.id_pedido == id_pedido
    ).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if pedido.status != "finalizado":
        raise HTTPException(status_code=400, detail="Pedido não está pronto para pagamento")

    # simulação
    aprovado = True

    if aprovado:
        pedido.status = "pago"
    else:
        pedido.status = "recusado"

    db.commit()

    return {
        "id_pedido": id_pedido,
        "status": pedido.status
    }