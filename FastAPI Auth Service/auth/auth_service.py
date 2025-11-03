from typing import Dict, List
from schemas import UserInDB, UserCreate, UserLogin, UserUpdate
from schemas import Token, TokenRefresh
from security import get_password_hash, verify_password, create_jwt_token, decode_jwt_token
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer



USERS_DB: Dict[str, UserInDB] = {}
user_id_counter = 1

def create_user_in_db(user: UserCreate) -> UserInDB:
    global user_id_counter
    if user.email in USERS_DB:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    if user.password != user.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password = get_password_hash(user.password)
    
    new_user = UserInDB(
        id=user_id_counter,
        email=user.email,
        first_name=user.first_name,
        hashed_password=hashed_password,
        role="USER", 
        status="ACTIVE"
    )
    
    USERS_DB[user.email] = new_user
    user_id_counter += 1
    return new_user

def get_user_by_email(email: str) -> UserInDB | None:
    return USERS_DB.get(email)

def authenticate_user(user_login: UserLogin) -> UserInDB:
    user = get_user_by_email(user_login.email)
    
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if user.status == "DELETED":
        raise HTTPException(status_code=401, detail="Account is soft-deleted and cannot be used")

    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    return user

def update_user_info(current_user: UserInDB, update_data: UserUpdate) -> UserInDB:
    if update_data.first_name is not None:
        current_user.first_name = update_data.first_name
        
    if update_data.email is not None and update_data.email != current_user.email:
        if update_data.email in USERS_DB:
            raise HTTPException(status_code=400, detail="New email already registered")
        
        del USERS_DB[current_user.email]
        current_user.email = update_data.email
        USERS_DB[current_user.email] = current_user

    if update_data.new_password is not None:
        current_user.hashed_password = get_password_hash(update_data.new_password)
        
    return current_user

def soft_delete_user(current_user: UserInDB):
    current_user.status = "DELETED"
    
admin_hash = get_password_hash("adminpass")
admin_user = UserInDB(
    id=0, email="admin@app.com", first_name="Admin", hashed_password=admin_hash, role="ADMIN", status="ACTIVE"
)
USERS_DB["admin@app.com"] = admin_user

manager_hash = get_password_hash("managerpass")
manager_user = UserInDB(
    id=10, email="manager@app.com", first_name="Manager", hashed_password=manager_hash, role="MANAGER", status="ACTIVE"
)
USERS_DB["manager@app.com"] = manager_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    try:
        payload = decode_jwt_token(token)
        user_email = payload.get("email")
        token_type = payload.get("token_type")
        
        if user_email is None or token_type != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or token type")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        
    user = get_user_by_email(user_email)
    if user is None or user.status == "DELETED":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or deleted")
        
    return user