import io
from aiohttp import ClientResponse, ClientError, log
from typing import Optional

import settings
from utils import read, convert_to_b64
from .exceptions import InternalError


class GoogleRecognizer:
    API_URL = "https://speech.googleapis.com/v1/speech:recognize"
    API_KEY = settings.SPEECH["GOOGLE_API_KEY"]
    LANGUAGE_CODE = settings.SPEECH["LANGUAGE_CODE"]
    ENCODING = "FLAC"
    CHUNK_SIZE = 1024 * 64

    def __init__(self, http_client):
        self.http_client = http_client

    async def make_request(self, audio_b64: str) -> Optional[ClientResponse]:
        try:
            response = await self.http_client.post(
                self.API_URL,
                json={
                    "audio": {
                        "content": audio_b64,
                    },
                    "config": {
                        "encoding": self.ENCODING,
                        "languageCode": self.LANGUAGE_CODE
                    }
                },
                params={"key": self.API_KEY}
            )
        except ClientError as err:
            log.client_logger.critical(str(err))
            return None
        else:
            return response

    async def extract_text(self, response: ClientResponse) -> Optional[str]:
        try:
            json = await response.json()
            text = json["results"][0]["alternatives"][0]["transcript"]
        except (ValueError, KeyError, IndexError):
            return None
        else:
            return text

    async def speech_to_text(self, audio_file: io.BytesIO) -> Optional[str]:
        audio = await read(audio_file, self.CHUNK_SIZE)
        audio_b64 = convert_to_b64(audio)
        response = await self.make_request(audio_b64)
        if response is None or 500 <= response.status < 600:
            raise InternalError("Unable to work with Google")
        text = await self.extract_text(response)
        return text
