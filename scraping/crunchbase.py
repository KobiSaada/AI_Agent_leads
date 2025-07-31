import requests
from bs4 import BeautifulSoup

def search_crunchbase(keyword, max_results=10):
    url = f"https://www.crunchbase.com/search/organization.companies/field/organizations/keywords/{keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    results = []
    for item in soup.select("a.cb-link"):
        title = item.get_text()
        link = "https://www.crunchbase.com" + item.get("href", "")
        results.append({"title": title, "url": link})
        if len(results) >= max_results:
            break
    return results
