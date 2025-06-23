"""Test NPB player stats retrieval directly"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from npb.providers.scraper_provider import ScraperProvider


async def main():
    """Test getting Ohtani's stats directly."""
    
    provider = ScraperProvider()
    
    print("Testing NPB player stats retrieval...")
    print("="*60)
    
    # Search for Ohtani first
    print("\n1. Searching for Shohei Ohtani...")
    players = await provider.search_player("Shohei Ohtani")
    
    if players:
        print(f"Found {len(players)} player(s):")
        for p in players:
            player_id = p.get('player_id', p.get('id', 'Unknown'))
            name = p.get('name_english', p.get('name', 'Unknown'))
            print(f"  - {name} (ID: {player_id})")
            print(f"    Full data: {p}")
    else:
        print("No players found")
        return
    
    # Get stats for the first player found
    if players:
        player_id = players[0].get('player_id', players[0].get('id', 'Unknown'))
        print(f"\n2. Getting stats for player ID: {player_id}")
        
        # Get 2017 stats
        stats_2017 = await provider.get_player_stats(player_id, 2017)
        
        if "error" not in stats_2017:
            print(f"\n2017 Season Stats:")
            print(f"Player: {stats_2017.get('player_info', {}).get('name_english', 'Unknown')}")
            print(f"Stats Type: {stats_2017.get('stats_type', 'Unknown')}")
            
            if stats_2017.get('stats'):
                for stat in stats_2017['stats']:
                    print(f"\nStats data: {stat}")
        else:
            print(f"Error: {stats_2017['error']}")
        
        # Get career stats (no season specified)
        print("\n3. Getting career stats...")
        career_stats = await provider.get_player_stats(player_id, None)
        
        if "error" not in career_stats:
            print(f"\nCareer Stats:")
            print(f"Player: {career_stats.get('player_info', {}).get('name_english', 'Unknown')}")
            print(f"Stats Type: {career_stats.get('stats_type', 'Unknown')}")
            print(f"Number of seasons: {len(career_stats.get('stats', []))}")
        else:
            print(f"Error: {career_stats['error']}")


if __name__ == "__main__":
    asyncio.run(main())