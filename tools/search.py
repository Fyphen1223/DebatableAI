import parlant.sdk as p
import asyncio
import requests
import os


async def searchWeb(context: p.ToolContext, query: str) -> p.ToolResult:
    return p.ToolResult(
        data=f"Search results for {query}\n 1: Website 1's Title, Snippet, URL\n 2: Website 2's Title, Snippet, URL"
    )


async def searchWebOrganic(query: str, num_results: int = 5):
    """Perform a simple web search and return a list of result URLs.

    This function wraps the blocking `googlesearch.search` call in
    `asyncio.to_thread` so it can be awaited from async code.

    Returns:
            list[str]: list of result URLs (length <= num_results).
            If an error occurs, returns a single-item list with an error message.
    """
    url = "http://localhost:3002/v2/search"
    payload = {
        "query": query,
        "sources": ["web"],
        "categories": [],
        "limit": 10,
        "scrapeOptions": {
            "onlyMainContent": True,
            "maxAge": 172800000,
            "parsers": ["pdf"],
            "formats": [],
        },
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('FIRECRAWL_API_KEY')}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


async def scrape(url: str):
    """Perform a simple web scrape and return a list of result URLs.

    Returns:
                        response.json(): JSON response from the scraping service.
    """
    firecrawl_url = "http://localhost:3002/v2/scrape"
    payload = {
        "url": url,
        "formats": ["markdown"],
    }
    headers = {
        "Content-Type": "application/json",
        "waitFor": "2000",
        "timeout": "5000",
    }
    response = requests.post(firecrawl_url, json=payload, headers=headers)
    return response.json()["data"]["markdown"]


def rotateProxy():
    # Placeholder for future proxy rotation logic.
    return None
