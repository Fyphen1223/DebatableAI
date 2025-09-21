import asyncio
import requests
import os


async def search(query: str, num_results: int = 5):
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
        "limit": num_results,
        "scrapeOptions": {"formats": ["links"]},
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    return response.json()


async def scrape(url: str):
    """Perform a simple web scrape and return a web page content formatted in Markdown.

    Returns:
                        response.json()["data"]["markdown"]: Markdown formatted content of the webpage.
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
