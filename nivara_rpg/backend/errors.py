from typing import Any, final


class DBException(Exception):
    """Base class of the database exceptions."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


@final
class DBConnectionException(DBException):
    """Raised when database connection issue arises.

    Attributes
    ------------
    error_code: :class:`int`
        The error code associated with connection exception.
    """

    def __init__(self, *args: Any, error_code: int, **kwargs: Any) -> None:
        self.error_code = error_code
        super().__init__(*args, **kwargs)


@final
class InvalidType(DBException):
    """Raised when an invalid type is passed.

    Attributes
    ------------
    val_type: :type:`type`
        The invalid type that was passed.

    expected_type: :type:`type`
        The type that was expected.
    """

    def __init__(
        self, *args: Any, val_type: type, expected_type: type, **kwargs: Any
    ) -> None:
        self.val_type = val_type
        self.expected_type = expected_type
        super().__init__(*args, **kwargs)
