from scraping.lead_scraper import scrape_leads
from processing.cleaner import clean_leads
from storage.excel_writer import save_to_excel,save_to_csv
from analysis.analyzer import analyze_leads
from ai_agent.suggestor import suggest_actions

def main():
    print("🔍 Scraping leads...")
    leads = scrape_leads()

    print("🧹 Cleaning leads...")
    cleaned = clean_leads(leads)
    #
    print("📊 Analyzing leads...")
    analyzed = analyze_leads(cleaned)
    #
    print("🤖 Suggesting actions...")
    with_actions = suggest_actions(analyzed)
    #
    print("💾 Saving to Excel...")
    save_to_excel(with_actions)

    print("✅ Done! Leads saved to leads.xlsx")

if __name__ == "__main__":
    main()
