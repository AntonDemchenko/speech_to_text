from typing import AsyncGenerator
from aiohttp import log

MAIN_APP_PUBKEY_URL = "http://localhost:8000/api/pubkey"


async def pubkey(app) -> AsyncGenerator:
    http_client = app['external_api']
    response = await http_client.get(MAIN_APP_PUBKEY_URL)
    json = await response.json()
    app['pubkey'] = json['pubkey']

    log.server_logger.info('Public key is gotten')

    yield
