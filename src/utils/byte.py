import base64
import io
from typing import AsyncGenerator


async def chunks(stream: io.BytesIO, chunk_size: int) -> AsyncGenerator[bytes, bytes]:
    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
        yield chunk
    return


async def read(stream: io.BytesIO, chunk_size: int) -> bytes:
    data = b''
    async for chunk in chunks(stream, chunk_size):
        data += chunk
    return data


def convert_to_b64(data: bytes) -> str:
    data = base64.b64encode(data)
    data = data.decode('ascii')
    return data
