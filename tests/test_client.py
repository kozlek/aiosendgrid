import json
import os

import pytest
from httpx import HTTPError
from pytest_httpx import HTTPXMock

from aiosendgrid import AsyncSendGridClient
from aiosendgrid.auth import BearerAuth


@pytest.mark.asyncio
async def test_async_sendgrid_client_init():
    client = AsyncSendGridClient(api_key="token")
    assert client.auth == BearerAuth("token")

    # missing api_key
    with pytest.raises(ValueError):
        AsyncSendGridClient()

    os.environ["SENDGRID_API_KEY"] = "token"
    assert client.auth == BearerAuth("token")


@pytest.mark.asyncio
async def test_async_sendgrid_client_send_email_v3(httpx_mock: HTTPXMock):
    data = {
        "personalizations": [
            {
                "to": [{"email": "test@example.com"}],
                "subject": "Sending with SendGrid is Fun",
            }
        ],
        "from": {"email": "test@example.com"},
        "content": [
            {"type": "text/plain", "value": "and easy to do anywhere, even with Python"}
        ],
    }

    httpx_mock.add_response(status_code=202)
    async with AsyncSendGridClient(api_key="token") as client:
        res = await client.send_mail_v3(data)
    assert res.status_code == 202
    assert httpx_mock.get_request().stream.read() == json.dumps(data).encode()

    httpx_mock.add_response(status_code=400)
    async with AsyncSendGridClient(api_key="token") as client:
        with pytest.raises(HTTPError):
            await client.send_mail_v3(data)
