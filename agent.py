import os

from tools.search import search, scrape

from typing import Annotated, Literal
from haystack.tools import tool
from haystack.components.agents import Agent
from haystack_integrations.components.generators.google_genai import (
    GoogleGenAIChatGenerator,
)
from haystack.dataclasses import ChatMessage
from haystack.tools import ComponentTool
from haystack.components.websearch import SerperDevWebSearch

# search_tool = ComponentTool(component=SerperDevWebSearch())
scrapeTool = ComponentTool(
    component=scrape,
    parameters={
        "type": str,
        "properties": {"url": {"type": "string"}},
        "required": ["url"],
    },
    name="scrape",
    description="Useful for scraping the content of a webpage given its URL.",
)


@tool
async def scrapeContent(
    url: Annotated[str, "the URL of the webpage to scrape"],
):
    """A simple function to scrape the content of a webpage within Markdown."""
    content = await scrape(url)
    return content


mainAgent = Agent(
    chat_generator=GoogleGenAIChatGenerator(model="gemini-2.5-flash-lite"),
    system_prompt="You are a skilled and well-trained debater. You focus on presenting logical arguments, counterarguments, researching papers.\nUse the same language as the user. Be extremely concise.",
    tools=[scrapeTool],
)

researchAgent = Agent(
    chat_generator=GoogleGenAIChatGenerator(model="gemini-2.5-flash-lite"),
    system_prompt="You are a skilled and well-trained researcher. You focus on finding relevant information, papers, and data to support arguments.\nUse the same language as the user. Be extremely concise.",
    tools=[scrapeTool],
)

result = mainAgent.run(messages=[ChatMessage.from_user("自己紹介をしてください。")])

print(result["last_message"].text)
