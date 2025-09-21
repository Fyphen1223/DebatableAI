from tools.search import search, scrape
import asyncio


async def main():
    print(await search("youtube"))


asyncio.run(main())
