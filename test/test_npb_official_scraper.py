"""Test NPB official site scraper."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from npb import NPBAPI


async def test_npb_api():
    """Test NPB API with official site scraper."""
    api = NPBAPI()
    
    print("Testing NPB API with Official Site Scraper")
    print("=" * 60)
    
    # Test 1: Search for active players
    print("\n1. Testing Player Search")
    print("-" * 40)
    
    test_players = ["Munetaka Murakami", "Roki Sasaki", "Yoshinobu Yamamoto"]
    
    for player in test_players:
        print(f"\nSearching for: {player}")
        result = await api.search_player(player)
        print(result)
    
    # Test 2: Get player stats
    print("\n\n2. Testing Player Stats")
    print("-" * 40)
    
    # Search for Murakami to get his ID
    search_result = await api.provider.search_player("Murakami")
    if search_result:
        player_id = search_result[0]["id"]
        print(f"\nGetting stats for: {search_result[0]['name_english']} (ID: {player_id})")
        stats = await api.get_player_stats(player_id, "2023")
        print(stats)
    
    # Test 3: Get teams
    print("\n\n3. Testing Teams List")
    print("-" * 40)
    teams = await api.get_teams()
    print(teams)
    
    # Test 4: Get standings (if implemented)
    print("\n\n4. Testing Standings")
    print("-" * 40)
    standings = await api.provider.get_standings()
    if "error" not in standings:
        print("Central League:")
        for team in standings.get("central", []):
            print(f"  {team.get('rank')}. {team.get('team')} - W:{team.get('wins')} L:{team.get('losses')} T:{team.get('ties')}")
        
        print("\nPacific League:")
        for team in standings.get("pacific", []):
            print(f"  {team.get('rank')}. {team.get('team')} - W:{team.get('wins')} L:{team.get('losses')} T:{team.get('ties')}")
    else:
        print("Standings not available")


if __name__ == "__main__":
    asyncio.run(test_npb_api())