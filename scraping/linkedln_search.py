import asyncio
from playwright.async_api import async_playwright
import json

COOKIE_FILE = "linkedin_cookies.json"

async def search_linkedin(keyword, max_results=10):
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        # טעינת קוקיז
        try:
            with open(COOKIE_FILE, "r") as f:
                cookies = json.load(f)
                await context.add_cookies(cookies)
        except FileNotFoundError:
            print("⚠️ קובץ קוקיז לא נמצא. הרץ קודם את save_linkedin_cookies.py")
            return []

        page = await context.new_page()

        search_url = f"https://www.linkedin.com/search/results/people/?keywords={keyword.replace(' ', '%20')}"
        await page.goto(search_url)

        await page.wait_for_timeout(5000)

        profiles = await page.query_selector_all("div.entity-result__content")

        for profile in profiles[:max_results]:
            try:
                name = await profile.query_selector("span[aria-hidden='true']")
                title = await profile.query_selector("div.entity-result__primary-subtitle")
                link_el = await profile.query_selector("a.app-aware-link")

                profile_data = {
                    "title": await name.inner_text() if name else "",
                    "url": await link_el.get_attribute("href") if link_el else "",
                    "company": await title.inner_text() if title else "",
                    "source": "linkedin"
                }
                results.append(profile_data)
            except:
                continue

        await browser.close()
        return results

# עוטף לגרסה סינכרונית:
def search_linkedin_profiles(keyword: str, max_results: int = 10):
    return asyncio.run(search_linkedin(keyword, max_results))
