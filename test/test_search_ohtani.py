"""Test searching for Ohtani using the MCP tool."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from baseball_mcp_server import search_npb_player, get_npb_player_stats


async def test_search_and_stats():
    """Search for Ohtani and get his stats."""
    print("Searching for Shohei Ohtani...")
    print("=" * 60)
    
    # Search for Ohtani
    search_result = await search_npb_player("Shohei Ohtani")
    print(search_result)
    
    # Also try searching for "Otani"
    print("\n\nSearching for 'Otani'...")
    print("=" * 60)
    search_result2 = await search_npb_player("Otani")
    print(search_result2)
    
    # If we found him, get his stats
    print("\n\nTrying to get stats with player ID 'otani,_shohei'...")
    print("=" * 60)
    stats = await get_npb_player_stats("otani,_shohei", "2017")
    print(stats)


if __name__ == "__main__":
    asyncio.run(test_search_and_stats())