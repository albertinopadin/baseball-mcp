#!/usr/bin/env python3
"""Test parsing directly."""

import asyncio
import httpx
from bs4 import BeautifulSoup
import sys
sys.path.insert(0, '/Users/albertinopadin/Desktop/Dev/Python Projects/baseball-mcp/src')
from npb.name_utils import match_name


async def test_direct():
    """Test parsing directly without the class."""
    url = "https://npb.jp/bis/eng/2024/stats/bat_c.html"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        page = BeautifulSoup(response.text, 'html.parser')
    
    tables = page.find_all('table')
    print(f"Found {len(tables)} tables")
    
    # Check first table with many rows
    for table_idx, table in enumerate(tables):
        rows = table.find_all('tr')
        if len(rows) > 20:
            print(f"\nTable {table_idx}: {len(rows)} rows")
            
            # Check header
            if rows[0]:
                header_cells = rows[0].find_all(['td', 'th'])
                print(f"First row: {[c.text.strip()[:20] for c in header_cells[:5]]}")
            
            if rows[1]:
                header_cells = rows[1].find_all(['td', 'th'])
                print(f"Second row: {[c.text.strip()[:20] for c in header_cells[:5]]}")
                header_text = ' '.join([h.text.strip() for h in header_cells])
                print(f"Has AVG/G/PA/AB: {any(stat in header_text for stat in ['AVG', 'G', 'PA', 'AB'])}")
            
            # Find Murakami
            found = False
            for row_idx, row in enumerate(rows):
                cells = row.find_all(['td'])
                if len(cells) >= 3:
                    player_name = cells[1].text.strip()
                    if "Murakami" in player_name:
                        print(f"\nMurakami found at row {row_idx}:")
                        print(f"  Cells: {len(cells)}")
                        print(f"  Name: '{player_name}'")
                        print(f"  Match test: {match_name('Murakami', player_name)}")
                        found = True
                        break
            
            if found:
                # Now test the parsing logic
                print("\nTesting parsing logic on stats rows:")
                data_start = 2 if any(stat in header_text for stat in ['AVG', 'G', 'PA', 'AB']) else 1
                
                for row_idx, row in enumerate(rows[data_start:data_start+5]):
                    cells = row.find_all(['td'])
                    if len(cells) >= 10:
                        name = cells[1].text.strip()
                        print(f"  Row {row_idx}: {name} - {len(cells)} cells")


if __name__ == "__main__":
    asyncio.run(test_direct())