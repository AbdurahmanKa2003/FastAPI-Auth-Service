🛡️ FastAPI Authentication & Authorization System
A comprehensive demonstration of a full-featured Authentication (AuthN) and Authorization (AuthZ) system built with FastAPI. This system implements JSON Web Tokens (JWT) for user identification and a flexible Role-Based Access Control (RBAC) model for resource access management.

🎯 Goals & Architecture
The primary objective of this project is to develop a custom backend system that fully implements user management and access control functionality.

1. Authorization Schema (RBAC)
The system is based on the Role → Resource → Action model, providing high flexibility:

Component	Example	Description
Role	ADMIN, MANAGER, USER	User groups defining permission sets
Resource	PROJECT, TASK, PERMISSIONS	System objects requiring access control
Action	READ, CREATE, UPDATE, DELETE	Operation types that can be performed on resources
Protection	Depends(check_permission("PROJECT", "CREATE"))	Routes protected by dependencies that verify user permissions
2. Project Structure
text
FastAPI Auth Service/
├── auth/
│   ├── auth_router.py          # Routes: /register, /login, /me, /logout
│   └── auth_service.py         # Business logic: hashing, Mock-DB, get_current_user
├── permissions/
│   ├── permission_data.py      # Data sets: roles, resources, access rules (PERMISSIONS)
│   └── permission_middleware.py # Dependency check_permission
├── schemas.py                  # Pydantic schemas for data, tokens, responses
├── security.py                 # JWT and bcrypt utility functions
└── main.py                     # Entry point, FastAPI initialization, Admin API, Mock API
⚙️ Setup & Installation
This project requires Python 3.11+.

1. Install Dependencies
Make sure you're in a virtual environment and install the required packages:

bash
pip install fastapi uvicorn pydantic python-jose[cryptography] bcrypt
2. Run the Server
Start the application with auto-reload:

bash
uvicorn main:app --reload
The server will be available at: http://127.0.0.1:8000

🧪 API Testing
Use the built-in Swagger UI for interactive testing: http://127.0.0.1:8000/docs

1. Test Accounts
The following test accounts are created by default in auth_service.py:

Email	Password	Role	Description
admin@app.com	adminpass	ADMIN	Full permissions, can manage access rules
manager@app.com	managerpass	MANAGER	Limited permissions
2. Testing Sequence (Scenario)
Follow these steps to test the complete functionality:

Login: Execute POST /api/v1/auth/login with admin@app.com/adminpass. Copy the received Access Token.

Authorization: Click the Authorize button in Swagger UI and paste the token in the field.

Identity Verification: Execute GET /api/v1/auth/me. Should return the Admin profile (200 OK).

Admin API Test: Execute GET /api/v1/admin/permissions. Should return all access rules (200 OK).

Testing 403 (Forbidden):

Get a token for MANAGER (manager@app.com)

With the Manager token, attempt to execute POST /api/v1/projects. Should receive 403 Forbidden.

Soft Delete: Register a new test user and execute DELETE /api/v1/auth/me with their token. Then verify they can no longer execute POST /api/v1/auth/login (should receive 401 Unauthorized).

📚 API Endpoints
Authentication Routes (/api/v1/auth)
POST /register - User registration

POST /login - User login

GET /me - Get current user profile

DELETE /me - Soft delete current user

POST /logout - User logout

Admin Routes (/api/v1/admin)
GET /permissions - View all permission rules (Admin only)

Protected Routes (/api/v1)
GET /projects - Get projects (requires PROJECT:READ)

POST /projects - Create project (requires PROJECT:CREATE)

GET /tasks - Get tasks (requires TASK:READ)

🔒 Security Features
JWT Tokens for stateless authentication

BCrypt for password hashing

RBAC with fine-grained permissions

Route protection with dependency injection

Soft delete functionality

Token blacklisting for logout

🚀 Development
The system is designed to be easily extensible. You can:

Add new resources and actions in permission_data.py

Create new roles with custom permission sets

Extend the user model with additional fields

Integrate with real databases (currently uses mock data)
