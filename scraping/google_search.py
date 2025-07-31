
import requests
from bs4 import BeautifulSoup

def search_google(query, num_results=10):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={num_results}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    results = []
    for result in soup.select("div.g"):
        title = result.select_one("h3")
        link = result.select_one("a")
        if title and link:
            results.append({"title": title.text, "url": link['href']})
    return results
