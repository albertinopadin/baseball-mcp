"""Test various endpoints with minor league sport IDs"""
import asyncio
import httpx
from datetime import datetime, timedelta

BASE_URL = "https://statsapi.mlb.com/api/v1"

async def test_minor_league_schedule():
    """Test schedule endpoint with minor league sport IDs"""
    print("Testing Schedule Endpoint for Minor Leagues")
    print("="*60)
    
    # Test date range
    today = datetime.now()
    start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    
    sport_names = {
        11: "Triple-A",
        12: "Double-A",
        13: "High-A",
        14: "Single-A"
    }
    
    async with httpx.AsyncClient() as client:
        for sport_id, sport_name in sport_names.items():
            url = f"{BASE_URL}/schedule?sportId={sport_id}&startDate={start_date}&endDate={end_date}"
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                dates = data.get('dates', [])
                total_games = sum(len(date.get('games', [])) for date in dates)
                print(f"\n{sport_name} (sportId={sport_id}):")
                print(f"  Found {total_games} games from {start_date} to {end_date}")
                
                # Show a sample game if available
                if dates and dates[0].get('games'):
                    game = dates[0]['games'][0]
                    teams = game.get('teams', {})
                    away = teams.get('away', {}).get('team', {}).get('name', 'Unknown')
                    home = teams.get('home', {}).get('team', {}).get('name', 'Unknown')
                    print(f"  Sample: {away} @ {home}")

async def test_minor_league_standings():
    """Test if standings work for minor leagues"""
    print("\n\nTesting Standings for Minor Leagues")
    print("="*60)
    
    # Minor leagues don't use the same league IDs as MLB
    # Let's try to get standings for specific sport IDs
    async with httpx.AsyncClient() as client:
        # First, let's see if we can get league info for minor leagues
        for sport_id in [11, 12, 13, 14]:
            # Try different approaches
            print(f"\nTesting sportId={sport_id}:")
            
            # Try regular season standings with sportId parameter
            url = f"{BASE_URL}/standings/regularSeason?sportId={sport_id}"
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                records = data.get('records', [])
                print(f"  Found {len(records)} division standings")
                if records:
                    division = records[0].get('division', {}).get('name', 'Unknown')
                    print(f"  Sample division: {division}")
            else:
                print(f"  Standings not available (Status: {response.status_code})")

async def test_specific_minor_league_game():
    """Test getting game info for a minor league game"""
    print("\n\nTesting Game Info for Minor League Games")
    print("="*60)
    
    # First get a recent minor league game
    today = datetime.now()
    yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    
    async with httpx.AsyncClient() as client:
        # Get Triple-A games from yesterday
        url = f"{BASE_URL}/schedule?sportId=11&date={yesterday}"
        response = await client.get(url)
        
        if response.status_code == 200:
            data = response.json()
            dates = data.get('dates', [])
            
            if dates and dates[0].get('games'):
                game = dates[0]['games'][0]
                game_pk = game.get('gamePk')
                teams = game.get('teams', {})
                away = teams.get('away', {}).get('team', {}).get('name', 'Unknown')
                home = teams.get('home', {}).get('team', {}).get('name', 'Unknown')
                
                print(f"\nFound Triple-A game: {away} @ {home}")
                print(f"Game ID: {game_pk}")
                
                # Try to get boxscore
                boxscore_url = f"{BASE_URL}/game/{game_pk}/boxscore"
                boxscore_response = await client.get(boxscore_url)
                
                if boxscore_response.status_code == 200:
                    print("  ✓ Boxscore data available!")
                else:
                    print(f"  ✗ Boxscore not available (Status: {boxscore_response.status_code})")
                
                # Try to get live feed
                feed_url = f"{BASE_URL}/game/{game_pk}/feed/live"
                feed_response = await client.get(feed_url)
                
                if feed_response.status_code == 200:
                    print("  ✓ Live feed data available!")
                else:
                    print(f"  ✗ Live feed not available (Status: {feed_response.status_code})")

async def test_player_search_with_sport_filter():
    """Test if player search can be filtered by sport"""
    print("\n\nTesting Player Search with Sport Filters")
    print("="*60)
    
    async with httpx.AsyncClient() as client:
        # Test if we can search with sport filter
        test_names = ["Smith", "Johnson"]
        
        for name in test_names:
            print(f"\nSearching for '{name}':")
            
            # Try with sportId parameter
            url = f"{BASE_URL}/people/search?names={name}&sportId=11"
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                people = data.get('people', [])
                print(f"  With sportId=11 filter: Found {len(people)} players")
            
            # Compare with no filter
            url = f"{BASE_URL}/people/search?names={name}"
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                people = data.get('people', [])
                print(f"  Without filter: Found {len(people)} players")

async def main():
    await test_minor_league_schedule()
    await test_minor_league_standings()
    await test_specific_minor_league_game()
    await test_player_search_with_sport_filter()

if __name__ == "__main__":
    asyncio.run(main())