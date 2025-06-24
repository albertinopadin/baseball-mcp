#!/usr/bin/env python3
"""Test the smart player selection feature for NPB searches."""

import asyncio
import sys
sys.path.insert(0, '../src')

from npb_api import search_npb_player, get_npb_player_stats


async def test_alex_cabrera():
    """Test that Alex Cabrera is automatically selected when multiple matches exist."""
    print("Testing Alex Cabrera search with smart selection...\n")
    
    # Search for Alex Cabrera
    result = await search_npb_player('Alex Cabrera')
    print(result)
    
    # If the smart selection worked, we should get a single player result
    if "Auto-selected" in result or "ID: br_cabrer001ale" in result:
        print("\n✅ SUCCESS: Smart selection found the correct Alex Cabrera!")
        
        # Get his stats to verify
        print("\nGetting career stats...")
        stats = await get_npb_player_stats('br_cabrer001ale', None, 'batting')
        if "HR: 375" in stats:
            print("✅ Verified: Found Alex Cabrera's 375 NPB home runs!")
        else:
            print("❌ Stats don't match expected values")
    else:
        print("\n❌ FAILED: Smart selection did not work as expected")


async def test_multiple_with_stats():
    """Test a case where multiple players might have NPB stats."""
    print("\n\nTesting with a common name that might have multiple NPB players...\n")
    
    # Try a common Japanese surname
    result = await search_npb_player('Yamada')
    print(f"First 500 chars: {result[:500]}...")
    
    if "Found" in result and "players" in result:
        print("\n✅ Correctly showing multiple results when multiple players have stats")
    else:
        print("\n❓ Unexpected result format")


async def main():
    """Run all tests."""
    print("=== Smart NPB Player Selection Tests ===\n")
    
    await test_alex_cabrera()
    await test_multiple_with_stats()
    
    print("\n=== Tests Complete ===")


if __name__ == "__main__":
    asyncio.run(main())