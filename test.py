import requests


def scrape(url: str):
    """Perform a simple web scrape and return a list of result URLs.

    Returns:
                        response.json(): JSON response from the scraping service.
    """
    firecrawl_url = "http://localhost:3002/v2/scrape"
    print(url)
    payload = {
        "url": url,
        "formats": ["markdown"],
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(firecrawl_url, json=payload, headers=headers)
    return response.json()["data"]["markdown"]


print(scrape("https://example.com"))
