import os

from tools.search import search, scrape, searchCiNii

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

from haystack.tools import ComponentTool
from duckduckgo_api_haystack import DuckduckgoApiWebSearch


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
    system_prompt=r"You are a skilled and well-trained debater. You focus on presenting logical arguments, counterarguments, researching papers.\nUse the same language as the user. Be extremely concise.\nFollow these rules to complete the task:\n1. Always use scrape_web tool to access ACTUAL papers when user requests to search for it. DO NOT USE CiNii search result's summary as text for report to the user.\nIT IS EXTREMELY IMPORTANT THAT YOU DO NOT SEARCH FOR PAPERS WITHOUT ACCESSING THE ACTUAL PAPER.\n2. Tip for searching in CiNii: Do not use too straight-forward keywords. Being abstractive might work. Limiting keywords length to under 2 words might be important.",
    tools=[scrape_tool, search_cinii_tool]
)


from haystack.dataclasses.streaming_chunk import StreamingChunk


def on_stream(chunk: StreamingChunk):
    content = chunk.content
    text = None
    if isinstance(content, (bytes, bytearray)):
        # まずUTF-8で試す
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            # 自動判別（charset-normalizer推奨）
            try:
                from charset_normalizer import from_bytes

                best = from_bytes(content).best()
                if best is not None:
                    text = str(best)  # str(best) はデコード済みテキスト
            except Exception:
                pass
            # それでもだめなら無難に置換
            if text is None:
                text = content.decode("utf-8", errors="replace")
    else:
        text = str(content) if content is not None else ""

    # メタ情報やfinish_reasonもお好みで
    if getattr(chunk, "meta", None):
        print(f"[meta] {chunk.meta}")
    if getattr(chunk, "finish_reason", None):
        return
        print(f"[finish_reason={chunk.finish_reason}]")
    if text:
        print(text, end="", flush=True)


mainAgent.warm_up()
result = mainAgent.run(
    messages=[
        ChatMessage.from_user(
            "以下の指示に従え。1.CiNiiで、司法取引の虚偽供述のリスクに関する論文を探す。2.そのページにアクセスし、実際にその論文のPDF等が公開されているページにアクセスしてその論文を読み、司法取引の虚偽供述のリスクは大きい、という趣旨の資料を探せ。あればユーザーにURLとその文章を報告せよ。きちんとそういうことを言っている文章を引用せよ。3.もし見つからなければ、キーワードを変えてCiNiiで検索をするところからやり直せ。"
        )
    ],
    exit_conditions=["end_session"],
    max_agent_steps=100,
#    streaming_callback=on_stream,
)

print("-----\n")
print(result["messages"][-1].text)
