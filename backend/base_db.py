from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from discord import MISSING
from sqlalchemy.ext.asyncio import AsyncSession

from backend.errors import DBConnectionException

if TYPE_CHECKING:
    from typing import Self

    from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker


logger = logging.getLogger(__name__)


class BaseData(ABC):
    """A class representing the base of all databases connected via Postgresql.

    Attributes
    ----------
    db_engine :class:`AsyncEngine`
        The SQLAlchemy async engine for the database. Remains as `discord.MISSING` if not connected.
    """

    db_engine: AsyncEngine = MISSING
    session_factory: async_sessionmaker[AsyncSession] = MISSING

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls.db_engine is MISSING:
            error_code = 1
            raise DBConnectionException(
                f"Database is not connected [{error_code=}]",
                error_code=error_code,
            )

        return super().__new__(cls)

    @abstractmethod
    async def post_account(self) -> Any: ...

    @staticmethod
    @abstractmethod
    async def find_account(key: str, value: Any) -> Any: ...

    @classmethod
    @abstractmethod
    async def get_all_accounts(cls) -> Any: ...

    @abstractmethod
    async def get_account(self) -> Any: ...

    @abstractmethod
    async def update_aspect(self, key: Any, value: Any) -> Any: ...

    @abstractmethod
    async def increment_aspect(self, key: Any, value: int) -> Any: ...

    @abstractmethod
    async def delete_account(self) -> Any: ...
