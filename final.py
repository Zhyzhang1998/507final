import json
import requests
from requests_oauthlib import OAuth1
import secret
import webbrowser
import yaml

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
    """Open saved cache or create a new cache.

    Parameters
    ----------
    None

    Returns
    ----------
    Dict
        If there is not saved cache.
    """
    try:
        with open(CACHE_FILENAME, 'r', encoding='utf-8') as file_obj:
            cache_dict = json.load(file_obj)
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict, encoding='utf-8', ensure_ascii=False, indent=2):
    """Save the cache file.

    Parameters
    ----------
    cache_dict: Dict

    Returns
    ----------
    None
    """
    with open(CACHE_FILENAME, 'w', encoding=encoding) as file_obj:
        json.dump(cache_dict, file_obj, ensure_ascii=ensure_ascii, indent=indent)


def get_data(keyword, platform):
    """Get the data.

    Parameters
    ----------
    keyword: str
    platform: str

    Returns
    ----------
    Dict
        Json data.
    """
    if platform == "twitter":
        params = {'q': keyword}
        return requests.get(endpoint_url_twitter, params=params, auth=oauth).json()
    if platform == 'newsapi':
        params = {'q': keyword, "sortBy": "top", "apiKey": newsapi_key}
        return requests.get(endpoint_url_newsapi, params=params).json()


def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """Export the json data to files.

    Parameters
    ----------
    filepath: str
    data: dict

    Returns
    ----------
    None
    """

    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)

def find_commonwords():
    pass

def generate_wordcloud():
    pass



# class Tweet:
#     def __init__(self, dic):
#         self.text = dic

# class News:
#     def __init__(self, dic):
#         self.

def main():
    """Print messages and start the program.

    Parameters
    ----------
    None

    Returns
    ----------
    None
    """
    print('Hello!')
    cache = open_cache()
    city = input('Which city do you want to know?\n')
    keywords = input('What do you want to know? Give me one keyword.\n')
    answer = city + " " +keywords

    try:
        # While we had the data cached before.
        twitter_result = cache[city][keywords]['Twitter']
        news_result = cache[city][keywords]['NewsAPI']

    except:
        # While there is no cache.
        twitter_result = get_data(answer, "twitter")["statuses"]
        news_result = get_data(answer, "newsapi")["articles"]
        if city not in cache.keys(): # If the city not in cache
            cache[city] = {keywords: {'Twitter': twitter_result, 'NewsAPI': news_result}}
        elif keywords not in cache[city].keys(): # If the keywords not in cache
            cache[city][keywords] = {'Twitter': twitter_result, 'NewsAPI': news_result}


    save_cache(cache)


if __name__ == '__main__':
    main()
