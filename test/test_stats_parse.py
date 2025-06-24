#!/usr/bin/env python3
"""Test NPB stats parsing."""

import asyncio
import sys
sys.path.insert(0, '/Users/albertinopadin/Desktop/Dev/Python Projects/baseball-mcp/src')

from npb.sources.npb_official import NPBOfficialSource


async def test_stats():
    """Test stats parsing."""
    source = NPBOfficialSource()
    
    # Test getting stats for Murakami
    print("=== Testing Get Player Stats ===")
    stats = await source.get_player_stats("npb_murakami,_munetaka_2024", 2024, "batting")
    
    if stats:
        print(f"Found stats for: {stats.player_id}")
        print(f"Season: {stats.season}")
        print(f"Games: {stats.games}")
        print(f"AVG: {stats.batting_average}")
        print(f"HR: {stats.home_runs}")
        print(f"RBI: {stats.rbi}")
    else:
        print("No stats found")
        
        # Debug: Try parsing the page manually
        print("\nDebug: Checking stats page directly...")
        url = f"{source.base_url}/2024/stats/bat_c.html"
        page = await source._fetch_page(url)
        
        if page:
            tables = page.find_all('table')
            print(f"Found {len(tables)} tables")
            
            # Look for Murakami in the main table
            for table_idx, table in enumerate(tables):
                rows = table.find_all('tr')
                if len(rows) > 20:
                    print(f"\nTable {table_idx}: {len(rows)} rows")
                    
                    # Check headers
                    for row_idx in range(min(3, len(rows))):
                        cells = rows[row_idx].find_all(['td', 'th'])
                        if cells:
                            print(f"Row {row_idx}: {[c.text.strip()[:10] for c in cells[:5]]}")
                    
                    # Find player
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) > 2:
                            name = cells[1].text.strip()
                            if "Murakami" in name:
                                print(f"\nFound Murakami: {name}")
                                print(f"Cells in row: {len(cells)}")
                                # Print some stats
                                if len(cells) > 10:
                                    print(f"Cell 2: {cells[2].text.strip()}")  # Team
                                    print(f"Cell 3: {cells[3].text.strip()}")  # AVG
                                    print(f"Cell 4: {cells[4].text.strip()}")  # G
                                    print(f"Cell 5: {cells[5].text.strip()}")  # PA
                                break


if __name__ == "__main__":
    asyncio.run(test_stats())