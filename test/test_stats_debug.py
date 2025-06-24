#!/usr/bin/env python3
"""Debug NPB stats column mapping."""

import asyncio
import httpx
from bs4 import BeautifulSoup
import sys
sys.path.insert(0, '/Users/albertinopadin/Desktop/Dev/Python Projects/baseball-mcp/src')


async def debug_stats():
    """Debug stats parsing."""
    url = "https://npb.jp/bis/eng/2024/stats/bat_c.html"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        page = BeautifulSoup(response.text, 'html.parser')
    
    tables = page.find_all('table')
    
    # Find the stats table
    for table_idx, table in enumerate(tables):
        rows = table.find_all('tr')
        if len(rows) > 20:
            print(f"Table {table_idx}: {len(rows)} rows")
            
            # Find header row
            header_row = None
            header_idx = -1
            for idx, row in enumerate(rows[:5]):
                cells = row.find_all(['td', 'th'])
                if any('AVG' in cell.text for cell in cells):
                    header_row = cells
                    header_idx = idx
                    break
            
            if header_row:
                print(f"\nHeader found at row {header_idx}:")
                for i, cell in enumerate(header_row):
                    print(f"  Col {i}: '{cell.text.strip()}'")
                
                # Find Murakami
                for row in rows[header_idx+1:]:
                    cells = row.find_all('td')
                    if len(cells) > 2:
                        name = cells[1].text.strip()
                        if "Murakami" in name:
                            print(f"\nMurakami row found:")
                            print(f"Name: {name}")
                            for i in range(min(15, len(cells))):
                                print(f"  Col {i}: '{cells[i].text.strip()}'")
                            break


if __name__ == "__main__":
    asyncio.run(debug_stats())