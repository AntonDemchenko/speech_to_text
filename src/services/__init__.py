from typing import Callable, List

from .http_client import external_api
from .pubkey import pubkey

SERVICES: List[Callable] = [
    external_api,
    pubkey
]

__all__ = [
    'external_api',
    'SERVICES'
]
