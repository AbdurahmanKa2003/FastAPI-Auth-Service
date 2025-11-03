import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
import bcrypt

SECRET_KEY = "YOUR_SUPER_SECRET_KEY_HERE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7



def verify_password(plain_password: str, hashed_password: str) -> bool:

    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
   
    password_bytes = password.encode('utf-8')
    
 
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    
    return hashed_bytes.decode('utf-8')

def create_jwt_token(data: Dict[str, Any], token_type: str) -> str:
    to_encode = data.copy()
    
    if token_type == "access":
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    elif token_type == "refresh":
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    else:
        raise ValueError("Invalid token type")

    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc), "token_type": token_type})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])