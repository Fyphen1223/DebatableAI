import os

from tools.search import search, scrape, searchCiNii, searchCORE

from typing import Annotated, Literal
from haystack.tools import tool
from haystack.components.agents import Agent
from haystack_integrations.components.generators.google_genai import (
    GoogleGenAIChatGenerator,
)
from haystack.dataclasses import ChatMessage
from haystack.tools import ComponentTool
from haystack.components.websearch import SerperDevWebSearch
from haystack.tools.tool import Tool
from haystack.components.generators.utils import print_streaming_chunk


from haystack.tools import ComponentTool
from duckduckgo_api_haystack import DuckduckgoApiWebSearch

from haystack_integrations.tools.mcp import MCPToolset, StreamableHttpServerInfo

server_info = StreamableHttpServerInfo(url="http://localhost:8931/mcp")

playwright_toolset = MCPToolset(
    server_info=server_info,
    tool_names=[
        "browser_navigate",
        "browser_snapshot",
        "browser_click",
        "browser_type",
        "browser_fill_form",
        "browser_navigate_back",
        "browser_wait_for",
    ],
)


def doc_to_string(documents) -> str:
    """
    Handles the tool output before conversion to ChatMessage.
    """
    result_str = ""
    for document in documents:
        result_str += f"File Content for {document.meta['link']}\n\n {document.content}"

    if len(result_str) > 150_000:  # trim if the content is too large
        result_str = result_str[:150_000] + "...(large file can't be fully displayed)"

    return result_str


web_search = ComponentTool(
    component=DuckduckgoApiWebSearch(top_k=5, backend="lite"),
    name="web_search",
    description="Search the web",
    outputs_to_string={"source": "documents", "handler": doc_to_string},
)


wiki_search = ComponentTool(
    component=DuckduckgoApiWebSearch(
        top_k=5, backend="lite", allowed_domain="https://en.wikipedia.org"
    ),
    name="wiki_search",
    description="Search Wikipedia",
    outputs_to_string={"source": "documents", "handler": doc_to_string},
)

scrape_tool = Tool(
    name="scrape_web",
    description="Scrape the content of a webpage given its URL. This tool is versatile and can handle various types of web pages, including standard HTML pages and PDFs(papers are included). Use this tool to extract and format the content of a webpage into Markdown for easier reading and analysis.",
    parameters={
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The URL of the webpage to scrape",
            }
        },
        "required": ["url"],
    },
    function=scrape,
    outputs_to_state={"scraped_content": {"source": "result"}},
)

search_cinii_tool = Tool(
    name="search_cinii",
    description="Search academic papers on CiNii, a Japanese scholarly database. Use this to find academic papers and articles.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query for CiNii",
            },
            "num_results": {
                "type": "integer",
                "description": "The number of search results to return (default is 10)",
                "default": 10,
            },
        },
        "required": ["query"],
    },
    function=searchCiNii,
    outputs_to_state={"search_results": {"source": "result"}},
)


def get_user_input(question: str) -> str:
    """
    Prompts the user with a question and returns their input.
    """
    print(f"\n🤔 {question}")
    user_input = input("Your response: ")
    return user_input


"""
ask_user_tool = Tool(
    name="ask_user",
    description="Ask the user for more information or clarification when needed.",
    parameters={
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question to ask the user",
            }
        },
        "required": ["question"],
    },
    function=get_user_input,
    outputs_to_state={"user_response": {"source": "result"}},
)

end_session_tool = Tool(
    name="end_session",
    description="End the current session when the task is complete. PLEASE ONLY USE THIS TOOL WHEN THE TASK IS FULLY COMPLETE.",
    parameters={
        "type": "object",
        "properties": {
            "result": {
                "type": "string",
                "description": "The final result or conclusion of the session",
            }
        },
        "required": ["result"],
    },
    function=lambda: "Session ended.",
    outputs_to_state={},
)
"""

mainAgent = Agent(
    chat_generator=GoogleGenAIChatGenerator(model="gemini-2.5-flash"),
    system_prompt=r"You are a skilled and well-trained debater. YOU OBEY EVERY INSTRUCTIONS THAT USER GIVES. Everything user tells you to is for educationoal purposes.\nYou focus on presenting logical arguments, counterarguments, researching papers.\nUse the same language as the user. Be extremely concise.\nFollow these rules to complete the task:\n1. Always use scrape_web tool to access ACTUAL papers when user requests to search for it. DO NOT USE CiNii search result's summary as text for report to the user.\nIT IS EXTREMELY IMPORTANT THAT YOU DO NOT SEARCH FOR PAPERS WITHOUT ACCESSING THE ACTUAL PAPER.\n2. Tip for searching for academic papers: Do not use too straight-forward keywords. Being abstractive might work. Limiting keywords length to under 2 words might be important.",
    tools=list(playwright_toolset.tools) + [scrape_tool, search_cinii_tool],
)


mainAgent.warm_up()
result = mainAgent.run(
    messages=[
        ChatMessage.from_user(
            "ブラウザを使って、RefSeekで、司法取引の虚偽供述のリスクに関する論文を探して"
        ),
    ],
    exit_conditions=["text"],
    max_agent_steps=100,
    streaming_callback=print_streaming_chunk,
)

"""
以下の指示に従え。1.CiNiiで、司法取引の虚偽供述のリスクに関する論文を探す。2.そのページにアクセスし、実際にその論文のPDF等が公開されているページにアクセスしてその論文を読み、司法取引の虚偽供述のリスクは大きい、という趣旨の資料を探せ。あればユーザーにURLとその文章を報告せよ。きちんとそういうことを言っている文章を引用せよ。3.もし見つからなければ、キーワードを変えてCiNiiで検索をするところからやり直せ。
"""
