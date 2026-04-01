from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from fastapi import Security, HTTPException

SECRET_KEY = "segredo-super-seguro"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_senha(senha: str):
    senha_truncada = senha[:72]
    return pwd_context.hash(senha_truncada)

def verificar_senha(senha: str, hash: str):
    senha_truncada = senha[:72]
    return pwd_context.verify(senha_truncada, hash)

def criar_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

security = HTTPBearer()

def verificar_token(credentials=Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=403, detail="Token inválido")