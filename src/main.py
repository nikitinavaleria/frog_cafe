from fastapi import FastAPI
from src.auth import router as auth_router
from src.menu import router as menu_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Frog Cafe API is running!"}

app.include_router(auth_router)
app.include_router(menu_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
