import requests
from bs4 import BeautifulSoup

def search_duckduckgo(query, num_results=10):
    url = f"https://html.duckduckgo.com/html?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.post(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    results = []
    for result in soup.select(".result"):
        title = result.select_one(".result__title")
        link = result.select_one("a.result__url")
        if title and link:
            results.append({
                "title": title.get_text(strip=True),
                "url": link["href"]
            })
        if len(results) >= num_results:
            break
    return results
