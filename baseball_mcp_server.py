from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from data_utils import format_player_data

BASE_URL = "https://statsapi.mlb.com/api/v1"
USER_AGENT = "baseball-mcp-server/1.0"

mcp = FastMCP("BaseballMcp")

async def make_mlb_stats_request(url: str) -> dict[str, Any] | None:
    """Make a request to the MLB Stats API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        

@mcp.tool()
async def search_player(search_str: str)  -> str:
    """Search for MLB player.

    Args:
        search_str: Name of player to search for
    """
    url = f"{BASE_URL}/people/search?names={search_str}"
    data = await make_mlb_stats_request(url)

    if not data or "people" not in data:
        return f"Unable to search for {search_str} or no player found."

    if not data["people"]:
        return f"No player found for search string: {search_str}"

    player_results = [format_player_data(player) for player in data["people"]]
    return "\n---\n".join(player_results)


if __name__ == "__main__":
    print("Baseball Stats MCP Server v0.0.1")
    # Initialize and run the server
    mcp.run(transport='stdio')