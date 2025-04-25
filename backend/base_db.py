from __future__ import annotations

import json
import logging
import traceback
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from discord import MISSING

from backend.errors import DBConnectionException

if TYPE_CHECKING:
    from typing import Self, TypeVar

    from backend.base_pg import BasePool

    _JSONT = TypeVar("_JSONT", str, bytes, bytearray)


logger = logging.getLogger(__name__)


class BaseData(ABC):
    """A class representing the base of all databases connected via Postgresql.

    Attributes
    ----------
    db_connection: :class:`None` | :class:`asyncpg.Pool`
        An active database pool connection. Remains `None` if not connected.
    """

    db_connection: BasePool = MISSING

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls.db_connection is not MISSING:
            if cls.db_connection.is_closing():
                stack_trace = "".join(traceback.format_stack())
                logger.warning(
                    "Connection to databse is closing.\nStack trace:\n%s",
                    stack_trace,
                )
        else:
            logger.info("Database is not connected.")

        if cls.db_connection is MISSING:
            error_code = 1
            raise DBConnectionException(
                f"Database is not connected [{error_code=}]",
                error_code=error_code,
            )

        if cls.db_connection.is_closing():
            error_code = 2
            raise DBConnectionException(
                f"Database connection is closed / closing [{error_code=}]",
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
