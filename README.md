# 🛡️ FastAPI Authentication & Authorization System

A comprehensive demonstration of a full-featured **Authentication (AuthN)** and **Authorization (AuthZ)** system built with **FastAPI**.  
This system implements **JSON Web Tokens (JWT)** for user identification and a flexible **Role-Based Access Control (RBAC)** model for managing access to resources.

---

## 🎯 Goals & Architecture

The primary goal of this project is to develop a **custom backend system** that fully implements **user management** and **access control** functionality.

---

### 🔐 Authorization Schema (RBAC)

The system is based on the **Role → Resource → Action** model, providing high flexibility:

| Component | Example | Description |
|------------|----------|-------------|
| **Role** | ADMIN, MANAGER, USER | User groups defining permission sets |
| **Resource** | PROJECT, TASK, PERMISSIONS | System objects requiring access control |
| **Action** | READ, CREATE, UPDATE, DELETE | Operation types that can be performed on resources |



⚙️ Setup & Installation

This project requires Python 3.11+

1️⃣ Install Dependencies

Make sure you’re inside a virtual environment and install required packages

Start the application in auto-reload mode:uvicorn main:app --reload

🧪 API Testing

Use the built-in Swagger UI for interactive testing:
🔗 http://127.0.0.1:8000/docs￼

🧩 Testing Sequence (Scenario)

1️⃣ Login:
Execute POST /api/v1/auth/login with admin@app.com/adminpass.
Copy the received Access Token.

2️⃣ Authorize:
Click Authorize in Swagger UI and paste the token.

3️⃣ Identity Verification:
Execute GET /api/v1/auth/me — should return Admin profile (200 OK).

4️⃣ Admin API Test:
Execute GET /api/v1/admin/permissions — should return all permission rules (200 OK).

5️⃣ 403 Forbidden Test:
Get token for manager@app.com.


📚 API Endpoints

🔑 Authentication Routes (/api/v1/auth)
	•	POST /register — User registration
	•	POST /login — User login
	•	GET /me — Get current user profile
	•	DELETE /me — Soft delete current user
	•	POST /logout — User logout

⚙️ Admin Routes (/api/v1/admin)
	•	GET /permissions — View all permission rules (Admin only)

🧱 Protected Routes (/api/v1)
	•	GET /projects — Get projects (requires PROJECT:READ)
	•	POST /projects — Create project (requires PROJECT:CREATE)
	•	GET /tasks — Get tasks (requires TASK:READ)

⸻

🔒 Security Features
	•	JWT Tokens for stateless authentication
	•	BCrypt for password hashing
	•	RBAC with fine-grained permissions
	•	Route protection with dependency injection
	•	Soft delete functionality
	•	Token blacklisting for logout

Then execute POST /api/v1/projects — should return 403 Forbidden.

6️⃣ Soft Delete:
Register a new user → execute DELETE /api/v1/auth/me using their token.
Then try POST /api/v1/auth/login again — should return 401 Unauthorized.
