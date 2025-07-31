from scraping.google_search import search_google
from scraping.ddg_search import search_duckduckgo
from scraping.reddit_seach import search_reddit
from scraping.twitter_search import search_twitter_profiles
from scraping.github_seach import search_github_users
from scraping.crunchbase import search_crunchbase
#from scraping.instagram_seach import search_instagram_bios
from scraping.linkedln_search import search_linkedin_profiles

import os
from dotenv import load_dotenv
load_dotenv()

def scrape_all_sources(keywords: list[str]) -> dict:
    all_results = {}

    for keyword in keywords:
        print(f"\n🔍 מחפש את '{keyword}'...")

        try:
            all_results[keyword] = {
                "linkedin": search_linkedin_profiles(keyword),
                "google": search_google(keyword),
                "duckduckgo": search_duckduckgo(keyword),
                "reddit": search_reddit(keyword),
                "twitter": search_twitter_profiles(keyword, bearer_token=os.getenv("TWITTER_BEARER")),
                "github": search_github_users(keyword),
                "crunchbase": search_crunchbase(keyword),

            }
        except Exception as e:
            print(f"⚠️ שגיאה עבור '{keyword}': {e}")
            continue

    return all_results
