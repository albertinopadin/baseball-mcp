"""Example test script demonstrating minor league data access"""
import asyncio
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import mlb_stats_api
import sports_api

async def demo_minor_league_access():
    """Demonstrate accessing minor league data through the MCP server functions"""
    
    print("Baseball MCP Server - Minor League Data Demo")
    print("=" * 60)
    
    # 1. Show available sports/leagues
    print("\n1. Available Sports/Leagues:")
    print("-" * 40)
    sports_list = await sports_api.get_available_sports()
    print(sports_list)
    
    # 2. Get Triple-A teams
    print("\n\n2. Triple-A Teams (sportId=11):")
    print("-" * 40)
    aaa_teams = await mlb_stats_api.search_teams(sport_id=11)
    # Just show first few lines to keep output manageable
    print(aaa_teams.split('\n')[:10])
    print("... (more teams)")
    
    # 3. Search for a player and get their minor league stats
    print("\n\n3. Player Minor League Stats Example:")
    print("-" * 40)
    
    # Search for Jackson Holliday
    player_search = await mlb_stats_api.search_player("Jackson Holliday")
    print(f"Player Search Result:\n{player_search.split('---')[0]}")
    
    # Get his Triple-A stats for 2024
    # Jackson Holliday's ID is 702616
    player_id = 702616
    print(f"\nGetting Triple-A stats for player ID {player_id}...")
    
    aaa_stats = await mlb_stats_api.get_player_stats(
        person_id=player_id,
        stats="season",
        sport_id=11,  # Triple-A
        season="2024"
    )
    print(f"\nTriple-A Stats:\n{aaa_stats}")
    
    # 4. Get Double-A schedule for a week
    print("\n\n4. Double-A Schedule Example (sportId=12):")
    print("-" * 40)
    
    aa_schedule = await mlb_stats_api.get_schedule(
        sport_id=12,  # Double-A
        start_date="2024-06-01",
        end_date="2024-06-03"
    )
    # Show first part of schedule
    print(aa_schedule.split('\n')[:20])
    print("... (more games)")
    
    # 5. Compare MLB vs Minor League stats for a player
    print("\n\n5. MLB vs Minor League Stats Comparison:")
    print("-" * 40)
    
    # Get MLB stats
    mlb_stats = await mlb_stats_api.get_player_stats(
        person_id=player_id,
        stats="season",
        sport_id=1,  # MLB
        season="2024"
    )
    print(f"MLB Stats (2024):\n{mlb_stats}")
    
    # Get Double-A stats from 2023
    aa_stats = await mlb_stats_api.get_player_stats(
        person_id=player_id,
        stats="season",
        sport_id=12,  # Double-A
        season="2023"
    )
    print(f"\nDouble-A Stats (2023):\n{aa_stats}")

async def main():
    """Run the demo"""
    try:
        await demo_minor_league_access()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Running Minor League Data Access Demo...")
    print("This demonstrates how the MCP server can access minor league data")
    print()
    asyncio.run(main())