from sqlalchemy import Integer, String, Integer, Column, BigInteger
from database import Base
from uuid import uuid4


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, index=True, autoincrement=True, primary_key=True)
    uuid = Column(String, index=True, unique=True)
    name = Column(String, index=True, unique=True)
    quantity = Column(Integer, index=False)
