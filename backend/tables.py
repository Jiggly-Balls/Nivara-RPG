from typing import final

from sqlalchemy import BigInteger, Column, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class BaseTable(AsyncAttrs, DeclarativeBase): ...


@final
class User(BaseTable):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    level = Column(Integer, default=0)
    exp = Column(Integer, default=0)
    wallet = Column(Integer, default=1000)
    bank = Column(Integer, default=0)
    net_worth = Column(Integer, default=1000)
