from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from db import get_db_connection
from schemas import LoginRequest, TokenResponse

router = APIRouter()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 30))

@router.post("/auth/login", response_model=TokenResponse)
def login(request: LoginRequest):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM frog_cafe.Users WHERE Name = %s AND Pass = %s",
        (request.username, request.password)
    )
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "sub": user["name"],
        "user_id": user["id"],
        "role_id": user["role_id"],
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}
