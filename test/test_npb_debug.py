"""Debug script to test NPB scraping directly."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from npb.scrapers.baseball_reference import BaseballReferenceNPBScraper


async def test_direct_scraping():
    """Test scraping directly to debug issues."""
    
    scraper = BaseballReferenceNPBScraper()
    
    async with scraper:
        # Test search
        print("Testing search for Ichiro...")
        results = await scraper.search_players("Ichiro")
        print(f"Found {len(results)} results")
        for r in results:
            print(f"  - {r}")
        
        if results:
            # Test stats retrieval
            player_id = results[0]["id"]
            print(f"\nTesting stats for player ID: {player_id}")
            stats = await scraper.get_player_stats(player_id)
            print(f"Stats result: {stats}")
            
            # Try with a specific season
            print(f"\nTesting 2000 season stats...")
            stats_2000 = await scraper.get_player_stats(player_id, 2000)
            print(f"2000 Stats result: {stats_2000}")


if __name__ == "__main__":
    asyncio.run(test_direct_scraping())