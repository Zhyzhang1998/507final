import json
import requests
from requests_oauthlib import OAuth1
import secret

# Secret
client_key = secret.TWITTER_API_KEY
client_secret = secret.TWITTER_API_SECRET
access_token = secret.TWITTER_ACCESS_TOKEN
access_token_secret = secret.TWITTER_ACCESS_TOKEN_SECRET
newsapi_key = secret.NEWSAPI

oauth = OAuth1(client_key,
            client_secret=client_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret)

# Endpoint
endpoint_url_twitter = 'https://api.twitter.com/1.1/search/tweets.json'
endpoint_url_newsapi = 'https://newsapi.org/v2/everything'

# Cache
CACHE_FILENAME = "cache.json"

def open_cache():

    try:
        with open(CACHE_FILENAME, 'r', encoding='utf-8') as file_obj:
            cache_dict = json.load(file_obj)
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict, encoding='utf-8', ensure_ascii=False, indent=2):
    with open(CACHE_FILENAME, 'w', encoding=encoding) as file_obj:
        json.dump(cache_dict, file_obj, ensure_ascii=ensure_ascii, indent=indent)


def get_data(keyword, platform):
    if platform == "twitter":
        params = {'q': keyword}
        return requests.get(endpoint_url_twitter, params=params, auth=oauth).json()
    if platform == 'newsapi':
        params = {'q': keyword, "sortBy": "top", "apiKey": newsapi_key}
        return requests.get(endpoint_url_newsapi, params=params).json()


def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path to the file
        data (dict)/(list): the data to be encoded as JSON and written to the file
        encoding (str): name of encoding used to encode the file
        ensure_ascii (str): if False non-ASCII characters are printed as is;
                            otherwise non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to
                      encoded JSON

    Returns:
        None
    """

    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)


def main():
    cache = open_cache()



    save_cache(cache)


if __name__ == '__main__':
    main()
