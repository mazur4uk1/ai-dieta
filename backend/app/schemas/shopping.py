from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .shopping import ShoppingItemResponse


class ShoppingListBase(BaseModel):
    name: str


class ShoppingListCreate(ShoppingListBase):
    pass


class ShoppingListUpdate(ShoppingListBase):
    pass


class ShoppingItemBase(BaseModel):
    item_name: str
    quantity: Optional[str] = None


class ShoppingItemCreate(ShoppingItemBase):
    pass


class ShoppingItemUpdate(ShoppingItemBase):
    is_completed: Optional[bool] = None


class ShoppingItemResponse(ShoppingItemBase):
    id: int
    is_completed: bool

    class Config:
        from_attributes = True


class ShoppingListResponse(ShoppingListBase):
    id: int
    user_id: int
    created_at: datetime
    items: List[ShoppingItemResponse]

    class Config:
        from_attributes = True