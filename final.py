import json
import requests
from requests_oauthlib import OAuth1
import secret
import webbrowser
import read_cache as rc
import constructs as co
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np

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
        params = {'q': keyword, "count": 100, "result_type": 'mixed', "include_entities": True}
        return requests.get(endpoint_url_twitter, params=params, auth=oauth).json()
    if platform == 'newsapi':
        params = {'q': keyword, "sortBy": "top", "apiKey": newsapi_key}
        return requests.get(endpoint_url_newsapi, params=params).json()


def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """Export the json data to files. Helper funciton.

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

def yes(prompt):
    """Returns True when if the answer is yes. False if it is no.

    Parameters
    ----------
    prompt: String

    Returns
    ----------
    Bool
    """
    while True:
        Ans_input = input(f"{prompt}\n")
        yes = ['y', 'yes', 'yup', 'sure']
        no = ['n', 'no']
        if Ans_input.lower() in yes:
            return True
        elif Ans_input.lower() in no:
            return False
        else:
            print('Please answer yes or no!')

def get_result(cache, city, keywords):
    """Returns result from API or cache.

    Parameters
    ----------
    cache: dic
    city: str
    keywords: str

    Returns
    ----------
    tuple
    """
    answer = city + " " +keywords
    try:
        # While we had the data cached before.
        twitter_result = cache[city][keywords]['Twitter']
        news_result = cache[city][keywords]['NewsAPI']

    except:
        # While there is no cache.
        twitter_result = get_data(answer, "twitter")["statuses"]
        news_result = get_data(answer, "newsapi")["articles"]
        # If the city not in cache
        if city not in cache.keys():
            cache[city] = {keywords: {'Twitter': twitter_result, 'NewsAPI': news_result}}
        elif keywords not in cache[city].keys():
        # If the keywords not in cache
            cache[city][keywords] = {'Twitter': twitter_result, 'NewsAPI': news_result}
    return twitter_result, news_result

def classdata(list):
    """Class the data.

    Parameters
    ----------
    list: list

    Returns
    ----------
    list
    """
    result = []
    for i in list:
        try:
            result.append(co.Tweet(i))
        except:
            result.append(co.News(i))
    return result

def sorttweet(tweet):
    """Sort the tweet data based on favorite_count.

    Parameters
    ----------
    tweet: list

    Returns
    ----------
    None
    """
    tweet.sort(reverse=True, key=lambda x:x.favorite_count)

def structure(city, keywords, tweet, news):
    """Structure the data into a tree.

    Parameters
    ----------
    city: str
    keywords: str
    tweet: list
    news: list

    Returns
    ----------
    Tree: dic
    """
    dic = {}
    sorttweet(tweet)
    dic[city] = {keywords: {'Twitter': tweet[:10], 'NewsAPI': news[:10]}}
    return dic

def printtree(tree, city, keywords):
    """Print the tree in a clear way.

    Parameters
    ----------
    tree: dic
    city: str
    keywords: str

    Returns
    ----------
    None
    """
    print(city)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f'   {keywords}')
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f'Twitter')

    indexnum = 0
    for item in tree[city][keywords]["Twitter"]:
        indexnum += 1
        print(f"      {indexnum}. Id: {item.id}")
        print(f"        Text: {item.text}")
        print(f"        retweet_count: {item.retweet_count}")
        print(f"        favorite_count: {item.favorite_count}")
        print(f"        url: {item.url}")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f'NewsAPI')
    indexnum = 0
    for item in tree[city][keywords]["NewsAPI"]:
        indexnum += 1
        print(f"      {indexnum}. Title: {item.title}")
        print(f"        Description: {item.description}")
        print(f"        Source: {item.source}")
        print(f"        author: {item.author}")
        print(f"        url: {item.url}")

def find_commonwords(list):
    """Find the most common words and return a list.

    Parameters
    ----------
    List: list

    Returns
    ----------
    List
    """
    words = ''
    try:
        for i in list:
            words += f' {i.title}'
    except:
        for i in list:
            words += f' {i.text}'
    word = words.split()
    return Counter(word).most_common()

def filterCommonword(list, city, keywords):
    """Filter the common words list with filter_words.

    Parameters
    ----------
    list: list
    city: str
    keywords: str

    Returns
    ----------
    list
    """
    filter_words = ['the', 'is', 'are', 'on', 'https',
    'this', 'for', 'to', 'in', 'a', 'and', 'of', 'that',
    'with', 'at', 'there', 'by', 'about', 'you', 'or'
    'just', 'they', 'they’re', 'over', 'thank', 'city', 'City', 'food']
    filter_words.extend(city.split())
    filter_words.extend(city.lower().split())
    filter_words.append(keywords)
    filter_words.append(keywords.capitalize())
    result = []
    for i in list:
        if i[0] not in filter_words:
            result.append(i)
    return result

def generate_wordcloud(str):
    """Generate the word cloud chart based on the common words list.

    Parameters
    ----------
    str: str

    Returns
    ----------
    None
    """
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(background_color ='white', stopwords = stopwords,).generate(str)
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.show()

def creatdata(twitterdata):
    """Create the data for plot a bar chart.

    Parameters
    ----------
    twitterdata: list

    Returns
    ----------
    dic
    """
    dic = {}
    for item in twitterdata[:8]:
        dic[item.text] = item.favorite_count
    return dic

def plotbarchart(data, city, keywords):
    """Plot a bar chart.

    Parameters
    ----------
    data: dic
    city: str
    keywords: str

    Returns
    ----------
    None
    """
    text = list(data.keys())
    value = list(data.values())
    fig, ax = plt.subplots(figsize =(16, 9))
    ax.barh(text, value)
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)
    ax.set_title(f"{city}'s Twitter about {keywords}",
			loc ='left', )
    plt.xlabel("Likes")
    plt.show()

def sortbysource(newsdata):
    """Sort the news data based on source.

    Parameters
    ----------
    newsdata: list

    Returns
    ----------
    dic: dic
    """
    dic = {}
    for i in newsdata:
        if i.source not in dic.keys():
            dic[i.source] = [i.title]
        else:
            dic[i.source].append(i.title)
    return dic


def createdataforpie(dic, totalnum):
    """Creat a new dictionary for pie chart.

    Parameters
    ----------
    dic: dic
        from funtion sortbysource()

    totalnum: int

    Returns
    ----------
    dicwithnum: dic
    """
    dicwithnum = {}
    for i in dic:
        dicwithnum[i] = len(dic[i])/totalnum*100
    return dicwithnum

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
    cache = rc.open_cache()
    while True:
        ## First question
        city = input('Which city do you want to know? Or you can enter exit to quit.\n')
        if city.lower() == 'exit':
            print("Goodbye!")
            break
        ## Second question
        keywords = input('What do you want to know? Give me one keyword.\n')

        ## Get the data
        twitter_result, news_result = get_result(cache, city, keywords)
        twitterdata = classdata(twitter_result)
        newsdata = classdata(news_result)

        ## Structure the data
        tree = structure(city, keywords, twitterdata, newsdata)

        ## Print out the tree
        if yes("Do want to see the result in the form of tree?"):
            printtree(tree, city, keywords)

        ## Ask users if they want to open the url in Webbrowser
            while True:
                sourcepick = input("Which one your want to learn more info, NewsAPI or Twitter? (Please enter 'NewsAPI' or 'Twitter'!!)\n")
                if str(sourcepick) == 'NewsAPI' or str(sourcepick) == 'Twitter':
                    break
                else:
                    print("Try again!")
            while True:
                numpick = input("Enter a number.\n")
                if 1 <= int(numpick) <= 10:
                    break
                else:
                    print("Try again!")
            urlpick = (tree[city][keywords][str(sourcepick)][int(numpick)-1]).url
            print("Launching")
            print(urlpick)
            print("in web browser...")
            webbrowser.open(urlpick)

        ## Find the top10 most common words and Draw the word cloud
        if yes("Do you want to see the word cloud based on the most common words? Which platform Please enter 'NewsAPI' or 'Twitter'!!"):
            while True:
                wordcloudpick = input("Which platform? Please enter 'NewsAPI' or 'Twitter'!!\n")
                if str(wordcloudpick) == 'Twitter':
                    commonword = find_commonwords(twitterdata)
                    commonwordfiltered = filterCommonword(commonword, city, keywords)
                    all = ''
                    for word in commonwordfiltered:
                        if 'https' not in word[0] and keywords != word[0].lower() and word[0].lower() not in city.split():
                            all += f'{word[0]} '
                    generate_wordcloud(all)
                    break
                if str(wordcloudpick) == 'NewsAPI':
                    commonword = find_commonwords(newsdata)
                    commonwordfiltered = filterCommonword(commonword, city, keywords)
                    all = ''
                    for word in commonwordfiltered:
                        if 'https' not in word[0] and keywords != word[0].lower() and word[0].lower() not in city.split():
                            all += f'{word[0]} '
                    generate_wordcloud(all)
                    break
                else:
                    print("Try again!")


        ## Plot the bar chart
        if yes("Do you want to see the most popular tweets ranking bar chart based on each tweet's likes?"):
            dataforplot = creatdata(twitterdata)
            plotbarchart(dataforplot, city, keywords)

        ## Plot the pie chart
        if yes("Do you want to see the percentage of each source takes?"):
            sorted_newsdic = sortbysource(newsdata)
            dicforpie = createdataforpie(sorted_newsdic, len(newsdata))
            y = np.array([i for i in dicforpie.values()])
            mylabels = [i for i in dicforpie.keys()]
            plt.pie(y, labels = mylabels)
            plt.title(f'Percentage of each source about {keywords} in {city}')
            plt.show()

        rc.save_cache(cache)

if __name__ == '__main__':
    main()
