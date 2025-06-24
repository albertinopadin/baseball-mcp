#!/usr/bin/env python3
"""Test year-by-year NPB stats functionality."""

import asyncio
import sys
sys.path.insert(0, '../src')

from baseball_mcp_server import search_player, get_player_stats


async def test_year_by_year_stats():
    """Test getting year-by-year NPB statistics."""
    
    print("=== NPB Year-by-Year Stats Test ===\n")
    
    # Test 1: Alex Cabrera year-by-year
    print("1. Getting Alex Cabrera's year-by-year NPB stats...")
    
    # First search for him
    search_result = await search_player("Alex Cabrera", sport_id=31)
    print("Search result:")
    print(search_result)
    
    print("\n2. Getting year-by-year stats using stats='yearByYear'...")
    yearly_stats = await get_player_stats(
        person_id="br_cabrer001ale",
        stats="yearByYear",
        sport_id=31
    )
    print(yearly_stats)
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Compare with career totals
    print("3. Getting career totals for comparison...")
    career_stats = await get_player_stats(
        person_id="br_cabrer001ale", 
        stats="batting",
        sport_id=31
    )
    print(career_stats[:500] + "..." if len(career_stats) > 500 else career_stats)
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: Try with an NPB Official player (should show not supported)
    print("4. Testing with NPB Official source player...")
    yearly_stats_npb = await get_player_stats(
        person_id="npb_murakami,_munetaka_2024",
        stats="yearByYear", 
        sport_id=31
    )
    print(yearly_stats_npb)


async def test_ichiro_year_by_year():
    """Test Ichiro's NPB career year-by-year."""
    print("\n\n=== Ichiro Suzuki Year-by-Year Test ===\n")
    
    # Search for Ichiro
    search_result = await search_player("Ichiro Suzuki", sport_id=31)
    print("Found Ichiro:", "br_suzuki001ich" in search_result)
    
    # Get year-by-year stats
    print("\nGetting Ichiro's NPB year-by-year stats...")
    yearly_stats = await get_player_stats(
        person_id="br_suzuki001ich",
        stats="yearByYear",
        sport_id=31
    )
    print(yearly_stats[:1000] + "..." if len(yearly_stats) > 1000 else yearly_stats)


async def main():
    """Run all tests."""
    await test_year_by_year_stats()
    await test_ichiro_year_by_year()
    print("\n=== Year-by-Year Tests Complete ===")


if __name__ == "__main__":
    asyncio.run(main())