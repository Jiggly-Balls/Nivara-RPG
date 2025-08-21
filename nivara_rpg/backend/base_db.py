from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from discord.utils import MISSING
from sqlalchemy.ext.asyncio import AsyncSession

from backend.errors import DBConnectionException

if TYPE_CHECKING:
    from typing import Self

    from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker


logger = logging.getLogger(__name__)


class BaseData(ABC):
    """The base class of all databases exposing the required endpoints as methods.

    Attributes
    ----------
    db_engine :class:`AsyncEngine`
        The SQLAlchemy async engine for the database.
        Remains as `discord.MISSING` if not connected.
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

    # @staticmethod
    # def session_factory() -> AsyncSession:
    #     session = async_sessionmaker(
    #         BaseData.db_engine, expire_on_commit=True
    #     )
    #     return session()

    @abstractmethod
    async def post_account(self) -> Any: ...

    @staticmethod
    @abstractmethod
    async def find_account(key: Any, value: Any) -> Any: ...

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
