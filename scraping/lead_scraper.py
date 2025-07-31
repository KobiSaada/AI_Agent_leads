from scraping.scrape_router import scrape_all_sources


from Ai_Agents.ai_agent.prompt_parser.parser import  expand_prompt

def scrape_leads():
    user_query = input("🔍 מה תרצה לחפש? >> ")
    keywords = expand_prompt(user_query)

    print(f"\n🧠 מילות מפתח שזוהו: {keywords}")
    raw_results = scrape_all_sources(keywords)

    leads = []

    for keyword, sources in raw_results.items():
        for source_name, entries in sources.items():
            for entry in entries:
                leads.append({
                    "source": source_name,
                    "keyword": keyword,
                    "title": entry.get("title"),
                    "url": entry.get("url")
                })

    print(leads)
    return leads
