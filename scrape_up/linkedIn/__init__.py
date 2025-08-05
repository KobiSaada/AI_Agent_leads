import asyncio
from playwright.async_api import async_playwright


class LinkedinScraper:
    def __init__(self):
        self.email = "kobisaada054@gmail.com"  # שים בקובץ .env אם זה production
        self.password = "Kobian054"

    async def _login(self, page):
        await page.goto("https://www.linkedin.com/login")
        await page.fill('input[name="session_key"]', self.email)
        await page.fill('input[name="session_password"]', self.password)
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("networkidle")

    async def _scrape_profile(self, page, url):
        try:
            await page.goto(url, timeout=60000)
            await page.wait_for_selector("h1", timeout=15000)
            await page.mouse.wheel(0, 6000)
            await page.wait_for_timeout(2000)

            name = await page.locator("h1").text_content()
            location = await page.locator("span.text-body-small").first.text_content()

            return {
                "url": url,
                "name": name.strip() if name else "",
                "location": location.strip() if location else "",
            }
        except Exception as e:
            print(f"❌ Failed to scrape profile {url}: {e}")
            return {}

    async def _search_profiles(self, keywords):
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await self._login(page)

            for keyword in keywords:
                search_url = f"https://www.linkedin.com/search/results/people/?keywords={keyword}"
                print(f"🔍 Searching: {search_url}")
                await page.goto(search_url)
                await page.wait_for_timeout(5000)

                profile_links = await page.locator("a.app-aware-link").all()
                seen = set()
                for link in profile_links:
                    href = await link.get_attribute("href")
                    if href and "/in/" in href and href not in seen:
                        seen.add(href)
                        profile_data = await self._scrape_profile(page, href)
                        if profile_data:
                            results.append(profile_data)
                        if len(results) >= 3:  # אפשר להגדיל
                            break

            await browser.close()
        return results

    def search(self, keyword):
        keywords = [keyword] if isinstance(keyword, str) else keyword
        return asyncio.run(self._search_profiles(keywords))
