import logging

import sentry_sdk
from aiohttp import web

import settings
from middleware import MIDDLEWARES
from routes import setup_routes
from services import SERVICES


async def init():
    sentry_sdk.init(settings.SENTRY_DSN)

    app = web.Application(
        middlewares=MIDDLEWARES,
        client_max_size=settings.CLIENT_MAX_SIZE
    )
    app.cleanup_ctx.extend(SERVICES)
    setup_routes(app)
    return app


logging.basicConfig(level=(logging.INFO if not settings.DEBUG else logging.DEBUG))

if __name__ == '__main__':
    web.run_app(init(), port=8085)
