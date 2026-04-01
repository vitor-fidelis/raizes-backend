# Raízes do Nordeste - Backend

API desenvolvida em FastAPI para gerenciamento de pedidos, clientes e pagamentos de uma rede de lanchonetes.

## Tecnologias

- FastAPI
- SQLAlchemy
- SQLite
- JWT (autenticação)
- Pydantic

## Funcionalidades

- Cadastro de clientes
- Login com autenticação JWT
- Criação de pedidos
- Adição de itens ao pedido
- Cálculo automático do total
- Finalização de pedido
- Simulação de pagamento

## ▶️ Como rodar

```bash
pip install -r requirements.txt
uvicorn main:app --reload