from haystack_integrations.tools.mcp import MCPToolset, StreamableHttpServerInfo

server_info = StreamableHttpServerInfo(url="http://localhost:8931/mcp")

toolset = MCPToolset(server_info=server_info, tool_names=["browser_navigate"])

print(toolset.tools)
