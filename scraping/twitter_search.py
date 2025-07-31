import requests
import os

def search_twitter_profiles(keyword, bearer_token, max_results=10):
    url = f"https://api.twitter.com/2/tweets/search/recent?query={keyword}&max_results={max_results}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    res = requests.get(url, headers=headers)
    tweets = res.json()
    results = []
    for tweet in tweets.get("data", []):
        results.append({
            "title": tweet["text"],
            "url": f"https://twitter.com/i/web/status/{tweet['id']}"
        })
    return results
