from fastapi import APIRouter, Depends, HTTPException, status
from src.db import get_db_connection
from src.schemas import Order, OrderCreate, OrderStatusUpdate
from src.dependencies import get_current_user, require_role


router = APIRouter(prefix="/api/orders", tags=["orders"])

# GET /api/orders — только админ
@router.get("/", response_model=list[Order], dependencies=[Depends(require_role([0]))])
def get_orders():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM frog_cafe.orders ORDER BY created_at DESC;")
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return orders

# POST /api/orders — создание заказа с автоматической жабой
@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(current_user=Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor()

    # Найдём свободную жабу
    cur.execute("SELECT id FROM frog_cafe.toads WHERE is_taken = false LIMIT 1;")
    toad = cur.fetchone()

    if not toad:
        raise HTTPException(status_code=400, detail="Нет свободных жаб 😢")

    toad_id = toad["id"]

    # Пометим жабу как занятую
    cur.execute("UPDATE frog_cafe.toads SET is_taken = true WHERE id = %s;", (toad_id,))

    # Получим id первого статуса (например, 'Создан')
    cur.execute("SELECT id FROM frog_cafe.order_statuses ORDER BY id LIMIT 1;")
    status_row = cur.fetchone()
    if not status_row:
        raise HTTPException(status_code=400, detail="Нет статусов заказов")

    status_id = status_row["id"]

    # Создадим заказ
    cur.execute("""
        INSERT INTO frog_cafe.orders (user_id, toad_id, status_id)
        VALUES (%s, %s, %s)
        RETURNING id, user_id, toad_id, status_id, created_at;
    """, (current_user["user_id"], toad_id, status_id))

    new_order = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_order

# GET /api/orders/{id}
@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, current_user=Depends(get_current_user)):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM frog_cafe.orders WHERE id = %s;", (order_id,))
    order = cur.fetchone()
    cur.close()
    conn.close()

    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    # Только админ или владелец заказа
    if current_user["role_id"] != 0 and order["user_id"] != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    return order

# PUT /api/orders/{id}/status
@router.put("/{order_id}/status", response_model=Order, dependencies=[Depends(require_role([0]))])
def update_order_status(order_id: int, update: OrderStatusUpdate):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE frog_cafe.orders
        SET status_id = %s
        WHERE id = %s
        RETURNING id, user_id, toad_id, status_id, created_at;
    """, (update.status_id, order_id))

    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    return updated
