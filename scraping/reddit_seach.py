import requests

def search_reddit(query, limit=10):
    url = f"https://www.reddit.com/search.json?q={query}&limit={limit}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    data = res.json()

    results = []
    for post in data["data"]["children"]:
        title = post["data"]["title"]
        link = "https://reddit.com" + post["data"]["permalink"]
        results.append({"title": title, "url": link})
    return results
