from fastapi import HTTPException, status, Depends
from typing import Callable
from auth.auth_router import get_current_user
from schemas import UserInDB
from permissions.permission_data import PERMISSIONS


def check_permission(resource: str, action: str) -> Callable:
    def permission_checker(current_user: UserInDB = Depends(get_current_user)):
        
        
        user_role = current_user.role
        
       
        if (user_role, resource, action) not in PERMISSIONS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Forbidden: Role {user_role} does not have {action} permission on {resource}"
            )
        return True 
        
    return permission_checker