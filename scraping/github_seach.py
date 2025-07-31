import requests

def search_github_users(keyword, max_users=10):
    url = f"https://api.github.com/search/users?q={keyword}+in:bio"
    res = requests.get(url)
    users = res.json().get("items", [])[:max_users]
    results = []
    for u in users:
        results.append({
            "title": u["login"],
            "url": u["html_url"]
        })
    return results
