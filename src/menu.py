from fastapi import APIRouter, Depends, HTTPException, status
from src.db import get_db_connection
from src.schemas import MenuItem, MenuItemCreate
from src.dependencies import require_role


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




@router.post("/", response_model=MenuItem, dependencies=[Depends(require_role([0]))])
def create_menu_item(item: MenuItemCreate):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO frog_cafe.menu 
        (dish_name, image, is_available, description, category, quantity_left)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, dish_name, image, is_available, description, category, quantity_left;
    """, (
        item.dish_name,
        item.image,
        item.is_available,
        item.description,
        item.category,
        item.quantity_left
    ))

    new_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_item




@router.get("/{item_id}", response_model=MenuItem)
def get_menu_item(item_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM frog_cafe.menu WHERE id = %s", (item_id,))
    item = cur.fetchone()

    cur.close()
    conn.close()

    if not item:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")

    return item





@router.put("/{item_id}", response_model=MenuItem, dependencies=[Depends(require_role([0]))])
def update_menu_item(item_id: int, item: MenuItemCreate):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE frog_cafe.menu
        SET dish_name = %s,
            image = %s,
            is_available = %s,
            description = %s
        WHERE id = %s
        RETURNING id, dish_name, image, is_available, description;
    """, (item.dish_name, item.image, item.is_available, item.description, item_id))

    updated_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated_item:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")

    return updated_item



@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role([0]))])
def delete_menu_item(item_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM frog_cafe.menu WHERE id = %s RETURNING id;", (item_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")

    return