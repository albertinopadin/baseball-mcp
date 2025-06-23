"""Test script to discover minor league sport IDs in MLB Stats API"""
import asyncio
import httpx
import json

BASE_URL = "https://statsapi.mlb.com/api/v1"

async def test_sports_endpoint():
    """Try to find all available sports"""
    print("Testing various approaches to find sport IDs...\n")
    
    # Try without sportId parameter
    print("1. Testing /api/v1/sports without parameters:")
    url = f"{BASE_URL}/sports"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                print(f"Success! Found {len(data.get('sports', []))} sports")
                for sport in data.get('sports', []):
                    print(f"  - ID: {sport.get('id')}, Name: {sport.get('name')}, Code: {sport.get('code')}")
            else:
                print(f"  Status: {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n2. Testing specific sport IDs based on common patterns:")
    # Common sport IDs based on the reference link
    sport_ids = [
        (1, "Major League Baseball"),
        (11, "Triple-A"),
        (12, "Double-A"),
        (13, "High-A"),
        (14, "Single-A"),
        (15, "Short Season A"),
        (16, "Rookie Advanced"),
        (17, "Rookie"),
        (22, "Mexican League"),
        (23, "Mexican Academy")
    ]
    
    for sport_id, expected_name in sport_ids:
        url = f"{BASE_URL}/sports/{sport_id}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    sports = data.get('sports', [])
                    if sports:
                        sport = sports[0]
                        print(f"  Sport ID {sport_id}: {sport.get('name')} (Code: {sport.get('code')})")
                else:
                    print(f"  Sport ID {sport_id}: Not found (Status: {response.status_code})")
            except Exception as e:
                print(f"  Sport ID {sport_id}: Error - {e}")

async def test_minor_league_teams():
    """Test getting teams for different sport IDs"""
    print("\n\n3. Testing teams endpoint with different sport IDs:")
    
    # Test a few minor league sport IDs
    test_sport_ids = [11, 12, 13, 14]  # Triple-A, Double-A, High-A, Single-A
    
    for sport_id in test_sport_ids:
        url = f"{BASE_URL}/teams?sportId={sport_id}&activeStatus=Y"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    teams = data.get('teams', [])
                    print(f"\n  Sport ID {sport_id}: Found {len(teams)} teams")
                    if teams:
                        # Show first 3 teams as examples
                        for team in teams[:3]:
                            print(f"    - {team.get('name')} (ID: {team.get('id')})")
                else:
                    print(f"\n  Sport ID {sport_id}: Status {response.status_code}")
            except Exception as e:
                print(f"\n  Sport ID {sport_id}: Error - {e}")

async def test_minor_league_player_stats():
    """Test getting player stats with minor league sport IDs"""
    print("\n\n4. Testing player stats with minor league sport IDs:")
    
    # Use a known player ID (example: a player who has played in minors)
    # Let's search for a player first
    search_url = f"{BASE_URL}/people/search?names=Bobby Witt"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(search_url)
            if response.status_code == 200:
                data = response.json()
                people = data.get('people', [])
                if people:
                    player = people[0]
                    player_id = player.get('id')
                    print(f"\n  Found player: {player.get('fullName')} (ID: {player_id})")
                    
                    # Try getting stats for different sport IDs
                    for sport_id in [1, 11, 12, 13, 14]:
                        stats_url = f"{BASE_URL}/people/{player_id}/stats?stats=season&sportId={sport_id}&season=2023"
                        response = await client.get(stats_url)
                        if response.status_code == 200:
                            stats_data = response.json()
                            stats = stats_data.get('stats', [])
                            if stats and stats[0].get('splits'):
                                print(f"    Sport ID {sport_id}: Has stats")
                            else:
                                print(f"    Sport ID {sport_id}: No stats found")
        except Exception as e:
            print(f"  Error: {e}")

async def main():
    """Run all tests"""
    await test_sports_endpoint()
    await test_minor_league_teams()
    await test_minor_league_player_stats()

if __name__ == "__main__":
    asyncio.run(main())