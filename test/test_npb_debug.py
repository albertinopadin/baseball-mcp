#!/usr/bin/env python3
"""Debug NPB HTML parsing."""

import asyncio
import sys
sys.path.insert(0, '/Users/albertinopadin/Desktop/Dev/Python Projects/baseball-mcp/src')

from npb.sources.npb_official import NPBOfficialSource


async def debug_html_parsing():
    """Debug HTML parsing to understand page structure."""
    source = NPBOfficialSource()
    
    # Fetch a page to examine structure
    url = "https://npb.jp/bis/eng/2024/stats/bat_c.html"
    print(f"Fetching: {url}")
    
    page = await source._fetch_page(url)
    if not page:
        print("Failed to fetch page")
        return
    
    print("\n=== Page Structure Debug ===")
    
    # Find all tables
    tables = page.find_all('table')
    print(f"\nFound {len(tables)} tables")
    
    for i, table in enumerate(tables[:3]):  # Check first 3 tables
        print(f"\n--- Table {i+1} ---")
        
        # Check table attributes
        attrs = table.attrs
        print(f"Attributes: {attrs}")
        
        # Check first few rows
        rows = table.find_all('tr')
        print(f"Rows: {len(rows)}")
        
        if rows:
            # Check header row
            print("\nHeader row:")
            headers = rows[0].find_all(['th', 'td'])
            print(f"Headers ({len(headers)}): {[h.text.strip() for h in headers[:10]]}")
            
            # Check first data row
            if len(rows) > 1:
                print("\nFirst data row:")
                cells = rows[1].find_all(['td', 'th'])
                print(f"Cells ({len(cells)}): {[c.text.strip() for c in cells[:10]]}")
    
    # Look for player links
    print("\n\n=== Player Links ===")
    links = page.find_all('a', href=True)
    player_links = [l for l in links if 'player' in l.get('href', '').lower()]
    
    print(f"Found {len(player_links)} player links")
    for link in player_links[:5]:
        print(f"  {link.text.strip()} -> {link['href']}")


if __name__ == "__main__":
    asyncio.run(debug_html_parsing())