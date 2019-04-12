import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

DEBUG: bool = bool(int(os.environ['DEBUG']))

CLIENT_MAX_SIZE = int(os.environ.get("CLIENT_MAX_SIZE", 1024 ** 2))

SPEECH = {
    "GOOGLE_API_KEY": os.environ.get("GOOGLE_API_KEY"),
    "ENCODING": "FLAC",
    "LANGUAGE_CODE": "en-US",
    "MAX_SIZE": 10485760,  # in bytes
    "MAX_LENGTH": 15  # in seconds
}
