from search import search_test
from constants import API_KEY

if not API_KEY:
    raise ValueError('Missing API key in environment variables!')

if __name__ == '__main__':
    search_test()
