import asyncio
from playwright.async_api import async_playwright
import json

COOKIE_FILE = "linkedin_cookies.json"

async def save_linkedin_cookies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.linkedin.com/login")
        print("🔐 היכנס עם שם משתמש וסיסמה. לאחר ההתחברות – לחץ Enter כאן.")
        input("▶️ לאחר התחברות מלאה והופעת פיד לינקדאין – לחץ Enter להמשך...")

        cookies = await context.cookies()
        with open(COOKIE_FILE, "w") as f:
            json.dump(cookies, f)

        await browser.close()
        print("✅ קובץ קוקיז נשמר:", COOKIE_FILE)

if __name__ == "__main__":
    asyncio.run(save_linkedin_cookies())
