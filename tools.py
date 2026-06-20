from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from langchain_community.tools import DuckDuckGoSearchResults
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()



@tool("Web_Search_Tool")
def web_search(query: str) -> str:
    """
    Performs a web search using DuckDuckGo and returns results.
    Returns title, URL, and snippet.
    """

    search = DuckDuckGoSearchResults(
        output_format="list",   # returns structured list
        max_results=5
    )

    results = search.invoke(query)

    out = []

    for r in results:
        out.append(
            f"Title: {r['title']}\nURL: {r['link']}\nSnippet: {r['snippet'][:300]}\n"
        )

    return "\n----\n".join(out)


# print(web_search.invoke("War update in Russia and Ukraine"))


@tool("Scrape_urls")
def scrape_urls(url: str) -> str:
    """
    Scrape and return clean text content from a given URL for deeper reading.
    """
    
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
            
# print(scrape_urls.invoke("https://www.hindustantimes.com/cricket/gt-vs-srh-live-cricket-score-ipl-2026-gujarat-titans-vs-sunrisers-hyderabad-match-today-12-may-latest-scorecard-101778582003529.html"))

            
            
