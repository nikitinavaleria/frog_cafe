from fastapi import APIRouter, Depends, HTTPException
from src.db import get_db_connection
from src.schemas import TVOrder
from src.dependencies import get_current_user

router = APIRouter(prefix="/api/tv", tags=["tv"])

@router.get("/orders", response_model=list[TVOrder])
def get_tv_orders(current_user=Depends(get_current_user)):
    if current_user["role_id"] != 2:
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT o.id, o.user_id, o.toad_id, s.name AS status_name, o.created_at
        FROM frog_cafe.orders o
        JOIN frog_cafe.order_statuses s ON o.status_id = s.id
        ORDER BY o.created_at DESC
    """)

    orders = cur.fetchall()
    cur.close()
    conn.close()
    return orders
