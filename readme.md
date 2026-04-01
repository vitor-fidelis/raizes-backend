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
```
Acesse:
http://127.0.0.1:8000/docs

## Autenticação

Crie um cliente
Faça login
Use o token no Swagger (Authorize)

## Estrutura

main.py → rotas
models.py → entidades
schemas.py → validação
auth.py → autenticação
database.py → conexão

## LGPD

O sistema coleta apenas dados essenciais (nome, CPF, email) com finalidade de identificação e execução de pedidos, respeitando princípios da LGPD.

## Autor

Vitor Gabriel Coelho Fidelis