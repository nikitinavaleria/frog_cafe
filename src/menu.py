from fastapi import APIRouter
from src.db import get_db_connection
from src.schemas import MenuItem

router = APIRouter(prefix="/api/menu", tags=["menu"])

@router.get("/", response_model=list[MenuItem])
def get_menu():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM frog_cafe.menu ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
