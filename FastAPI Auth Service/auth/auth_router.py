from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from schemas import UserCreate, UserLogin, UserUpdate, UserInDB, Token, TokenRefresh, SuccessMessage
from security import create_jwt_token
from auth.auth_service import create_user_in_db, authenticate_user, update_user_info, soft_delete_user, get_current_user 

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")





@auth_router.post("/register", response_model=UserInDB)
def register_user(user: UserCreate):
    return create_user_in_db(user)

@auth_router.post("/login", response_model=Token)
def login_for_access_token(user_login: UserLogin):
    user = authenticate_user(user_login)
    access_token = create_jwt_token({"email": user.email, "role": user.role}, "access")
    return {"access_token": access_token}

@auth_router.post("/logout", response_model=SuccessMessage)
def logout_user(current_user: UserInDB = Depends(get_current_user)):
    
    return {"detail": "Successfully logged out"}

@auth_router.post("/refresh", response_model=Token)
def refresh_access_token(token_refresh: TokenRefresh):
    
    from security import decode_jwt_token
    from auth.auth_service import get_user_by_email 

    try:
        payload = decode_jwt_token(token_refresh.refresh_token)
        user_email = payload.get("email")
        token_type = payload.get("token_type")

        if user_email is None or token_type != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
            
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate refresh token")
        
    user = get_user_by_email(user_email)
    if user is None or user.status == "DELETED":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or deleted")

    new_access_token = create_jwt_token({"email": user.email, "role": user.role}, "access")
    return {"access_token": new_access_token}


@auth_router.get("/me", response_model=UserInDB)
def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user

@auth_router.put("/me", response_model=UserInDB)
def update_users_me(update_data: UserUpdate, current_user: UserInDB = Depends(get_current_user)):
    return update_user_info(current_user, update_data)

@auth_router.delete("/me", response_model=SuccessMessage)
def delete_users_me(current_user: UserInDB = Depends(get_current_user)):
    soft_delete_user(current_user)
    return {"detail": "Account soft-deleted. User logged out."}