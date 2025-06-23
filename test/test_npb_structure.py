"""Test NPB site structure to find correct URLs."""

import asyncio
import httpx
from bs4 import BeautifulSoup


async def explore_npb_structure():
    """Explore NPB site to find correct URLs."""
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    print("Exploring NPB Site Structure")
    print("=" * 40)
    
    async with httpx.AsyncClient(headers=headers) as client:
        # Check main stats page for 2023
        url = "https://npb.jp/bis/eng/2023/stats/"
        print(f"\nChecking: {url}")
        
        response = await client.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Look for all links
            print("\nFound links:")
            links = soup.find_all("a", href=True)
            
            # Filter for stats-related links
            stats_links = []
            for link in links:
                href = link.get("href", "")
                text = link.text.strip()
                if "stats" in href or "standings" in href or ".html" in href:
                    stats_links.append((text, href))
                    print(f"  - {text}: {href}")
            
            # Look for tables
            print(f"\nTables found: {len(soup.find_all('table'))}")
            
            # Check frames or iframes
            frames = soup.find_all(["frame", "iframe"])
            if frames:
                print(f"\nFrames found: {len(frames)}")
                for frame in frames:
                    print(f"  - {frame.get('src', 'no-src')}")


if __name__ == "__main__":
    asyncio.run(explore_npb_structure())