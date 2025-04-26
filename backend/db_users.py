from __future__ import annotations

from typing import TYPE_CHECKING

from backend.base_db import BaseData
from backend.tables import User

if TYPE_CHECKING:
    from typing import Any


class UserDB(BaseData):
    def __init__(self, id: int) -> None:
        self.id = id

    async def post_account(self) -> None:
        async with BaseData.make_session() as session:
            async with session.begin():
                session.add(User(id=self.id))

    @staticmethod
    async def find_account() -> Any: ...

    @classmethod
    async def get_all_accounts(cls) -> Any: ...

    async def get_attrs(self) -> Any: ...

    async def get_account(self) -> Any: ...

    async def update_attr(self) -> Any: ...

    async def update_increment(self) -> Any: ...

    async def delete_account(self) -> Any: ...
