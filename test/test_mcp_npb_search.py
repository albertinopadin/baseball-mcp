#!/usr/bin/env python3
"""Test MCP server NPB search functionality."""

import asyncio
import sys
sys.path.insert(0, '../src')

from baseball_mcp_server import search_player


async def test_npb_search():
    """Test NPB player search through MCP interface."""
    print("Testing NPB search through MCP server...\n")
    
    # Test 1: Alex Cabrera with NPB sport_id
    print("=== Test 1: Alex Cabrera (sport_id=31) ===")
    result = await search_player("Alex Cabrera", sport_id=31)
    print(result)
    
    if "br_cabrer001ale" in result:
        print("\n✅ SUCCESS: Found Alex Cabrera in NPB search")
    else:
        print("\n❌ FAILED: Did not find Alex Cabrera")
    
    # Test 2: Ichiro with NPB sport_id
    print("\n\n=== Test 2: Ichiro Suzuki (sport_id=31) ===")
    result = await search_player("Ichiro Suzuki", sport_id=31)
    print(result[:300] + "..." if len(result) > 300 else result)
    
    if "br_suzuki001ich" in result:
        print("\n✅ SUCCESS: Found Ichiro in NPB search")
    else:
        print("\n❌ FAILED: Did not find Ichiro")
    
    # Test 3: Current NPB player
    print("\n\n=== Test 3: Munetaka Murakami (sport_id=31) ===")
    result = await search_player("Munetaka Murakami", sport_id=31)
    print(result[:300] + "..." if len(result) > 300 else result)
    
    if "Murakami" in result:
        print("\n✅ SUCCESS: Found Murakami in NPB search")
    else:
        print("\n❌ FAILED: Did not find Murakami")


async def main():
    """Run all tests."""
    await test_npb_search()
    print("\n=== MCP NPB Search Tests Complete ===")


if __name__ == "__main__":
    asyncio.run(main())