from __future__ import annotations

from typing import Any, Generator, TYPE_CHECKING

from httpx import Auth

if TYPE_CHECKING:
    from httpx._models import Request, Response


class BearerAuth(Auth):
    __slots__ = ("bearer_token",)

    def __init__(self, bearer_token: str, /):
        self.bearer_token = bearer_token

    def __eq__(self, other: Any):
        return (
            isinstance(other, self.__class__)
            and other.bearer_token == self.bearer_token
        )

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        if "Authorization" not in request.headers:
            request.headers["Authorization"] = f"Bearer {self.bearer_token}"
        yield request
