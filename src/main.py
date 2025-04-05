from fastapi import FastAPI

from src.auth import router as auth_router
from src.menu import router as menu_router
from src.users import router as users_router
from src.roles import router as roles_router
from src.order_statuses import router as status_router
from src.toads import router as toads_router
from src.orders import router as orders_router
from src.cart import router as cart_router
from src.tv import router as tv_router

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app = FastAPI()

app.include_router(auth_router)
app.include_router(menu_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(status_router)
app.include_router(toads_router)
app.include_router(orders_router)
app.include_router(cart_router)
app.include_router(tv_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
