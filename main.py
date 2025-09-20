import asyncio
import parlant.sdk as p
from datetime import datetime
from words import add_domain_glossary
from tools.search import searchWebOrganic, scrape
from tools.conditions import searchCondition


@p.tool
async def summarize(context: p.ToolContext, text: str) -> p.ToolResult:
    return p.ToolResult(data=f"Summary of the text: {text[:30]}...\n")


@p.tool
async def getContent(context: p.ToolContext, url: str) -> p.ToolResult:
    return p.ToolResult(data=f"Content fetched from {url}\n")


@p.tool
async def searchWeb(context: p.ToolContext, query: str) -> p.ToolResult:
    return p.ToolResult(
        data=f"Search results for {query}\n 1: Website 1's Title, Snipper, URL\n 2: Website 2's Title, Snipper, URL"
    )


@p.tool
async def scrapeWeb(context: p.ToolContext, url: str) -> p.ToolResult:
    content = await scrape(url)
    return p.ToolResult(data=content)


async def main():
    async with p.Server(
        nlp_service=p.NLPServices.gemini,
        session_store="local",  # Change this to your desired model
    ) as server:
        agent = await server.create_agent(
            name="Mr.D",
            description="You are a skilled and well-trained debater. You focus on presenting logical arguments, counterarguments, researching papers.\nUse the same language as the user. Be as concise as possible.",
        )
        await agent.attach_tool(condition=searchCondition, tool=scrapeWeb)
        await add_domain_glossary(agent)


asyncio.run(main())
