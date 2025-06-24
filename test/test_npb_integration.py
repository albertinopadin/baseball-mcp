#!/usr/bin/env python3
"""Test script for NPB MCP integration."""

import asyncio
import sys
sys.path.insert(0, '/Users/albertinopadin/Desktop/Dev/Python Projects/baseball-mcp/src')

# Import the MCP tools directly
from baseball_mcp_server import search_player, get_player_stats, search_teams
from sports_constants import NIPPON_PROFESSIONAL as NPB


async def test_npb_mcp_integration():
    """Test NPB integration through MCP tools."""
    print("Testing NPB MCP Integration")
    print("=" * 50)
    
    # Test 1: Search for NPB teams
    print("\nTest 1: Getting NPB teams (sport_id=31)")
    teams_result = await search_teams(sport_id=NPB)
    print(teams_result)
    
    # Test 2: Search for NPB player (even though scraping not fully implemented)
    print("\nTest 2: Searching for NPB player 'Murakami' (sport_id=31)")
    player_result = await search_player("Murakami", sport_id=NPB)
    print(player_result)
    
    # Test 3: Try to get player stats (placeholder for now)
    print("\nTest 3: Getting NPB player stats")
    stats_result = await get_player_stats("npb_murakami_munetaka", stats="batting", sport_id=NPB)
    print(stats_result)
    
    # Test 4: Verify MLB still works
    print("\nTest 4: Verifying MLB search still works (sport_id=1)")
    mlb_player = await search_player("Aaron Judge", sport_id=1)
    print("MLB search result preview:", mlb_player[:200] + "..." if len(mlb_player) > 200 else mlb_player)
    
    print("\n" + "=" * 50)
    print("NPB MCP Integration tests completed!")


if __name__ == "__main__":
    asyncio.run(test_npb_mcp_integration())