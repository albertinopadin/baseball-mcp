#!/usr/bin/env python3
"""Debug NPB player search issue."""

import asyncio
import sys
sys.path.insert(0, '/Users/albertinopadin/Desktop/Dev/Python Projects/baseball-mcp/src')

from npb.sources.npb_official import NPBOfficialSource
from npb.name_utils import match_name


async def debug_search():
    """Debug the search process step by step."""
    source = NPBOfficialSource()
    
    # Test direct page fetch
    print("=== Testing Page Fetch ===")
    url = "https://npb.jp/bis/eng/2024/stats/bat_c.html"
    page = await source._fetch_page(url)
    print(f"Page fetched: {page is not None}")
    
    if page:
        # Check table structure
        tables = page.find_all('table')
        print(f"Tables found: {len(tables)}")
        
        # Find the stats table
        for i, table in enumerate(tables):
            rows = table.find_all('tr')
            if len(rows) > 20:  # Stats table should have many rows
                print(f"\nTable {i} - {len(rows)} rows")
                
                # Check a few rows for Murakami
                for j, row in enumerate(rows[:30]):  # Check first 30 rows
                    cells = row.find_all('td')
                    if len(cells) > 2:
                        rank = cells[0].text.strip()
                        name = cells[1].text.strip()
                        team = cells[2].text.strip() if len(cells) > 2 else ""
                        
                        if "Murakami" in name:
                            print(f"\nFOUND at row {j}:")
                            print(f"  Rank: {rank}")
                            print(f"  Name: '{name}'")
                            print(f"  Team: '{team}'")
                            
                            # Test name matching
                            print(f"\nName matching tests:")
                            test_searches = ["Murakami", "munetaka", "Munetaka Murakami"]
                            for search in test_searches:
                                result = match_name(search, name)
                                print(f"  match_name('{search}', '{name}') = {result}")
    
    # Now test the full search
    print("\n\n=== Testing Full Search ===")
    players = await source.search_player("Murakami")
    print(f"Players found: {len(players)}")
    for p in players:
        print(f"  - {p.name_english} ({p.id})")


if __name__ == "__main__":
    asyncio.run(debug_search())