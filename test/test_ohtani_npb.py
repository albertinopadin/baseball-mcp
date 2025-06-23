"""Test NPB functionality with Shohei Ohtani's stats."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from baseball_mcp_server import search_npb_player, get_npb_player_stats


async def test_ohtani_npb_stats():
    """Test getting Shohei Ohtani's NPB statistics."""
    print("Testing NPB Tools with Shohei Ohtani")
    print("=" * 60)
    
    # Step 1: Search for Shohei Ohtani
    print("\n1. Searching for Shohei Ohtani in NPB...")
    print("-" * 40)
    search_result = await search_npb_player("Shohei Ohtani")
    print(search_result)
    
    # Step 2: Get his NPB stats
    # Note: We need to extract the player ID from search results
    # Let's try with his likely ID format
    print("\n2. Getting Shohei Ohtani's NPB Statistics...")
    print("-" * 40)
    
    # Try different possible IDs
    possible_ids = ["ohtani000sho", "otani-000sho", "ohtani_shohei"]
    
    for player_id in possible_ids:
        print(f"\nTrying player ID: {player_id}")
        try:
            # Get career stats
            career_stats = await get_npb_player_stats(player_id)
            print("Career Stats:")
            print(career_stats)
            
            # Get specific season (2017 was his last NPB season)
            print("\n2017 Season Stats:")
            stats_2017 = await get_npb_player_stats(player_id, "2017")
            print(stats_2017)
            
            # If we got data, break
            if "No statistics available" not in career_stats:
                break
                
        except Exception as e:
            print(f"Error with ID {player_id}: {e}")
    
    # Step 3: Also test with current NPB players
    print("\n\n3. Testing with current NPB player (Munetaka Murakami)...")
    print("-" * 40)
    search_result = await search_npb_player("Munetaka Murakami")
    print(search_result)
    
    # Try to get Murakami's 2023 stats
    print("\nGetting Murakami's 2023 stats...")
    murakami_stats = await get_npb_player_stats("murakami_munetaka", "2023")
    print(murakami_stats)


if __name__ == "__main__":
    asyncio.run(test_ohtani_npb_stats())