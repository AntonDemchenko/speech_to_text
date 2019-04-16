from typing import AsyncGenerator

from aiohttp import ClientError, log

from settings import MAIN_APP_PUBKEY_URL


async def pubkey(app) -> AsyncGenerator:
    http_client = app['external_api']

    try:
        response = await http_client.get(MAIN_APP_PUBKEY_URL)
        json = await response.json()
        app['pubkey'] = json['pubkey']
    except (ClientError, ValueError, KeyError):
        log.server_logger.critical('Unable to get public key')
    else:
        log.server_logger.info('Public key is gotten')

    yield
