#!/usr/bin/env python3
"""Unit tests for MLB Stats API module."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import mlb_stats_api


async def test_search_player():
    """Test player search functionality."""
    print("\n" + "="*60)
    print("Testing Player Search")
    print("="*60)
    
    # Test searching for active player
    print("\n1. Searching for Mike Trout:")
    result = await mlb_stats_api.search_player("Mike Trout")
    print(result[:300] + "..." if len(result) > 300 else result)
    assert "Mike Trout" in result
    assert "ID:" in result
    
    # Test searching for retired player
    print("\n2. Searching for Babe Ruth:")
    result = await mlb_stats_api.search_player("Babe Ruth")
    print(result[:300] + "..." if len(result) > 300 else result)
    assert "Babe Ruth" in result or "George Ruth" in result
    
    # Test searching for non-existent player
    print("\n3. Searching for non-existent player:")
    result = await mlb_stats_api.search_player("Fake Player XYZ")
    print(result)
    assert "No player found" in result


async def test_get_player():
    """Test getting specific player information."""
    print("\n" + "="*60)
    print("Testing Get Player")
    print("="*60)
    
    # Test getting Mike Trout's info (ID: 545361)
    print("\n1. Getting Mike Trout's information:")
    result = await mlb_stats_api.get_player(545361)
    print(result)
    assert "Mike Trout" in result
    assert "Outfielder" in result
    
    # Test with invalid ID
    print("\n2. Testing invalid player ID:")
    result = await mlb_stats_api.get_player(999999999)
    print(result)
    assert "Unable to find player" in result


async def test_get_player_stats():
    """Test getting player statistics."""
    print("\n" + "="*60)
    print("Testing Get Player Stats")
    print("="*60)
    
    # Test getting season stats
    print("\n1. Getting Mike Trout's 2024 season stats:")
    result = await mlb_stats_api.get_player_stats(545361, "season", "2024", group="hitting")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Test getting career stats
    print("\n2. Getting career stats:")
    result = await mlb_stats_api.get_player_stats(545361, "career", group="hitting")
    print(result[:500] + "..." if len(result) > 500 else result)


async def test_search_teams():
    """Test team search functionality."""
    print("\n" + "="*60)
    print("Testing Team Search")
    print("="*60)
    
    # Test searching all teams
    print("\n1. Getting all active teams:")
    result = await mlb_stats_api.search_teams()
    print(f"Found {result.count('Team Information:')} teams")
    assert "Los Angeles Dodgers" in result
    assert "New York Yankees" in result
    
    # Test searching by league
    print("\n2. Getting American League teams:")
    result = await mlb_stats_api.search_teams(league_id=103)  # AL
    print(f"Found {result.count('Team Information:')} AL teams")
    assert "New York Yankees" in result
    assert "Los Angeles Dodgers" not in result  # NL team


async def test_get_team():
    """Test getting specific team information."""
    print("\n" + "="*60)
    print("Testing Get Team")
    print("="*60)
    
    # Test getting Dodgers info (ID: 119)
    print("\n1. Getting LA Dodgers information:")
    result = await mlb_stats_api.get_team(119)
    print(result)
    assert "Los Angeles Dodgers" in result
    assert "Dodger Stadium" in result


async def test_get_schedule():
    """Test getting schedule information."""
    print("\n" + "="*60)
    print("Testing Get Schedule")
    print("="*60)
    
    # Test getting schedule for specific date range
    print("\n1. Getting schedule for June 1-3, 2024:")
    result = await mlb_stats_api.get_schedule(
        start_date="2024-06-01",
        end_date="2024-06-03"
    )
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Test getting team-specific schedule
    print("\n2. Getting Dodgers schedule for June 2024:")
    result = await mlb_stats_api.get_schedule(
        start_date="2024-06-01",
        end_date="2024-06-30",
        team_id=119
    )
    games_count = result.count("Game")
    print(f"Found {games_count} games for Dodgers in June 2024")


async def test_get_standings():
    """Test getting standings information."""
    print("\n" + "="*60)
    print("Testing Get Standings")
    print("="*60)
    
    # Test getting AL standings
    print("\n1. Getting AL standings for 2024:")
    result = await mlb_stats_api.get_standings(103, "2024")  # AL
    print(result)
    assert "Standings:" in result
    
    # Test getting NL standings
    print("\n2. Getting NL standings for 2024:")
    result = await mlb_stats_api.get_standings(104, "2024")  # NL
    print(result)
    assert "Standings:" in result


async def main():
    """Run all tests."""
    print("Starting MLB Stats API Tests")
    print("This may take a moment as we're making real API calls...")
    
    try:
        await test_search_player()
        await test_get_player()
        await test_get_player_stats()
        await test_search_teams()
        await test_get_team()
        await test_get_schedule()
        await test_get_standings()
        
        print("\n" + "="*60)
        print("All MLB Stats API tests passed!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())