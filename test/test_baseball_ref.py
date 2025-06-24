#!/usr/bin/env python3
"""Test Baseball Reference NPB integration with priority players."""

import asyncio
import sys
sys.path.insert(0, '/Users/albertinopadin/Desktop/Dev/Python Projects/baseball-mcp/src')

from baseball_mcp_server import search_player, get_player_stats


async def test_baseball_reference():
    """Test Baseball Reference integration with priority players."""
    
    # Test players as requested
    test_players = [
        ("Ichiro Suzuki", "Check MLB and NPB stats"),
        ("Sadaharu Oh", "NPB legend"),
        ("Munetaka Murakami", "Current NPB star"),
        ("Alex Cabrera", "MLB and NPB player"),
        ("Karl Rhodes", "MLB and NPB player")
    ]
    
    print("=== Testing Baseball Reference NPB Integration ===\n")
    
    for player_name, description in test_players:
        print(f"\n{'='*60}")
        print(f"Testing: {player_name} ({description})")
        print('='*60)
        
        # Search for player
        print(f"\nSearching for '{player_name}'...")
        result = await search_player(player_name, sport_id=31)
        print(result)
        
        # For players we expect to find, try to get their stats
        if "br_" in result:
            # Extract player ID from the result
            lines = result.split('\n')
            player_id = None
            for line in lines:
                if 'ID:' in line:
                    player_id = line.split('ID:')[1].strip()
                    break
            
            if player_id:
                print(f"\nGetting career batting stats for {player_id}...")
                stats = await get_player_stats(player_id, 'batting', sport_id=31)
                print(stats)
                
                # For specific seasons (like Ichiro's 2000 NPB season)
                if "Ichiro" in player_name:
                    print(f"\nGetting 2000 season stats for Ichiro...")
                    stats_2000 = await get_player_stats(player_id, 'batting', season='2000', sport_id=31)
                    print(stats_2000)
    
    print("\n\n=== Test Complete ===")


async def test_disambiguation():
    """Test disambiguation with common names."""
    print("\n=== Testing Disambiguation ===")
    
    # Test with a common name that might have multiple results
    print("\nSearching for 'Yamamoto'...")
    result = await search_player("Yamamoto", sport_id=31)
    print(result)
    
    print("\nSearching for 'Suzuki'...")
    result = await search_player("Suzuki", sport_id=31)
    print(result)


if __name__ == "__main__":
    asyncio.run(test_baseball_reference())
    # asyncio.run(test_disambiguation())