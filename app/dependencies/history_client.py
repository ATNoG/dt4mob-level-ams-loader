import time
from http import HTTPStatus

import httpx
from loguru import logger
from pydantic import BaseModel

from app.settings import settings


class OIDCTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    refresh_expires_in: int


class AsyncAutoRefreshAuth(httpx.Auth):
    def __init__(self):
        self.tokens: OIDCTokenResponse | None = None
        self.access_expires_at: float = 0.0
        self.refresh_expires_at: float = 0.0

    async def _fetch_new_tokens(self) -> OIDCTokenResponse | None:
        if settings.oidc is None:
            return None
        now = time.time()

        if self.tokens and now < self.refresh_expires_at:
            logger.info("Refresh token valid. Requesting refresh token grant...")
            data = {
                "grant_type": "refresh_token",
                "refresh_token": self.tokens.refresh_token,
                "client_id": settings.oidc.client_id,
            }
        else:
            logger.info(
                "No valid refresh token available. Falling back to password grant..."
            )
            data = {
                "grant_type": "password",
                "username": settings.oidc.username,
                "password": settings.oidc.password,
                "client_id": settings.oidc.client_id,
                "scope": "openid",
            }

        base_url = str(settings.oidc.base_url).rstrip("/")
        token_url = f"{base_url}/auth/realms/{settings.oidc.realm}/protocol/openid-connect/token"

        async with httpx.AsyncClient() as session:
            try:
                response = await session.post(token_url, data=data)
                response.raise_for_status()
                return OIDCTokenResponse(**response.json())

            except httpx.HTTPStatusError as e:
                logger.error(
                    f"OIDC token request failed ({data['grant_type']}): Status {e.response.status_code}"
                )
                return None
            except Exception as e:
                logger.error(f"Unexpected error parsing OIDC response: {e}")
                return None

    async def _update_auth_state(self):
        new_tokens = await self._fetch_new_tokens()

        if new_tokens:
            self.tokens = new_tokens
            self.access_expires_at = time.time() + new_tokens.expires_in - 10
            self.refresh_expires_at = time.time() + new_tokens.refresh_expires_in - 10
        else:
            self.tokens = None
            self.access_expires_at = 0.0
            self.refresh_expires_at = 0.0

    async def async_auth_flow(self, request: httpx.Request):
        if not self.tokens or time.time() >= self.access_expires_at:
            await self._update_auth_state()

        if not self.tokens:
            raise httpx.HTTPStatusError(
                "Authentication failed: Unable to acquire a valid access token.",
                request=request,
                response=httpx.Response(status_code=HTTPStatus.UNAUTHORIZED),
            )

        request.headers["Authorization"] = f"Bearer {self.tokens.access_token}"

        response: httpx.Response = yield request

        if response.status_code == 401:
            logger.warning(
                "Request returned a 401. Forcing an immediate token refresh..."
            )
            await self._update_auth_state()

            if self.tokens:
                request.headers["Authorization"] = f"Bearer {self.tokens.access_token}"
                yield request


auth = AsyncAutoRefreshAuth()
history_client = httpx.AsyncClient(
    base_url=str(settings.history.base_url),
    headers={"x-forwarded-user": "ditto"},
    auth=auth,
    verify=False,
    timeout=300,
)


def get_history_client() -> httpx.AsyncClient:
    return history_client
