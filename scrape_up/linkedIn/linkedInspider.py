import asyncio
from playwright.async_api import async_playwright
import json

LINKEDIN_EMAIL = "kobisaada054@gmail.com"
LINKEDIN_PASSWORD = "Kobian054"
PROFILE_URLS = [
    "https://www.linkedin.com/in//",
    # תוכל להוסיף כאן עמודים של חברות או משרות בהמשך
]


async def extract_about(page):
    try:
        about_handle = page.locator('section.pv-about-section')
        if await about_handle.is_visible():
            return await about_handle.inner_text()
    except:
        pass
    return ""


async def extract_experience(page):
    experience_data = []
    try:
        await page.locator("#experience").scroll_into_view_if_needed()
        await page.wait_for_selector("li.pvs-list__paged-list-item")
        experience_blocks = page.locator("#experience li.pvs-list__paged-list-item")
        count = await experience_blocks.count()
        for i in range(count):
            item = experience_blocks.nth(i)
            position = await item.locator("span[aria-hidden='true']").first.text_content()
            org = await item.locator("span.t-14.t-normal").first.text_content()
            experience_data.append({
                "position": position.strip() if position else "",
                "organization": org.strip() if org else ""
            })
    except:
        pass
    return experience_data


async def extract_education(page):
    education_data = []
    try:
        await page.locator("#education").scroll_into_view_if_needed()
        await page.wait_for_selector("li.pvs-list__paged-list-item")
        edu_blocks = page.locator("#education li.pvs-list__paged-list-item")
        count = await edu_blocks.count()
        for i in range(count):
            item = edu_blocks.nth(i)
            school = await item.locator("span[aria-hidden='true']").first.text_content()
            degree = await item.locator("span.t-14.t-normal").first.text_content()
            education_data.append({
                "school": school.strip() if school else "",
                "degree": degree.strip() if degree else ""
            })
    except:
        pass
    return education_data


async def scrape_profile(page, url):
    await page.goto(url, timeout=60000)
    await page.wait_for_selector("h1", timeout=15000)
    await page.mouse.wheel(0, 6000)
    await page.wait_for_timeout(2000)  # להמתין לטעינה דינמית

    name = await page.locator("h1").text_content()
    location = await page.locator("span.text-body-small").first.text_content()

    connections = ""
    try:
        all_spans = await page.locator("span.top-card__subline-item").all()
        for el in all_spans:
            text = await el.text_content()
            if "connections" in text:
                connections = text.strip()
    except:
        pass

    # --- About Section ---
    about = ""
    try:
        await page.locator("section:has-text('About')").scroll_into_view_if_needed()
        await page.wait_for_timeout(1000)
        about = await page.locator("section:has-text('About') span.visually-hidden").first.text_content()
    except:
        pass

    # --- Experience Section ---
    experience = []
    try:
        exp_section = page.locator("section:has(h2:has-text('Experience')) li")
        count = await exp_section.count()
        for i in range(count):
            item = exp_section.nth(i)
            try:
                position = await item.locator("span[aria-hidden='true']").first.text_content()
                company = await item.locator("span.t-14.t-normal").first.text_content()
                experience.append({
                    "position": position.strip() if position else "",
                    "organization": company.strip() if company else ""
                })
            except:
                continue
    except:
        pass

    # --- Education Section ---
    education = []
    try:
        edu_section = page.locator("section:has(h2:has-text('Education')) li")
        count = await edu_section.count()
        for i in range(count):
            item = edu_section.nth(i)
            try:
                school = await item.locator("span[aria-hidden='true']").first.text_content()
                degree = await item.locator("span.t-14.t-normal").first.text_content()
                education.append({
                    "school": school.strip() if school else "",
                    "degree": degree.strip() if degree else ""
                })
            except:
                continue
    except:
        pass

    return {
        "url": url,
        "name": name.strip() if name else "",
        "location": location.strip() if location else "",
        "connections": connections,
        "about": about.strip() if about else "",
        "experience": experience,
        "education": education,
    }



async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.linkedin.com/login")
        await page.fill('input[name="session_key"]', LINKEDIN_EMAIL)
        await page.fill('input[name="session_password"]', LINKEDIN_PASSWORD)
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("networkidle")

        results = []
        for url in PROFILE_URLS:
            try:
                profile_data = await scrape_profile(page, url)
                results.append(profile_data)
            except Exception as e:
                print(f"Failed to scrape {url}: {e}")

        with open("linkedin_profiles.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
