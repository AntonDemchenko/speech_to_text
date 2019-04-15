from .exception import exception_middleware
from .login import login_middleware

MIDDLEWARES = [
    exception_middleware,
    login_middleware
]

__all__ = [
    'MIDDLEWARES'
]
