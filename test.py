from tools.search import search, scrape, searchCiNii
import asyncio


async def main():
    print(
        await scrape(
            "https://www.jstage.jst.go.jp/article/pacjpa/87/0/87_1B-055-PE/_pdf"
        )
    )


asyncio.run(main())
