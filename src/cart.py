from fastapi import APIRouter, Depends, HTTPException
from src.db import get_db_connection
from src.dependencies import get_current_user
from src.schemas import CartItem, CartAddMultiple

router = APIRouter(prefix="/api/cart", tags=["cart"])

@router.get("/{order_id}", response_model=list[CartItem])
def get_cart(order_id: int, current_user=Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor()

    # Проверка: владелец или админ?
    cur.execute("SELECT user_id FROM frog_cafe.orders WHERE id = %s;", (order_id,))
    order = cur.fetchone()

    if not order:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Заказ не найден")

    is_admin = current_user["role_id"] == 0
    is_owner = order["user_id"] == current_user["user_id"]

    if not (is_admin or is_owner):
        cur.close()
        conn.close()
        raise HTTPException(status_code=403, detail="Нет доступа к заказу")

    # Получаем блюда из корзины
    cur.execute("""
        SELECT m.id, m.dish_name, m.image, m.description, m.is_available
        FROM frog_cafe.cart c
        JOIN frog_cafe.menu m ON c.menu_item = m.id
        WHERE c.order_id = %s
    """, (order_id,))

    items = cur.fetchall()
    cur.close()
    conn.close()
    return items




@router.post("/{order_id}", status_code=201)
def add_multiple_to_cart(order_id: int, items: CartAddMultiple, current_user=Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor()

    # Проверка, чей заказ
    cur.execute("SELECT user_id FROM frog_cafe.orders WHERE id = %s", (order_id,))
    order = cur.fetchone()

    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    is_admin = current_user["role_id"] == 0
    is_owner = order["user_id"] == current_user["user_id"]

    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Нет доступа к заказу")

    # Добавим блюда в заказ
    values = [(order_id, menu_id) for menu_id in items.menu_items]

    cur.executemany(
        "INSERT INTO frog_cafe.cart (order_id, menu_item) VALUES (%s, %s);",
        values
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"message": f"{len(values)} блюд добавлено в заказ"}