"""Test which years are available on NPB site."""

import asyncio
import httpx


async def test_available_years():
    """Check which years have data on NPB site."""
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    print("Testing NPB Data Availability by Year")
    print("=" * 40)
    
    # Test different years
    years = [2024, 2023, 2022, 2021, 2020]
    
    async with httpx.AsyncClient(headers=headers) as client:
        for year in years:
            print(f"\nYear {year}:")
            
            # Test batting stats
            batting_url = f"https://npb.jp/bis/eng/{year}/stats/bat_avg_1.html"
            try:
                response = await client.get(batting_url)
                if response.status_code == 200:
                    print(f"  ✅ Batting stats available")
                else:
                    print(f"  ❌ Batting stats: {response.status_code}")
            except Exception as e:
                print(f"  ❌ Batting stats error: {e}")
            
            # Test standings
            standings_url = f"https://npb.jp/bis/eng/{year}/standings/standings_01.html"
            try:
                response = await client.get(standings_url)
                if response.status_code == 200:
                    print(f"  ✅ Standings available")
                else:
                    print(f"  ❌ Standings: {response.status_code}")
            except Exception as e:
                print(f"  ❌ Standings error: {e}")
            
            # Check the main stats page
            main_url = f"https://npb.jp/bis/eng/{year}/stats/"
            try:
                response = await client.get(main_url)
                if response.status_code == 200:
                    print(f"  ✅ Main stats page available")
                else:
                    print(f"  ❌ Main stats page: {response.status_code}")
            except Exception as e:
                print(f"  ❌ Main stats page error: {e}")


if __name__ == "__main__":
    asyncio.run(test_available_years())