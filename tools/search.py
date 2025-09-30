import asyncio
import requests
import os
from urllib.parse import quote


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


def format_cinii_results(cinii_json: dict) -> str:
    """
    CiNiiの検索結果(JSON)を、論文情報のリスト文字列に変換します。
    """
    if not cinii_json or "items" not in cinii_json or not cinii_json["items"]:
        return "関連する論文は見つかりませんでした。"

    papers_list = []
    for item in cinii_json.get("items", []):
        title = item.get("title", "タイトルなし")
        link = item.get("link", {}).get("@id", "リンクなし")

        authors = item.get("dc:creator")
        if isinstance(authors, list):
            authors_str = ", ".join(authors)
        else:
            authors_str = "著者情報なし"

        publisher = item.get("dc:publisher", "大学/出版社情報なし")
        publication_name = item.get("prism:publicationName", "出版物名なし")
        publication_date = item.get("prism:publicationDate", "日付なし")
        description = item.get("description", "概要なし")

        source_links = item.get("dc:source", [])
        source_links_str = "\n".join([source.get("@id", "") for source in source_links])

        paper_info = (
            f"Title: {title}\n"
            f"Authors: {authors_str}\n"
            f"Publisher: {publisher}\n"
            f"Publication: {publication_name} ({publication_date})\n"
            f"Link: {link}\n"
            f"Source Links:\n{source_links_str}\n"
            f"Summary: {description}"
        )
        papers_list.append(paper_info)

    return "\n\n---\n\n".join(papers_list)


def scrape(url: str):
    """Perform a simple web scrape and return a web page content formatted in Markdown This function can be used with normal web page, PDF, etc.

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
    print("[Tool: scrape] Scraping tool was used with URL:", url)
    return response.json()["data"]["markdown"]


def searchCiNii(query: str, num_results: int = 10):
    """Perform a search on CiNii and return a list of result URLs.

    Returns:
                    list[str]: list of result URLs (length <= num_results).
                    If an error occurs, returns a single-item list with an error message.
    """
    encoded_query = quote(query, safe="")
    url = f"http://cir.nii.ac.jp/opensearch/articles?q={encoded_query}&count={num_results}&start=1&hasLinkToFullText=true&lang=ja,en&format=json&appid={os.getenv('CINII_APPLICATION_ID')}"
    print("[Tool: searchCiNii] Searching CiNii with URL:", url)
    response = requests.get(url)
    if response.status_code != 200:
        return [f"Error: Received status code {response.status_code} from CiNii"]
    else:
        return format_cinii_results(response.json())


def searchCORE(query: str, num_results: int = 10):
    """Perform a search on CORE and return a list of result URLs.

    Returns:
                                    list[str]: list of result URLs (length <= num_results).
                                    If an error occurs, returns a single-item list with an error message.
    """
    encoded_query = quote(query, safe="")
    url = f"https://api.core.ac.uk/v3/search/works?query={encoded_query}&page=1&pageSize={num_results}&apiKey={os.getenv('CORE_API_KEY')}"
    print("[Tool: searchCORE] Searching CORE with URL:", url)
    response = requests.get(url)
    if response.status_code != 200:
        return [f"Error: Received status code {response.status_code} from CORE"]
    else:
        results = response.json().get("results", [])
        if not results:
            return ["No relevant papers found."]
        papers_list = []
        for item in results:
            title = item.get("title", "No title")
            link = item.get("fullTextUrl", ["No link"])[0]
            authors = item.get("authors", ["No authors"])
            authors_str = ", ".join(authors) if isinstance(authors, list) else authors
            publication_date = item.get("publishedDate", "No date")
            description = item.get("abstract", "No abstract")

            paper_info = (
                f"Title: {title}\n"
                f"Authors: {authors_str}\n"
                f"Publication Date: {publication_date}\n"
                f"Link: {link}\n"
                f"Summary: {description}"
            )
            papers_list.append(paper_info)
        return "\n\n---\n\n".join(papers_list)


def rotateProxy():
    # Placeholder for future proxy rotation logic.
    return None
