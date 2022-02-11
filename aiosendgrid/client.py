from __future__ import annotations

import os
from typing import Any, Optional, TYPE_CHECKING

from httpx import AsyncClient

from .auth import BearerAuth
from .constants import SENDGRID_BASE_URL

if TYPE_CHECKING:
    from httpx._models import Response
    from httpx._types import AuthTypes, URLTypes


class AsyncSendGridClient(AsyncClient):
    __slots__ = ()

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: URLTypes = SENDGRID_BASE_URL,
        auth: AuthTypes = None,
        **kwargs: Any,
    ):
        if auth is None:
            api_key = api_key or os.environ.get("SENDGRID_API_KEY")
            if api_key is None:
                raise ValueError("`api_key` and `auth` cannot be both null.")
            auth = BearerAuth(api_key)

        kwargs.setdefault("http2", True)
        super().__init__(auth=auth, base_url=base_url, **kwargs)

    async def send_mail_v3(self, body: dict[str, Any]) -> Response:
        res = await self.post("/v3/mail/send", json=body)
        res.raise_for_status()
        return res
