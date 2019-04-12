from aiohttp import web

import recognizers
from recognizers import GoogleRecognizer


class SpeechRecognition(web.View):

    @staticmethod
    def error(message, status_code):
        return web.json_response(
            {"error": message},
            status=status_code
        )

    async def post(self) -> web.Response:
        data = await self.request.post()

        audio_field = data.get("audio")
        if not audio_field:
            return self.error("Missed audio file argument.", 400)

        audio = audio_field.file

        try:
            recognizer = GoogleRecognizer(self.request.app["external_api"])
            text = await recognizer.speech_to_text(audio)
        except recognizers.InternalError:
            return self.error(
                "Something went wrong. Please try again later.",
                500
            )

        if not text:
            return self.error(
                "Unable to recognize speech. "
                "Please provide another audio file.",
                400
            )

        return web.json_response({
            "result": text
        })
