import time
from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, some_attribute: str) -> None:
        super().__init__(app)
        self.some_attribute = some_attribute

    async def dispatch(self, request: Request, call_next: Callable[..., Awaitable[Response]]) -> Response:
        start_time = time.monotonic()
        response = await call_next(request)
        process_time = time.monotonic() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
