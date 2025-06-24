#!/usr/bin/env python3
"""Test NPB name parsing and matching."""

import asyncio
import sys
sys.path.insert(0, '/Users/albertinopadin/Desktop/Dev/Python Projects/baseball-mcp/src')

from npb.sources.npb_official import NPBOfficialSource
from npb.name_utils import match_name, normalize_name


async def test_name_parsing():
    """Test actual name parsing from NPB site."""
    source = NPBOfficialSource()
    
    # Fetch a page
    url = "https://npb.jp/bis/eng/2024/stats/bat_c.html"
    page = await source._fetch_page(url)
    
    if not page:
        print("Failed to fetch page")
        return
    
    # Find the stats table
    tables = page.find_all('table')
    
    for table in tables:
        rows = table.find_all('tr')
        if len(rows) < 5:
            continue
            
        # Check headers
        header_row = rows[0]
        headers = header_row.find_all(['td', 'th'])
        header_text = ' '.join([h.text.strip() for h in headers])
        
        if 'AVG' in header_text:
            print("Found stats table!")
            print(f"Headers: {[h.text.strip() for h in headers[:5]]}")
            
            # Show first few player names
            print("\nFirst 10 players:")
            for i, row in enumerate(rows[1:11]):
                cells = row.find_all(['td'])
                if len(cells) >= 2:
                    rank = cells[0].text.strip()
                    name = cells[1].text.strip()
                    print(f"  {rank}. {name}")
                    
                    # Test name matching
                    if "Murakami" in name:
                        print(f"     -> Found Murakami! Full name: '{name}'")
                        print(f"     -> Normalized: '{normalize_name(name)}'")
                        print(f"     -> Match test: {match_name('Murakami', name)}")
            
            break


if __name__ == "__main__":
    asyncio.run(test_name_parsing())