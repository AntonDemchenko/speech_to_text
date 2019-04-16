from aiohttp import web

import recognizers
from recognizers import GoogleRecognizer
from utils import error


class SpeechRecognition(web.View):

    async def post(self) -> web.Response:
        data = await self.request.post()

        audio_field = data.get('audio')
        if not audio_field:
            return error('Missed audio file argument.', 400)

        audio = audio_field.file

        try:
            recognizer = GoogleRecognizer(self.request.app['external_api'])
            text = await recognizer.speech_to_text(audio)
        except recognizers.InternalError:

            return error(
                'Something went wrong. Please try again later.',
                500
            )
        except recognizers.RecognitionError:
            return error(
                'Unable to recognize speech. '
                'Please provide another audio file.',
                400
            )

        return web.json_response({
            'result': text
        })
