# Manipulação de datas para expiração de token
from datetime import datetime, timedelta

# Biblioteca para criação e validação de JWT
from jose import jwt

# Biblioteca para hash de senha
from passlib.context import CryptContext

# Segurança no FastAPI (captura token no header)
from fastapi.security import HTTPBearer
from fastapi import Security, HTTPException


# Chave secreta usada na assinatura do token JWT
SECRET_KEY = "segredo-super-seguro"

# Algoritmo de criptografia
ALGORITHM = "HS256"

# Tempo de expiração do token (em minutos)
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Configuração do hash de senha com bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Gera hash da senha (armazenamento seguro)
def hash_senha(senha: str):
    # Limita tamanho devido à limitação do bcrypt (72 caracteres)
    senha_truncada = senha[:72]
    return pwd_context.hash(senha_truncada)


# Verifica se senha informada bate com hash armazenado
def verificar_senha(senha: str, hash: str):
    senha_truncada = senha[:72]
    return pwd_context.verify(senha_truncada, hash)


# Cria token JWT com tempo de expiração
def criar_token(data: dict):
    to_encode = data.copy()

    # Define tempo de expiração
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Adiciona expiração ao payload
    to_encode.update({"exp": expire})

    # Gera token assinado
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Define esquema de autenticação via Bearer Token
security = HTTPBearer()


# Valida token JWT recebido nas requisições protegidas
def verificar_token(credentials=Security(security)):
    token = credentials.credentials

    try:
        # Decodifica token e valida assinatura
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Retorna dados do usuário (payload)
        return payload

    except:
        # Caso token inválido ou expirado
        raise HTTPException(status_code=403, detail="Token inválido")