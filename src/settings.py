import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

DEBUG: bool = bool(int(os.environ['DEBUG']))

CLIENT_MAX_SIZE = int(os.environ.get('CLIENT_MAX_SIZE', 1024 ** 2))

SPEECH = {
    'GOOGLE_API_KEY': os.environ.get('GOOGLE_API_KEY'),
    'LANGUAGE_CODE': 'en-US',
}

JWT_ALGORITHM = 'RS256'

MAIN_APP_PUBKEY_URL = 'http://localhost:8000/api/pubkey'

SENTRY_DSN = os.environ.get('SENTRY_SDN')
