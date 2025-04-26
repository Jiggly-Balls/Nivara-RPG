from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from discord import MISSING
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.errors import DBConnectionException

if TYPE_CHECKING:
    from typing import Self, TypeVar

    from sqlalchemy.ext.asyncio import AsyncEngine

    # from backend.base_pg import BasePool

    _JSONT = TypeVar("_JSONT", str, bytes, bytearray)


logger = logging.getLogger(__name__)


class BaseData(ABC):
    """A class representing the base of all databases connected via Postgresql.

    Attributes
    ----------
    db_engine :class:`AsyncEngine`
        An active database pool connection. Remains `None` if not connected.
    """

    db_engine: AsyncEngine = MISSING

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls.db_engine is MISSING:
            error_code = 1
            raise DBConnectionException(
                f"Database is not connected [{error_code=}]",
                error_code=error_code,
            )

        return super().__new__(cls)

    @staticmethod
    def _json_loader(obj: _JSONT) -> _JSONT | dict[str, Any]:
        try:
            loaded_obj = json.loads(obj)
        except (TypeError, json.decoder.JSONDecodeError):
            return obj
        return loaded_obj

    @staticmethod
    def make_session(
        expire_on_commit: bool = True, **kwargs: Any
    ) -> AsyncSession:
        session = async_sessionmaker(
            BaseData.db_engine, expire_on_commit=expire_on_commit, **kwargs
        )
        return session()

    @abstractmethod
    async def post_account(self) -> Any: ...

    @staticmethod
    @abstractmethod
    async def find_account() -> Any: ...

    @classmethod
    @abstractmethod
    async def get_all_accounts(cls) -> Any: ...

    @abstractmethod
    async def get_attrs(self) -> Any: ...

    @abstractmethod
    async def get_account(self) -> Any: ...

    @abstractmethod
    async def update_attr(self) -> Any: ...

    @abstractmethod
    async def update_increment(self) -> Any: ...

    @abstractmethod
    async def delete_account(self) -> Any: ...
