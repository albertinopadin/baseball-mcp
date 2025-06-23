"""Test script to fetch and examine NPB player page structure."""

import asyncio
import httpx
from bs4 import BeautifulSoup


async def fetch_and_examine():
    """Fetch a player page and examine its structure."""
    
    # Ichiro's Baseball-Reference NPB page
    url = "https://www.baseball-reference.com/register/player.fcgi?id=cano--000ich"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    async with httpx.AsyncClient(follow_redirects=True, headers=headers) as client:
        response = await client.get(url)
        print(f"Status code: {response.status_code}")
        print(f"URL after redirects: {response.url}")
        print(f"Content length: {len(response.text)}")
        html = response.text
        
        # Save HTML for inspection
        with open("ichiro_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        soup = BeautifulSoup(html, "html.parser")
        
        # Look for player name
        print("Looking for player name...")
        h1_tags = soup.find_all("h1")
        for i, h1 in enumerate(h1_tags):
            print(f"  h1[{i}]: {h1.text.strip()}")
        
        # Look for tables
        print("\nLooking for tables...")
        tables = soup.find_all("table")
        for i, table in enumerate(tables):
            table_id = table.get("id", "no-id")
            table_class = table.get("class", ["no-class"])
            print(f"  table[{i}]: id='{table_id}', class={table_class}")
            
            # Check if it has headers
            headers = table.find("thead")
            if headers:
                header_cells = headers.find_all(["th", "td"])
                header_text = [cell.text.strip() for cell in header_cells[:5]]  # First 5 headers
                print(f"    Headers: {header_text}...")
        
        # Look for divs with player info
        print("\nLooking for player info divs...")
        info_div = soup.find("div", {"id": "info"})
        if info_div:
            print("  Found div#info")
        
        meta_div = soup.find("div", {"id": "meta"})
        if meta_div:
            print("  Found div#meta")
            
        print("\nPage saved to ichiro_page.html for inspection")


if __name__ == "__main__":
    asyncio.run(fetch_and_examine())