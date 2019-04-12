from aiohttp import web
from mutagen.flac import FLAC
from mutagen import MutagenError

from external.speech import speech_to_text
import settings


class SpeechRecognition(web.View):
    MAX_SIZE = settings.SPEECH["MAX_SIZE"]
    MAX_LENGTH = settings.SPEECH["MAX_LENGTH"]

    @staticmethod
    def error(message, status_code):
        return web.json_response(
            {"error": message},
            status=status_code
        )

    @staticmethod
    def get_flac(audio):
        flac = None
        try:
            flac = FLAC(audio)
        except MutagenError:
            pass
        finally:
            audio.seek(0)
        return flac

    def post(self, request):
        audio = request.FILES.get("audio")

        if not audio:
            return self.error("Missed audio file argument.", 400)

        if audio.size > self.MAX_SIZE:
            return self.error(
                "Too big audio file. "
                "Maximal possible size is {} byte(s).".format(self.MAX_SIZE),
                400
            )

        flac = self.get_flac(audio)
        if not flac:
            return self.error("Invalid encoding. Please provide audio file in FLAC encoding.", 400)

        if flac.info.length > self.MAX_LENGTH:
            return self.error(
                "Too long audio file. "
                "Maximal possible length is {} second(s).".format(self.MAX_LENGTH),
                400
            )

        if flac.info.channels != 1:
            return self.error(
                "Passed stereo file but one channel file is required.",
                400
            )

        try:
            text = speech_to_text(audio)
        except RuntimeError:
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

        return Response({
            "result": text
        })
