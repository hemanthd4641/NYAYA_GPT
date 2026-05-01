# tools/state_law_search_tool.py

import os
from dotenv import load_dotenv
from crewai.tools import tool
from tavily import TavilyClient

load_dotenv()

@tool("State Law Variations Tool")
def state_law_variations_tool(query: str) -> str:
    """
    Use this tool to search the internet for specific state-level amendments 
    or variations of Indian central laws (like IPC, CrPC) in a specific state.
    Provide a clear search query like: "Maharashtra amendment to IPC Section 302"
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key or api_key == "tvly-placeholder":
        return "Warning: TAVILY_API_KEY is missing or invalid. Cannot search for state laws."

    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(
            query=query,
            search_depth="basic",
            max_results=3
        )
        results = [item["content"] for item in response.get("results", [])]
        if results:
            return "\n\n".join(results)
        return "No specific state amendments found."
    except Exception as e:
        return f"Error searching for state laws: {str(e)}"
