from __future__ import annotations

from enum import StrEnum, auto
from typing import TYPE_CHECKING, overload

import sqlalchemy
from sqlalchemy import select, update

from backend.base_db import BaseData
from backend.tables import User

if TYPE_CHECKING:
    from typing import Any, Literal


class UserAspect(StrEnum):
    level = auto()
    exp = auto()
    wallet = auto()
    bank = auto()


class UserDB(BaseData):
    def __init__(self, id: int) -> None:
        self.id: int = id

    async def post_account(self) -> bool:
        async with BaseData.session_factory() as session:
            try:
                async with session.begin():
                    session.add(User(id=self.id))
                    return True
            except sqlalchemy.exc.IntegrityError:
                return False

    @staticmethod
    async def find_account(key: User, value: Any) -> Any: ...

    @classmethod
    async def get_all_accounts(cls) -> Any: ...

    @overload
    async def get_account(self, auto_create: Literal[True] = ...) -> User: ...

    @overload
    async def get_account(
        self, auto_create: Literal[False]
    ) -> None | User: ...

    async def get_account(self, auto_create: bool = True):
        async with BaseData.session_factory() as session:
            get_user_query = select(User).where(User.id == self.id)
            result = await session.execute(get_user_query)
            data = result.fetchone()

            if data is None:
                if auto_create:
                    await self.post_account()
                    return await self.get_account()
                return None
            return data[0]

    async def update_aspect(self, key: UserAspect, value: Any) -> None:
        async with BaseData.session_factory() as session:
            payload = {str(key): value}

            update_user_query = (
                update(User)
                .where(User.id == self.id)
                .values(**payload)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(update_user_query)
            await session.commit()

    async def increment_aspect(self, key: UserAspect, value: int = 1) -> None:
        user = await self.get_account()
        final_val = user.__dict__[key] + value
        await self.update_aspect(key=key, value=final_val)

    async def delete_account(self) -> Any: ...
