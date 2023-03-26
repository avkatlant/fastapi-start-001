from functools import wraps

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def router_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except IntegrityError as err:
            # logger.error(err)
            raise HTTPException(status_code=503, detail=f"Database error: {err}")

        return result

    return wrapper
