from typing import AsyncGenerator
from aiohttp import log
from settings import MAIN_APP_PUBKEY_URL


async def pubkey(app) -> AsyncGenerator:
    http_client = app['external_api']
    response = await http_client.get(MAIN_APP_PUBKEY_URL)
    json = await response.json()
    app['pubkey'] = json['pubkey']

    log.server_logger.info('Public key is gotten')

    yield
