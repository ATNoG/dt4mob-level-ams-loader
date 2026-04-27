import httpx

from app.settings import settings

history = settings.history
auth = None
if history.username and history.password:
    auth = httpx.BasicAuth(username=history.username, password=history.password)
history_client = httpx.AsyncClient(
    base_url=str(history.base_url),
    headers={"x-forwarded-user": "ditto"},
    auth=auth,
    verify=False,
    timeout=300,
)


def get_history_client() -> httpx.AsyncClient:
    return history_client
