#!/usr/bin/env python
"""Test script for NPB historical data implementation."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from npb import NPBAPI


async def test_player_search(api: NPBAPI, name: str):
    """Test searching for a player."""
    print(f"\nSearching for '{name}'...")
    print("=" * 60)
    result = await api.search_player(name)
    print(result)
    return result


async def test_player_stats(api: NPBAPI, player_id: str, player_name: str):
    """Test getting player statistics."""
    print(f"\n\nGetting career statistics for {player_name} (ID: {player_id})...")
    print("=" * 60)
    stats = await api.get_player_stats(player_id)
    print(stats)
    
    # Also test specific season if available
    print(f"\n\nGetting 1994 season statistics for {player_name}...")
    print("=" * 60)
    season_stats = await api.get_player_stats(player_id, "1994")
    print(season_stats)


async def main():
    """Test NPB historical data with three legendary players."""
    print("NPB Historical Data Test")
    print("Testing with: Ichiro Suzuki, Sadaharu Oh, Tetsuharu Kawakami")
    
    # Initialize API with historical data enabled
    api = NPBAPI(use_historical=True)
    
    # Test players
    test_cases = [
        ("Ichiro", "suzuki-ichiro", "Ichiro Suzuki"),
        ("Sadaharu Oh", "oh-sadaharu", "Sadaharu Oh"),
        ("Kawakami", "kawakami-tetsuharu", "Tetsuharu Kawakami")
    ]
    
    for search_name, player_id, full_name in test_cases:
        # Test search
        await test_player_search(api, search_name)
        
        # Test stats retrieval
        await test_player_stats(api, player_id, full_name)
    
    # Test team functionality
    print("\n\nTesting team functionality...")
    print("=" * 60)
    
    # Get all teams
    teams_result = await api.get_teams()
    print("Available teams:")
    print(teams_result)
    
    # Test traditional metrics display
    print("\n\nTraditional Metrics Summary")
    print("=" * 60)
    
    # Get Ichiro's stats to show traditional metrics
    ichiro_stats_raw = await api.provider.get_player_stats("suzuki-ichiro")
    if "stats" in ichiro_stats_raw:
        print("\nIchiro's NPB Career (Traditional Stats):")
        career_stats = ichiro_stats_raw.get("career_totals", {})
        if career_stats:
            print(f"Games: {career_stats.get('games', 0)}")
            print(f"At Bats: {career_stats.get('at_bats', 0)}")
            print(f"Hits: {career_stats.get('hits', 0)}")
            print(f"Home Runs: {career_stats.get('home_runs', 0)}")
            print(f"RBIs: {career_stats.get('rbis', 0)}")
            print(f"Batting Average: {career_stats.get('batting_average', 0):.3f}")
            print(f"Stolen Bases: {career_stats.get('stolen_bases', 0)}")
    
    # Get Oh's stats
    oh_stats_raw = await api.provider.get_player_stats("oh-sadaharu")
    if "stats" in oh_stats_raw:
        print("\nSadaharu Oh's NPB Career (Traditional Stats):")
        career_stats = oh_stats_raw.get("career_totals", {})
        if career_stats:
            print(f"Games: {career_stats.get('games', 0)}")
            print(f"At Bats: {career_stats.get('at_bats', 0)}")
            print(f"Hits: {career_stats.get('hits', 0)}")
            print(f"Home Runs: {career_stats.get('home_runs', 0)}")
            print(f"RBIs: {career_stats.get('rbis', 0)}")
            print(f"Batting Average: {career_stats.get('batting_average', 0):.3f}")
            print(f"Walks: {career_stats.get('walks', 0)}")
    
    print("\n\nTest completed successfully!")
    print("Historical NPB data is now available for players before 2005.")


if __name__ == "__main__":
    asyncio.run(main())