"""Test accessing NPB official site."""

import asyncio
import httpx
from bs4 import BeautifulSoup


async def test_npb_official():
    """Test if we can access npb.jp without Cloudflare issues."""
    
    urls = [
        "https://npb.jp/eng/",
        "https://npb.jp/bis/eng/stats/",
        "https://npb.jp/bis/eng/2023/stats/"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }
    
    async with httpx.AsyncClient(follow_redirects=True, headers=headers) as client:
        for url in urls:
            print(f"\nTesting: {url}")
            print("-" * 50)
            
            try:
                response = await client.get(url, timeout=10.0)
                print(f"Status: {response.status_code}")
                print(f"Content length: {len(response.text)}")
                
                # Check for Cloudflare
                if "cloudflare" in response.text.lower() or response.status_code == 403:
                    print("⚠️  Cloudflare detected!")
                else:
                    print("✅ No Cloudflare detected")
                    
                    # Parse and look for data
                    soup = BeautifulSoup(response.text, "html.parser")
                    
                    # Look for tables
                    tables = soup.find_all("table")
                    print(f"Tables found: {len(tables)}")
                    
                    # Look for player links
                    player_links = soup.find_all("a", href=lambda x: x and "player" in x.lower())
                    print(f"Player links found: {len(player_links)}")
                    
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_npb_official())