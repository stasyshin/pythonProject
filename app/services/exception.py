from functools import wraps

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, DBAPIError

from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


class ExistsException(HTTPException):
    def __init__(self, field: str):
        super().__init__(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"This {field} already exists"
        )


class NotExistsException(HTTPException):
    def __init__(self, field: str):
        super().__init__(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"This {field} doesn't exist"
        )


def exception_decorator(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (IntegrityError, DBAPIError) as exc:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail=exc.args[0]
            )

    return wrapped
