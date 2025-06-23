"""Test if we can find Ohtani in 2017 NPB data."""

import asyncio
import httpx
from bs4 import BeautifulSoup


async def check_2017_npb_data():
    """Check what data is available for 2017 NPB season."""
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    print("Checking 2017 NPB Data (Ohtani's last NPB season)")
    print("=" * 60)
    
    async with httpx.AsyncClient(headers=headers) as client:
        # Check Pacific League batting (Ohtani played for Nippon-Ham Fighters in Pacific League)
        print("\n1. Pacific League Batting Leaders 2017")
        print("-" * 40)
        
        url = "https://npb.jp/bis/eng/2017/stats/bat_p.html"
        response = await client.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Look for Ohtani
            ohtani_found = False
            tables = soup.find_all("table")
            
            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    text = row.text
                    if "ohtani" in text.lower() or "otani" in text.lower():
                        print(f"Found Ohtani reference: {text.strip()}")
                        ohtani_found = True
                        
                        # Get all cells in this row
                        cells = row.find_all("td")
                        if cells:
                            print("Stats cells:")
                            for i, cell in enumerate(cells):
                                print(f"  [{i}]: {cell.text.strip()}")
            
            if not ohtani_found:
                print("Ohtani not found in batting leaders")
                # Let's check how many rows are in the table
                if tables:
                    main_table = tables[0]
                    rows = main_table.find_all("tr")
                    print(f"Total rows in table: {len(rows)}")
                    # Show first few player names
                    print("First few players:")
                    for i, row in enumerate(rows[1:6]):  # Skip header, show 5
                        cells = row.find_all("td")
                        if len(cells) > 1:
                            print(f"  {cells[0].text.strip()}: {cells[1].text.strip()}")
        
        # Check Pacific League pitching
        print("\n\n2. Pacific League Pitching Leaders 2017")
        print("-" * 40)
        
        url = "https://npb.jp/bis/eng/2017/stats/pit_p.html"
        response = await client.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Look for Ohtani
            ohtani_found = False
            tables = soup.find_all("table")
            
            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    text = row.text
                    if "ohtani" in text.lower() or "otani" in text.lower():
                        print(f"Found Ohtani reference: {text.strip()}")
                        ohtani_found = True
                        
                        # Get all cells in this row
                        cells = row.find_all("td")
                        if cells:
                            print("Stats cells:")
                            for i, cell in enumerate(cells):
                                print(f"  [{i}]: {cell.text.strip()}")
            
            if not ohtani_found:
                print("Ohtani not found in pitching leaders")
                # Show first few pitchers
                if tables:
                    main_table = tables[0]
                    rows = main_table.find_all("tr")
                    print(f"Total rows in table: {len(rows)}")
                    print("First few pitchers:")
                    for i, row in enumerate(rows[1:6]):  # Skip header, show 5
                        cells = row.find_all("td")
                        if len(cells) > 1:
                            print(f"  {cells[0].text.strip()}: {cells[1].text.strip()}")
        
        # Check if there's a different URL structure for full stats
        print("\n\n3. Checking for individual team pages...")
        print("-" * 40)
        
        # Nippon-Ham Fighters team page
        url = "https://npb.jp/bis/eng/2017/stats/idb1_f.html"
        response = await client.get(url)
        
        if response.status_code == 200:
            print("✅ Found Fighters batting stats page!")
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Look for Ohtani
            tables = soup.find_all("table")
            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    text = row.text
                    if "ohtani" in text.lower() or "otani" in text.lower():
                        print(f"Found Ohtani: {text.strip()}")
                        
                        cells = row.find_all("td")
                        if cells:
                            print("Full stats:")
                            for i, cell in enumerate(cells):
                                print(f"  [{i}]: {cell.text.strip()}")


if __name__ == "__main__":
    asyncio.run(check_2017_npb_data())