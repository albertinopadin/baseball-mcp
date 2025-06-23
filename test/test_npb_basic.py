"""Basic test script for NPB functionality."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from npb import NPBAPI


async def test_npb_search():
    """Test NPB player search functionality."""
    api = NPBAPI()
    
    print("Testing NPB Player Search")
    print("=" * 50)
    
    # Test with some famous NPB players
    test_names = [
        "Shohei Ohtani",  # Famous player who played in NPB
        "Yu Darvish",     # Another famous NPB alumnus
        "Ichiro",         # Legend
        "Sadaharu Oh"     # Home run king
    ]
    
    for name in test_names:
        print(f"\nSearching for: {name}")
        print("-" * 30)
        result = await api.search_player(name)
        print(result)


async def test_npb_stats():
    """Test NPB player stats retrieval."""
    api = NPBAPI()
    
    print("\n\nTesting NPB Player Stats")
    print("=" * 50)
    
    # First search for a player to get their ID
    search_result = await api.provider.search_player("Ichiro")
    
    if search_result:
        player_id = search_result[0]["id"]
        print(f"\nGetting stats for player ID: {player_id}")
        print("-" * 30)
        
        # Get career stats
        career_stats = await api.get_player_stats(player_id)
        print("\nCareer Stats:")
        print(career_stats)
        
        # Get specific season
        season_stats = await api.get_player_stats(player_id, "2000")
        print("\n\n2000 Season Stats:")
        print(season_stats)


async def test_npb_teams():
    """Test NPB teams listing."""
    api = NPBAPI()
    
    print("\n\nTesting NPB Teams")
    print("=" * 50)
    
    teams = await api.get_teams()
    print(teams)


async def main():
    """Run all tests."""
    print("NPB Integration Test Suite")
    print("*" * 60)
    
    await test_npb_search()
    await test_npb_stats()
    await test_npb_teams()
    
    print("\n\nAll tests completed!")


if __name__ == "__main__":
    asyncio.run(main())