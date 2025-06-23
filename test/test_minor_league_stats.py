"""Test minor league player statistics retrieval"""
import asyncio
import httpx
import json

BASE_URL = "https://statsapi.mlb.com/api/v1"

async def test_player_minor_league_stats():
    """Test retrieving minor league stats for various players"""
    
    # Players to test - mix of current prospects and recent call-ups
    test_players = [
        "Jackson Holliday",  # Orioles prospect
        "Paul Skenes",       # Pirates prospect
        "Jasson Dominguez",  # Yankees prospect
        "Jordan Walker",     # Cardinals
        "Gunnar Henderson"   # Orioles - had minor league time
    ]
    
    async with httpx.AsyncClient() as client:
        for player_name in test_players:
            print(f"\n{'='*60}")
            print(f"Testing: {player_name}")
            print('='*60)
            
            # Search for player
            search_url = f"{BASE_URL}/people/search?names={player_name}"
            response = await client.get(search_url)
            
            if response.status_code != 200:
                print(f"  Error searching for {player_name}")
                continue
                
            data = response.json()
            people = data.get('people', [])
            
            if not people:
                print(f"  Player not found: {player_name}")
                continue
            
            player = people[0]
            player_id = player.get('id')
            print(f"  Found: {player.get('fullName')} (ID: {player_id})")
            
            # Test different sport IDs and years
            sport_names = {
                1: "MLB",
                11: "Triple-A",
                12: "Double-A", 
                13: "High-A",
                14: "Single-A",
                16: "Rookie"
            }
            
            for sport_id, sport_name in sport_names.items():
                # Try multiple years
                for year in [2024, 2023, 2022]:
                    stats_url = f"{BASE_URL}/people/{player_id}/stats?stats=season&sportId={sport_id}&season={year}"
                    stats_response = await client.get(stats_url)
                    
                    if stats_response.status_code == 200:
                        stats_data = stats_response.json()
                        stats = stats_data.get('stats', [])
                        
                        if stats and stats[0].get('splits'):
                            splits = stats[0]['splits']
                            print(f"\n  {sport_name} ({sport_id}) - {year}: Found {len(splits)} record(s)")
                            
                            # Show first split details
                            if splits:
                                split = splits[0]
                                team = split.get('team', {})
                                print(f"    Team: {team.get('name')}")
                                
                                # Show some stats
                                stat = split.get('stat', {})
                                if 'battingAverage' in stat:  # Hitting stats
                                    print(f"    Games: {stat.get('gamesPlayed', 'N/A')}")
                                    print(f"    AVG: {stat.get('battingAverage', 'N/A')}")
                                    print(f"    HR: {stat.get('homeRuns', 'N/A')}")
                                    print(f"    RBI: {stat.get('runs', 'N/A')}")
                                elif 'era' in stat:  # Pitching stats
                                    print(f"    Games: {stat.get('gamesPlayed', 'N/A')}")
                                    print(f"    ERA: {stat.get('era', 'N/A')}")
                                    print(f"    W-L: {stat.get('wins', 0)}-{stat.get('losses', 0)}")
                                    print(f"    SO: {stat.get('strikeOuts', 'N/A')}")

async def test_year_by_year_stats():
    """Test yearByYear stats to see all levels a player has played"""
    print("\n\n" + "="*60)
    print("Testing yearByYear stats across all levels")
    print("="*60)
    
    test_player = "Gunnar Henderson"
    
    async with httpx.AsyncClient() as client:
        # Search for player
        search_url = f"{BASE_URL}/people/search?names={test_player}"
        response = await client.get(search_url)
        
        if response.status_code == 200:
            data = response.json()
            people = data.get('people', [])
            
            if people:
                player = people[0]
                player_id = player.get('id')
                print(f"\nPlayer: {player.get('fullName')} (ID: {player_id})")
                
                # Get yearByYear stats - this should show all levels
                stats_url = f"{BASE_URL}/people/{player_id}/stats?stats=yearByYear&group=hitting"
                stats_response = await client.get(stats_url)
                
                if stats_response.status_code == 200:
                    stats_data = stats_response.json()
                    stats = stats_data.get('stats', [])
                    
                    if stats and stats[0].get('splits'):
                        splits = stats[0]['splits']
                        print(f"\nFound {len(splits)} season(s) of data:")
                        
                        for split in splits:
                            season = split.get('season')
                            team = split.get('team', {})
                            league = split.get('league', {})
                            sport = split.get('sport', {})
                            stat = split.get('stat', {})
                            
                            print(f"\n  {season}:")
                            print(f"    Team: {team.get('name')}")
                            print(f"    League: {league.get('name')}")
                            print(f"    Level: {sport.get('name')} (ID: {sport.get('id')})")
                            print(f"    Games: {stat.get('gamesPlayed', 'N/A')}")
                            if 'battingAverage' in stat:
                                print(f"    AVG: {stat.get('battingAverage', 'N/A')}, HR: {stat.get('homeRuns', 'N/A')}")

async def main():
    await test_player_minor_league_stats()
    await test_year_by_year_stats()

if __name__ == "__main__":
    asyncio.run(main())