import httpx
import pytest
from pytest_httpx import HTTPXMock

from aiosendgrid.auth import BearerAuth


@pytest.mark.asyncio
async def test_bearer_auth(httpx_mock: HTTPXMock):
    httpx_mock.add_response()
    async with httpx.AsyncClient(auth=BearerAuth("token")) as client:
        await client.get("https://test_url")
    assert httpx_mock.get_request().headers["Authorization"] == "Bearer token"
