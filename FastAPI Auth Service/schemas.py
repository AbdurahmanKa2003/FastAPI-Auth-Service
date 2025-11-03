from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    email: str
    first_name: str
    
class UserCreate(UserBase):
    password: str
    password_confirm: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    email: Optional[str] = None
    new_password: Optional[str] = None
    
class UserInDB(UserBase):
    id: int
    hashed_password: str
    role: str = "USER"
    status: str = "ACTIVE"

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class TokenRefresh(BaseModel):
    refresh_token: str
    
class PermissionSchema(BaseModel):
    role_name: str
    resource_name: str
    action_name: str
    
class SuccessMessage(BaseModel):
    detail: str