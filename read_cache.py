import json

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

# cache = open_cache()
# print(yaml.dump(cache, default_flow_style=False))