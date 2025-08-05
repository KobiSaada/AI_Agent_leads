from setuptools import setup, find_packages

setup(
    name='ai_agent_leads',
    version='0.1.0',
    description='Smart AI Agent with multi-source scraping from scrape_up',
    author='Your Name',
    packages=find_packages(include=[
        "scrape_up",
        "scrape_up.*",
        "ai_agent",
        "ai_agent.*",
        "analysis",
        "analysis.*",
        "scraping",
        "scraping.*",
        "processing",
        "processing.*",
        "storage",
        "storage.*",
    ]),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "lxml",
        "langchain",
        "langchain-community",
        "ollama",
        "openai",
        "scrapy"
    ],
    python_requires=">=3.8",
)
