import ssl

import httpx

from app.settings import settings

ditto = settings.ditto
auth = None
if ditto.username and ditto.password:
    auth = httpx.BasicAuth(username=ditto.username, password=ditto.password)
ctx = ssl.create_default_context(cafile=ditto.cafile, cadata=ditto.cadata)
ditto_client = httpx.AsyncClient(base_url=str(ditto.base_url), auth=auth, verify=ctx)


def get_ditto_client() -> httpx.AsyncClient:
    return ditto_client
