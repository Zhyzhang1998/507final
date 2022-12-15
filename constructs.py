# import read_cache as rc

# cache = rc.open_cache()

# CREATE CLASSES
## Class for Twitter
class Tweet():
    def __init__(self, json):
        self.id = json["id"]
        self.text = json["text"]
        self.screenname = json["user"]['screen_name']
        self.url = f"https://twitter.com/{self.screenname}/status/{self.id}"
        self.retweet_count = json["retweet_count"]
        self.favorite_count = json["favorite_count"]

## Class for NewsAPI
class News():
    def __init__(self, json):
        self.title = json["title"]
        self.description = json["description"]
        self.url = json["url"]
        self.source = json["source"]["name"]
        self.author = json["author"]



