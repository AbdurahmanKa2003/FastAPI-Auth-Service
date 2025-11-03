from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from auth.auth_router import auth_router # ИЗМЕНЕНИЕ: get_current_user УДАЛЕН
from permissions.permission_middleware import check_permission
from schemas import UserInDB, PermissionSchema, SuccessMessage
from permissions.permission_data import PERMISSIONS, RESOURCES, ACTIONS, ROLES
from typing import List, Tuple, Dict, Any
from auth.auth_service import get_current_user 

app = FastAPI(title="Auth/Auth System Demo")

app.include_router(auth_router, prefix="/api/v1")


mock_router = APIRouter(prefix="/api/v1", tags=["Business Resources"])

@mock_router.get("/projects", dependencies=[Depends(check_permission("PROJECT", "READ"))])
def get_projects():
    return [{"id": 1, "name": "Project Alpha", "status": "Active"}]

@mock_router.post("/projects", dependencies=[Depends(check_permission("PROJECT", "CREATE"))])
def create_project():
    return {"id": 10, "name": "New Project", "detail": "Project created successfully"}

@mock_router.get("/tasks", dependencies=[Depends(check_permission("TASK", "READ"))])
def get_tasks():
    return [{"id": 101, "title": "Task 1", "priority": "High"}]

@mock_router.put("/tasks/{task_id}", dependencies=[Depends(check_permission("TASK", "UPDATE"))])
def update_task(task_id: int):
    return {"id": task_id, "title": "Updated Task", "detail": "Task updated successfully"}
    
app.include_router(mock_router)


admin_router = APIRouter(prefix="/api/v1/admin", tags=["Admin Permissions"])

def check_admin_role(current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only ADMIN can access this resource")
    return current_user

@admin_router.get("/permissions", dependencies=[Depends(check_admin_role), Depends(check_permission("PERMISSIONS", "READ"))])
def list_permissions() -> List[Dict[str, str]]:
    return [
        {"role": r, "resource": res, "action": a} 
        for r, res, a in PERMISSIONS
    ]

@admin_router.post("/permissions", dependencies=[Depends(check_admin_role), Depends(check_permission("PERMISSIONS", "CREATE"))], response_model=SuccessMessage)
def add_permission(perm: PermissionSchema):
    new_perm = (perm.role_name, perm.resource_name, perm.action_name)
    
    if perm.role_name not in ROLES or perm.resource_name not in RESOURCES or perm.action_name not in ACTIONS:
        raise HTTPException(status_code=400, detail="Invalid Role, Resource, or Action name")
        
    if new_perm in PERMISSIONS:
        return {"detail": "Permission already exists"}
        
    PERMISSIONS.add(new_perm)
    return {"detail": "Permission added successfully"}

@admin_router.delete("/permissions", dependencies=[Depends(check_admin_role), Depends(check_permission("PERMISSIONS", "DELETE"))], response_model=SuccessMessage)
def delete_permission(perm: PermissionSchema):
    old_perm = (perm.role_name, perm.resource_name, perm.action_name)
    
    if old_perm not in PERMISSIONS:
        raise HTTPException(status_code=404, detail="Permission not found")
        
    PERMISSIONS.remove(old_perm)
    return {"detail": "Permission deleted successfully"}

app.include_router(admin_router)