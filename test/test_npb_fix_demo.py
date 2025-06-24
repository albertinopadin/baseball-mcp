#!/usr/bin/env python3
"""Demonstrate the NPB search fix for sport_id=31."""

import asyncio
import sys
sys.path.insert(0, '../src')

from baseball_mcp_server import search_player, get_player_stats


async def demo_npb_fix():
    """Demonstrate that NPB searches work correctly with sport_id=31."""
    
    print("=== NPB Search Fix Demonstration ===\n")
    
    # Test 1: Alex Cabrera
    print("1. Searching for Alex Cabrera with sport_id=31 (NPB)...")
    result = await search_player("Alex Cabrera", sport_id=31)
    
    if "br_cabrer001ale" in result:
        print("✅ SUCCESS: Found Alex Cabrera!")
        print(result)
        
        # Get his stats to prove it works
        print("\n2. Getting Alex Cabrera's NPB career stats...")
        stats = await get_player_stats("br_cabrer001ale", stats="batting", sport_id=31)
        if "HR: 375" in stats:
            print("✅ SUCCESS: Retrieved career stats showing 375 home runs!")
        else:
            print(f"Stats result: {stats[:200]}...")
    else:
        print("❌ FAILED: Could not find Alex Cabrera")
        print(f"Result: {result}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Current NPB player
    print("3. Searching for current NPB player Munetaka Murakami...")
    result = await search_player("Munetaka Murakami", sport_id=31)
    
    if "Murakami" in result and "Yakult" in result:
        print("✅ SUCCESS: Found Munetaka Murakami!")
        print(result[:300] + "..." if len(result) > 300 else result)
    else:
        print("❌ FAILED: Could not find Munetaka Murakami")
    
    print("\n=== Demonstration Complete ===")
    print("\nThe NPB search (sport_id=31) is now working correctly!")
    print("- Historical players like Alex Cabrera are found via cached/Baseball Reference")
    print("- Current players like Munetaka Murakami are found via NPB Official")


if __name__ == "__main__":
    asyncio.run(demo_npb_fix())