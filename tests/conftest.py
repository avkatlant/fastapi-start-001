import asyncio
import sys
from asyncio import AbstractEventLoop
from pathlib import Path
from typing import AsyncIterator, Generator

import pytest
from httpx import AsyncClient

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client
