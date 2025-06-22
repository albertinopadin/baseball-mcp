#!/usr/bin/env python3
"""Test script to get complete offensive stats for Dodgers players"""

import asyncio
import httpx
import json

BASE_URL = "https://statsapi.mlb.com/api/v1"

# Dodgers players and their IDs
DODGERS_PLAYERS = {
    "Mookie Betts": 605141,
    "Shohei Ohtani": 660271,
    "Freddie Freeman": 518692,
    "Will Smith": 669257,
    "Teoscar Hernandez": 606192,
    "Andy Pages": 681624,
    "Enrique Hernández": 571771,
    "Hyeseong Kim": 808975,
    "Max Muncy": 571970,
    "Michael Conforto": 624424,
    "Miguel Rojas": 500743,
    "Tommy Edman": 669242,
    "Dalton Rushing": 687221
}

async def get_player_stats(client, player_name, player_id):
    """Get hitting stats for a player"""
    url = f"{BASE_URL}/people/{player_id}/stats?stats=season&group=hitting&season=2025&sportId=1"
    
    try:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            return player_name, player_id, data
        else:
            return player_name, player_id, None
    except Exception as e:
        print(f"Error fetching stats for {player_name}: {e}")
        return player_name, player_id, None

def format_player_stats_full(player_name, data):
    """Format player stats with all offensive statistics"""
    if not data or "stats" not in data:
        return f"{player_name}: No stats available"
    
    stats_output = []
    stats_output.append(f"\n{'='*80}")
    stats_output.append(f"{player_name}")
    stats_output.append('='*80)
    
    for stat_group in data["stats"]:
        splits = stat_group.get("splits", [])
        if splits:
            split = splits[0]  # Get first split (current season)
            stat_data = split.get("stat", {})
            
            # Extract all offensive stats
            stats_output.append(f"Games: {stat_data.get('gamesPlayed', 0)}")
            stats_output.append(f"At Bats: {stat_data.get('atBats', 0)}")
            stats_output.append(f"Runs: {stat_data.get('runs', 0)}")
            stats_output.append(f"Hits: {stat_data.get('hits', 0)}")
            stats_output.append(f"Doubles: {stat_data.get('doubles', 0)}")
            stats_output.append(f"Triples: {stat_data.get('triples', 0)}")
            stats_output.append(f"Home Runs: {stat_data.get('homeRuns', 0)}")
            stats_output.append(f"RBI: {stat_data.get('rbi', 0)}")
            stats_output.append(f"Walks: {stat_data.get('baseOnBalls', 0)}")
            stats_output.append(f"Strikeouts: {stat_data.get('strikeOuts', 0)}")
            stats_output.append(f"Stolen Bases: {stat_data.get('stolenBases', 0)}")
            stats_output.append(f"Caught Stealing: {stat_data.get('caughtStealing', 0)}")
            stats_output.append(f"AVG: {stat_data.get('avg', 'N/A')}")
            stats_output.append(f"OBP: {stat_data.get('obp', 'N/A')}")
            stats_output.append(f"SLG: {stat_data.get('slg', 'N/A')}")
            stats_output.append(f"OPS: {stat_data.get('ops', 'N/A')}")
            
            # Additional stats if available
            stats_output.append(f"Total Bases: {stat_data.get('totalBases', 0)}")
            stats_output.append(f"HBP: {stat_data.get('hitByPitch', 0)}")
            stats_output.append(f"Sac Flies: {stat_data.get('sacFlies', 0)}")
            stats_output.append(f"Sac Bunts: {stat_data.get('sacBunts', 0)}")
            stats_output.append(f"GIDP: {stat_data.get('groundIntoDoublePlay', 0)}")
            stats_output.append(f"PA: {stat_data.get('plateAppearances', 0)}")
            
    return '\n'.join(stats_output)

async def main():
    """Main function to get all player stats"""
    async with httpx.AsyncClient() as client:
        # Get stats for all players
        tasks = []
        for player_name, player_id in DODGERS_PLAYERS.items():
            tasks.append(get_player_stats(client, player_name, player_id))
        
        results = await asyncio.gather(*tasks)
        
        # Create a summary table
        print("\n2025 LOS ANGELES DODGERS OFFENSIVE STATISTICS")
        print("=" * 150)
        print(f"{'Player':<20} {'G':<5} {'AB':<5} {'R':<5} {'H':<5} {'2B':<5} {'3B':<5} {'HR':<5} {'RBI':<5} {'BB':<5} {'SO':<5} {'SB':<5} {'AVG':<7} {'OBP':<7} {'SLG':<7} {'OPS':<7}")
        print("-" * 150)
        
        # Process and display results
        for player_name, player_id, data in results:
            if data and "stats" in data:
                for stat_group in data["stats"]:
                    splits = stat_group.get("splits", [])
                    if splits:
                        split = splits[0]
                        stat_data = split.get("stat", {})
                        
                        # Format stats for table
                        print(f"{player_name:<20} "
                              f"{stat_data.get('gamesPlayed', 0):<5} "
                              f"{stat_data.get('atBats', 0):<5} "
                              f"{stat_data.get('runs', 0):<5} "
                              f"{stat_data.get('hits', 0):<5} "
                              f"{stat_data.get('doubles', 0):<5} "
                              f"{stat_data.get('triples', 0):<5} "
                              f"{stat_data.get('homeRuns', 0):<5} "
                              f"{stat_data.get('rbi', 0):<5} "
                              f"{stat_data.get('baseOnBalls', 0):<5} "
                              f"{stat_data.get('strikeOuts', 0):<5} "
                              f"{stat_data.get('stolenBases', 0):<5} "
                              f"{stat_data.get('avg', 'N/A'):<7} "
                              f"{stat_data.get('obp', 'N/A'):<7} "
                              f"{stat_data.get('slg', 'N/A'):<7} "
                              f"{stat_data.get('ops', 'N/A'):<7}")
                        break
            else:
                print(f"{player_name:<20} No stats available for 2025")
        
        print("\n" + "=" * 150)
        
        # Also print detailed stats for each player
        print("\n\nDETAILED PLAYER STATISTICS:")
        for player_name, player_id, data in results:
            print(format_player_stats_full(player_name, data))

if __name__ == "__main__":
    asyncio.run(main())