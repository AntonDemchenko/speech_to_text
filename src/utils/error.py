from aiohttp import web


def error(message, status_code):
    return web.json_response(
        {"error": message},
        status=status_code
    )
