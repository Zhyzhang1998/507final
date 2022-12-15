# SI507 Final Project
You can use this program to find the Twttier and News trend of specific keywords and city.

## How to supply API keys
- TwitterAPI (6)
  - Document links: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
  - Apply API: https://developer.twitter.com/en/apply-for-access
  - Endpoint: https://api.twitter.com/1.1/search/tweets.json
- NewsAPI (2)
  - Document links: https://newsapi.org/docs/endpoints/everything
  - Apply API: https://newsapi.org/account
  - Endpoint: https://newsapi.org/v2/everything
- Save the keys and tokens to ./secret.py
- Challenge score: 6 + 2 = 8

## How to run
1. install all requirements with `pip install -r requirements.txt`
2. run with `python final.py`

## Data Structure
1. I organized data into a tree.
2. [Data_structure](data_structure.png)

## How to use
They program will:
1. Ask the user which city they want to know
2. Ask the user to give the keywords they want to know
3. Ask whether to print out the results in the form of a tree
4. Ask whether to open the url in web browser
5. Ask if users want to see the word cloud diagram based on the most common words from the text.
6. Ask if users want to see the most popular tweets ranking bar chart based on each tweet's likes?
7. Ask if users want to see the percentage of each source takes.
Steps 3, 4, 5, 6, 7 will allow users to decide and select whether to display data.

## Project Demo

