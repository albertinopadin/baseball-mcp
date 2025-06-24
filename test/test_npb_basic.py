#!/usr/bin/env python3
"""Basic test script for NPB functionality."""

import asyncio
import sys
sys.path.insert(0, '/Users/albertinopadin/Desktop/Dev/Python Projects/baseball-mcp/src')

from npb.sources.npb_official import NPBOfficialSource
from npb.models import NPBPlayer, NPBTeam, NPBLeague


async def test_npb_source():
    """Test basic NPB source functionality."""
    print("Testing NPB Official Source...")
    
    # Initialize source
    source = NPBOfficialSource()
    print(f"✓ Source initialized: {source.name}")
    print(f"  Base URL: {source.base_url}")
    print(f"  Cache TTL: {source.cache_ttl} seconds")
    
    # Test health check
    print("\nTesting health check...")
    is_healthy = await source.health_check()
    print(f"✓ Health check: {'Passed' if is_healthy else 'Failed'}")
    
    # Test team retrieval
    print("\nTesting team retrieval...")
    teams = await source.get_teams()
    print(f"✓ Retrieved {len(teams)} teams")
    
    # Display teams by league
    central_teams = [t for t in teams if t.league == NPBLeague.CENTRAL]
    pacific_teams = [t for t in teams if t.league == NPBLeague.PACIFIC]
    
    print("\nCentral League Teams:")
    for team in central_teams:
        print(f"  - {team.name_english} ({team.abbreviation})")
    
    print("\nPacific League Teams:")
    for team in pacific_teams:
        print(f"  - {team.name_english} ({team.abbreviation})")
    
    # Test player search (placeholder for now)
    print("\nTesting player search...")
    test_names = ["Murakami", "Yamamoto", "Ohtani"]
    for name in test_names:
        print(f"\n  Searching for '{name}'...")
        players = await source.search_player(name)
        print(f"  Found {len(players)} player(s)")
        for player in players:
            print(f"    - {player.name_english} ({player.team.name_english if player.team else 'No team'})")
    
    print("\n✓ Basic NPB source tests completed!")


async def test_cache_key_generation():
    """Test cache key generation."""
    print("\n\nTesting cache key generation...")
    source = NPBOfficialSource()
    
    # Test different cache keys
    key1 = source.get_cache_key("search_player", "Murakami")
    key2 = source.get_cache_key("get_player_stats", "player123", season=2024)
    key3 = source.get_cache_key("get_teams", season=2024)
    
    print(f"✓ Cache key 1: {key1}")
    print(f"✓ Cache key 2: {key2}")
    print(f"✓ Cache key 3: {key3}")


async def test_data_models():
    """Test NPB data models."""
    print("\n\nTesting NPB data models...")
    
    # Test team model
    team = NPBTeam(
        id="npb_G",
        name_english="Yomiuri Giants",
        name_japanese="読売ジャイアンツ",
        abbreviation="G",
        league=NPBLeague.CENTRAL,
        city="Tokyo",
        source="npb_official",
        source_id="G"
    )
    print(f"✓ Created team: {team.name_english}")
    print(f"  Team dict: {team.to_dict()}")
    
    # Test player model
    player = NPBPlayer(
        id="npb_murakami_munetaka",
        name_english="Munetaka Murakami",
        name_japanese="村上宗隆",
        team=team,
        jersey_number="55",
        position="3B",
        source="npb_official",
        source_id="murakami_m"
    )
    print(f"\n✓ Created player: {player.name_english}")
    print(f"  Player dict: {player.to_dict()}")


if __name__ == "__main__":
    print("NPB Integration Basic Test Suite")
    print("=" * 50)
    
    asyncio.run(test_npb_source())
    asyncio.run(test_cache_key_generation())
    asyncio.run(test_data_models())
    
    print("\n" + "=" * 50)
    print("All tests completed!")