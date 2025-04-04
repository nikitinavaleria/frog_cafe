from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

# Зависимость для получения текущего пользователя из токена
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        name = payload.get("sub")
        role_id = payload.get("role_id")

        if user_id is None or role_id is None:
            raise HTTPException(status_code=401, detail="Invalid token structure")

        return {
            "user_id": user_id,
            "name": name,
            "role_id": role_id
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Проверка доступа по ролям
def require_role(allowed_roles: list[int]):
    def checker(current_user: dict = Depends(get_current_user)):
        if current_user["role_id"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return current_user
    return checker
