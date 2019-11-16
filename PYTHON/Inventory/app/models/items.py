from pydantic import BaseModel, Schema
from typing import List
from pydantic.types import UUID4, PositiveInt
import sys
from db.items import Item as ItemDb
from sqlalchemy.orm import Session


class Item(BaseModel):
    id: int = Schema(None, title="id", le=99999999, ge=1)
    name: str = Schema(..., title="name", min_length=1, max_length=256)
    uuid: str = Schema(None, title="unique id", max_length=256)
    quantity: PositiveInt = Schema(
        title="quantity", le=sys.maxsize, default=0)

    # maps to ORM objects
    class Config:
        orm_mode = True
        anystr_strip_whitespace = True
        # arbitrary_types_allowed = True
        #keep_untouched = True

# class ItemsList(BaseModel):
#     items: List[Item] = Schema(default=[])


def get_all_items(db: Session) -> List[ItemDb]:
    return db.query(ItemDb).all()


def get_items_by_name(db: Session, name: str) -> List[ItemDb]:
    return db.query(ItemDb).filter(ItemDb.name == name).first()


def get_items_by_name_and_uuid(db: Session, name: str, uuid: UUID4) -> List[ItemDb]:
    return db.query(ItemDb).filter(ItemDb.name == name).filter(ItemDb.uuid == uuid).first()


def update_item_by_id(db: Session, id: int, quantity: PositiveInt) -> ItemDb:
    try:
        db.begin()
        item = db.query(ItemDb).filter_by(id=id).first()
        item.quantity = quantity
        db.commit()
    except Exception as e:
        db.rollback
        return 0
    return item
