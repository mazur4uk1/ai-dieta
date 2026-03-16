from sqlalchemy.orm import Session
from typing import List
from app.models.shopping import ShoppingList, ShoppingItem
from app.schemas.shopping import ShoppingListCreate, ShoppingListUpdate, ShoppingItemCreate, ShoppingItemUpdate


class ShoppingService:
    @staticmethod
    def create_shopping_list(db: Session, user_id: int, list_data: ShoppingListCreate, items: List[ShoppingItemCreate]) -> ShoppingList:
        shopping_list = ShoppingList(user_id=user_id, **list_data.model_dump())
        db.add(shopping_list)
        db.flush()
        for item_data in items:
            item = ShoppingItem(list_id=shopping_list.id, **item_data.model_dump())
            db.add(item)
        db.commit()
        db.refresh(shopping_list)
        return shopping_list

    @staticmethod
    def get_user_shopping_lists(db: Session, user_id: int) -> List[ShoppingList]:
        return db.query(ShoppingList).filter(ShoppingList.user_id == user_id).all()

    @staticmethod
    def update_shopping_list(db: Session, list_id: int, list_update: ShoppingListUpdate) -> ShoppingList:
        update_data = list_update.model_dump(exclude_unset=True)
        db.query(ShoppingList).filter(ShoppingList.id == list_id).update(update_data)
        db.commit()
        shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
        return shopping_list

    @staticmethod
    def add_item_to_list(db: Session, list_id: int, item_data: ShoppingItemCreate) -> ShoppingItem:
        item = ShoppingItem(list_id=list_id, **item_data.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update_item(db: Session, item_id: int, item_update: ShoppingItemUpdate) -> ShoppingItem:
        update_data = item_update.model_dump(exclude_unset=True)
        db.query(ShoppingItem).filter(ShoppingItem.id == item_id).update(update_data)
        db.commit()
        item = db.query(ShoppingItem).filter(ShoppingItem.id == item_id).first()
        return item