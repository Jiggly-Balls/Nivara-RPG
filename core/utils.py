from __future__ import annotations

from typing import Any, overload

from discord import Embed

from data.constants.core import ERROR_COLOUR, PRIMARY_COLOUR


class MainEmbed(Embed):
    @overload
    def __init__(self, description: str, **kwargs: Any) -> None: ...

    @overload
    def __init__(
        self, title: str, description: str, **kwargs: Any
    ) -> None: ...

    def __init__(  # pyright:ignore[reportInconsistentOverload]
        self, title: str, description: str | None = None, /, **kwargs: Any
    ) -> None:
        if description is None:
            description = title
            title = None

        super().__init__(
            title=title,
            description=description,
            colour=PRIMARY_COLOUR,
            **kwargs,
        )


class ErrorEmbed(Embed):
    @overload
    def __init__(self, description: str, **kwargs: Any) -> None: ...

    @overload
    def __init__(
        self, title: str, description: str, **kwargs: Any
    ) -> None: ...

    def __init__(  # pyright:ignore[reportInconsistentOverload]
        self, title: str, description: str | None = None, /, **kwargs: Any
    ) -> None:
        if description is None:
            description = title
            title = None

        super().__init__(
            title=title,
            description=description,
            colour=ERROR_COLOUR,
            **kwargs,
        )
