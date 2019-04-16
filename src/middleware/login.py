import jwt
from aiohttp import web
from jwt.exceptions import DecodeError, ExpiredSignatureError

from settings import JWT_ALGORITHM
from utils import error


@web.middleware
async def login_middleware(request: web.Request, handler) -> web.Response:
    try:
        token = request.headers['Authorization'].split()[1]
        jwt.decode(token, request.app['pubkey'], algorithms=JWT_ALGORITHM)
    except (KeyError, IndexError):
        return error('Authorization header is required', 401)
    except DecodeError:
        return error('Unable to decode token', 401)
    except ExpiredSignatureError:
        return error('Token lifetime is expired.', 401)
    else:
        response: web.Response = await handler(request)
        return response
