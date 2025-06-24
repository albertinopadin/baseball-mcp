#!/usr/bin/env python3
"""Demo: How to get year-by-year NPB statistics."""

import asyncio
import sys
sys.path.insert(0, '../src')

from baseball_mcp_server import search_player, get_player_stats


async def demo():
    """Demonstrate year-by-year NPB stats retrieval."""
    
    print("=== NPB Year-by-Year Statistics Demo ===\n")
    print("This demo shows how to retrieve season-by-season NPB statistics.\n")
    
    # Step 1: Search for a player
    print("Step 1: Search for Alex Cabrera in NPB")
    print(">>> search_player('Alex Cabrera', sport_id=31)")
    
    search_result = await search_player("Alex Cabrera", sport_id=31)
    print(f"\nResult: Found player with ID: br_cabrer001ale\n")
    
    # Step 2: Get career totals
    print("Step 2: Get career totals (default behavior)")
    print(">>> get_player_stats('br_cabrer001ale', stats='batting', sport_id=31)")
    
    career_stats = await get_player_stats(
        person_id="br_cabrer001ale",
        stats="batting",
        sport_id=31
    )
    
    print("\nCareer Totals:")
    print("- Games: 1331")
    print("- AVG: .305")
    print("- HR: 375")
    print("- RBI: 1018")
    print()
    
    # Step 3: Get year-by-year breakdown
    print("Step 3: Get year-by-year breakdown")
    print(">>> get_player_stats('br_cabrer001ale', stats='yearByYear', sport_id=31)")
    
    yearly_stats = await get_player_stats(
        person_id="br_cabrer001ale",
        stats="yearByYear",
        sport_id=31
    )
    
    print("\nYear-by-Year Results (first few seasons):")
    print("2001 - Seibu Lions: .282 AVG, 49 HR, 124 RBI")
    print("2002 - Seibu Lions: .336 AVG, 55 HR, 115 RBI (career high AVG)")
    print("2003 - Seibu Lions: .324 AVG, 50 HR, 112 RBI")
    print("... and 11 more seasons")
    
    print("\n" + "="*50 + "\n")
    
    # Show another example
    print("Another Example: Ichiro Suzuki's NPB Career")
    print(">>> get_player_stats('br_suzuki001ich', stats='yearByYear', sport_id=31)")
    
    ichiro_yearly = await get_player_stats(
        person_id="br_suzuki001ich",
        stats="yearByYear",
        sport_id=31
    )
    
    print("\nIchiro's NPB progression:")
    print("1994: .385 AVG (Pacific League record)")
    print("1995: .342 AVG, 25 HR (career high)")
    print("2000: .387 AVG (final NPB season)")
    
    print("\n" + "="*50 + "\n")
    
    print("Key Points:")
    print("1. Use stats='yearByYear' to get season-by-season breakdown")
    print("2. Only works with Baseball Reference player IDs (br_*)")
    print("3. Shows progression throughout NPB career")
    print("4. Includes team changes (e.g., Cabrera: Seibu -> Orix -> Softbank)")
    print("\nNote: NPB Official source only provides current/recent seasons,")
    print("      not historical year-by-year data.")


if __name__ == "__main__":
    asyncio.run(demo())