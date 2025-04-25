from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

import asyncpg
from asyncpg import connection, protocol

from backend.base_db import BaseData

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from typing import Any

    from asyncpg import Connection


logger = logging.getLogger(__name__)


class BasePool(asyncpg.Pool):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__host = kwargs.get("host")
        self.__database = kwargs.get("database")
        self.__port = kwargs.get("port")
        self.__user = kwargs.get("user")
        self.__password = kwargs.get("password")

    async def __reconnect_execution(
        self,
        method: Callable[..., Coroutine[Any, Any, Any]],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """|coro|

        Calls and awaits the method with passed passed args & kwargs.
        If the database connection fails, it attempts to reconnect once
        and re-executes the passed method.

        Parameters
        ----------
        method: :class:`Coroutine`
            The method associated with :class:`asyncpg.Pool`.
        """

        try:
            return await method(*args, **kwargs)
        except asyncpg.ConnectionDoesNotExistError:
            logger.warning(
                f"Failed to connect to DB while executing method: {method.__name__}. "
                "Attempting to create new pool connection..."
            )
            await asyncio.sleep(3)
            BaseData.db_connection = await create_base_pool_connection(
                host=self.__host,
                database=self.__database,
                port=self.__port,
                user=self.__user,
                password=self.__password,
                max_inactive_connection_lifetime=0,
            )
            logger.warning(
                "Successfully created a new pool connection. "
                f"Attempting to re-execute method: {method.__name__}"
            )

            result = await method(*args, **kwargs)

            logger.warning(
                f"Successfully re-executed method: {method.__name__}."
            )

            return result

    async def execute(
        self, query: str, *args: Any, timeout: None | float = None
    ) -> str:
        return await self.__reconnect_execution(
            super().execute,
            query,
            *args,
            timeout=timeout,  # pyright:ignore[reportUnknownArgumentType]
        )

    async def fetch(
        self,
        query: str,
        *args: Any,
        timeout: float | None = None,
        record_class: Any | None = None,
    ) -> list[Any]:
        return await self.__reconnect_execution(
            super().fetch,  # pyright:ignore[reportUnknownArgumentType]
            query,
            *args,
            timeout=timeout,
            record_class=record_class,
        )

    async def fetchrow(
        self,
        query: str,
        *args: Any,
        timeout: float | None = None,
        record_class: Any | None = None,
    ) -> Any:
        return await self.__reconnect_execution(
            super().fetchrow,  # pyright:ignore[reportUnknownArgumentType]
            query,
            *args,
            timeout=timeout,
            record_class=record_class,
        )


def create_base_pool_connection(
    dsn: None | str = None,
    *,
    min_size: int = 10,
    max_size: int = 10,
    max_queries: int = 50000,
    max_inactive_connection_lifetime: float = 300.0,
    setup: None | Coroutine[Any, Any, Any] = None,
    init: None | Coroutine[Any, Any, Any] = None,
    loop: None | Any = None,
    connection_class: type[Connection] = connection.Connection,
    record_class: Any = protocol.Record,
    **connect_kwargs: Any,
) -> BasePool:
    r"""Create a connection pool.

    Can be used either with an ``async with`` block:

    .. code-block:: python

        async with asyncpg.create_pool(user='postgres',
                                       command_timeout=60) as pool:
            await pool.fetch('SELECT 1')

    Or to perform multiple operations on a single connection:

    .. code-block:: python

        async with asyncpg.create_pool(user='postgres',
                                       command_timeout=60) as pool:
            async with pool.acquire() as con:
                await con.execute('''
                   CREATE TABLE names (
                      id serial PRIMARY KEY,
                      name VARCHAR (255) NOT NULL)
                ''')
                await con.fetch('SELECT 1')

    Or directly with ``await`` (not recommended):

    .. code-block:: python

        pool = await asyncpg.create_pool(user='postgres', command_timeout=60)
        con = await pool.acquire()
        try:
            await con.fetch('SELECT 1')
        finally:
            await pool.release(con)

    .. warning::
        Prepared statements and cursors returned by
        :meth:`Connection.prepare() <asyncpg.connection.Connection.prepare>`
        and :meth:`Connection.cursor() <asyncpg.connection.Connection.cursor>`
        become invalid once the connection is released.  Likewise, all
        notification and log listeners are removed, and ``asyncpg`` will
        issue a warning if there are any listener callbacks registered on a
        connection that is being released to the pool.

    :param str dsn:
        Connection arguments specified using as a single string in
        the following format:
        ``postgres://user:pass@host:port/database?option=value``.

    :param \*\*connect_kwargs:
        Keyword arguments for the :func:`~asyncpg.connection.connect`
        function.

    :param Connection connection_class:
        The class to use for connections.  Must be a subclass of
        :class:`~asyncpg.connection.Connection`.

    :param type record_class:
        If specified, the class to use for records returned by queries on
        the connections in this pool.  Must be a subclass of
        :class:`~asyncpg.Record`.

    :param int min_size:
        Number of connection the pool will be initialized with.

    :param int max_size:
        Max number of connections in the pool.

    :param int max_queries:
        Number of queries after a connection is closed and replaced
        with a new connection.

    :param float max_inactive_connection_lifetime:
        Number of seconds after which inactive connections in the
        pool will be closed.  Pass ``0`` to disable this mechanism.

    :param coroutine setup:
        A coroutine to prepare a connection right before it is returned
        from :meth:`Pool.acquire() <pool.Pool.acquire>`.  An example use
        case would be to automatically set up notifications listeners for
        all connections of a pool.

    :param coroutine init:
        A coroutine to initialize a connection when it is created.
        An example use case would be to setup type codecs with
        :meth:`Connection.set_builtin_type_codec() <\
        asyncpg.connection.Connection.set_builtin_type_codec>`
        or :meth:`Connection.set_type_codec() <\
        asyncpg.connection.Connection.set_type_codec>`.

    :param loop:
        An asyncio event loop instance.  If ``None``, the default
        event loop will be used.

    :return: An instance of :class:`~asyncpg.pool.Pool`.

    .. versionchanged:: 0.10.0
       An :exc:`~asyncpg.exceptions.InterfaceError` will be raised on any
       attempted operation on a released connection.

    .. versionchanged:: 0.13.0
       An :exc:`~asyncpg.exceptions.InterfaceError` will be raised on any
       attempted operation on a prepared statement or a cursor created
       on a connection that has been released to the pool.

    .. versionchanged:: 0.13.0
       An :exc:`~asyncpg.exceptions.InterfaceWarning` will be produced
       if there are any active listeners (added via
       :meth:`Connection.add_listener()
       <asyncpg.connection.Connection.add_listener>`
       or :meth:`Connection.addlogger_listener()
       <asyncpg.connection.Connection.addlogger_listener>`) present on the
       connection at the moment of its release to the pool.

    .. versionchanged:: 0.22.0
       Added the *record_class* parameter.
    """
    return BasePool(
        dsn,
        connection_class=connection_class,
        record_class=record_class,
        min_size=min_size,
        max_size=max_size,
        max_queries=max_queries,
        loop=loop,
        setup=setup,
        init=init,
        max_inactive_connection_lifetime=max_inactive_connection_lifetime,
        **connect_kwargs,
    )
