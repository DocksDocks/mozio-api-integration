import os

BASE_URL = 'https://api-testing.mozio.com'
LANGUAGE = 'en-US'
API_KEY = os.environ.get('MOZIO_API_KEY')
HEADERS = {
    'Content-Type': 'application/json',
    'API-KEY': API_KEY,
    'LANG': LANGUAGE
}
indent = 4
