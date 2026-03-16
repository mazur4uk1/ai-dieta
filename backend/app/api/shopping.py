from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.auth import get_current_user
from app.core.database import get_db
from app.services.shopping_service import ShoppingService
from app.schemas.shopping import ShoppingListCreate, ShoppingListUpdate, ShoppingListResponse, ShoppingItemCreate, ShoppingItemUpdate, ShoppingItemResponse
from app.models.shopping import ShoppingList, ShoppingItem

router = APIRouter()

@router.post("/", response_model=ShoppingListResponse)
def create_shopping_list(list_data: ShoppingListCreate, items: List[ShoppingItemCreate], current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    shopping_list = ShoppingService.create_shopping_list(db, current_user.id, list_data, items)
    return ShoppingListResponse.model_validate(shopping_list)

@router.get("/", response_model=List[ShoppingListResponse])
def get_shopping_lists(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    lists = ShoppingService.get_user_shopping_lists(db, current_user.id)
    return [ShoppingListResponse.model_validate(lst) for lst in lists]

@router.put("/{list_id}", response_model=ShoppingListResponse)
def update_shopping_list(list_id: int, list_update: ShoppingListUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id, ShoppingList.user_id == current_user.id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    updated_list = ShoppingService.update_shopping_list(db, list_id, list_update)
    return ShoppingListResponse.model_validate(updated_list)

@router.delete("/{list_id}")
def delete_shopping_list(list_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id, ShoppingList.user_id == current_user.id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    db.delete(shopping_list)
    db.commit()
    return {"message": "Shopping list deleted"}

@router.post("/{list_id}/items", response_model=ShoppingItemResponse)
def add_item_to_list(list_id: int, item_data: ShoppingItemCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id, ShoppingList.user_id == current_user.id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    item = ShoppingService.add_item_to_list(db, list_id, item_data)
    return ShoppingItemResponse.model_validate(item)

@router.put("/items/{item_id}", response_model=ShoppingItemResponse)
def update_item(item_id: int, item_update: ShoppingItemUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(ShoppingItem).join(ShoppingList).filter(ShoppingItem.id == item_id, ShoppingList.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Shopping item not found")
    updated_item = ShoppingService.update_item(db, item_id, item_update)
    return ShoppingItemResponse.model_validate(updated_item)

@router.delete("/items/{item_id}")
def delete_item(item_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(ShoppingItem).join(ShoppingList).filter(ShoppingItem.id == item_id, ShoppingList.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Shopping item not found")
    db.delete(item)
    db.commit()
    return {"message": "Shopping item deleted"}