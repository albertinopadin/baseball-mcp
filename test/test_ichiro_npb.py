#!/usr/bin/env python
"""Test script to get Ichiro Suzuki's NPB career statistics."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from npb import NPBAPI


async def main():
    """Get Ichiro's NPB career stats."""
    api = NPBAPI()
    
    print("Searching for Ichiro Suzuki in NPB database...")
    print("=" * 60)
    
    # Search for Ichiro
    search_results = await api.search_player("Ichiro Suzuki")
    print(search_results)
    
    # Try different search terms
    for search_term in ["Ichiro", "Suzuki Ichiro"]:
        print(f"\nSearching for '{search_term}'...")
        print("=" * 60)
        results = await api.search_player(search_term)
        print(results)
    
    # Get Ichiro's career stats by trying to fetch each year
    print("\n\nIchiro's NPB Career Statistics (1992-2000)")
    print("=" * 80)
    
    # Ichiro played in NPB from 1992-2000
    career_stats = []
    for year in range(1992, 2001):
        print(f"\nFetching {year} season...")
        try:
            # We need to find his player ID first
            # Based on the pattern, it might be something like suzuki-000ich
            stats = await api.get_player_stats("suzuki-000ich", str(year))
            career_stats.append((year, stats))
        except Exception as e:
            # Try alternate ID formats
            for alt_id in ["suzuki,_ichiro", "ichiro-suzuki", "suzuki_ichiro"]:
                try:
                    stats = await api.get_player_stats(alt_id, str(year))
                    career_stats.append((year, stats))
                    break
                except:
                    continue
            else:
                print(f"Could not fetch {year} stats: {e}")
    
    # Display career summary
    if career_stats:
        print("\n\nCareer Summary:")
        print("=" * 120)
        print(f"{'Year':<6} {'Team':<12} {'G':<5} {'AB':<6} {'R':<5} {'H':<5} {'2B':<5} {'3B':<5} {'HR':<5} {'RBI':<5} {'SB':<5} {'AVG':<7} {'OBP':<7} {'SLG':<7} {'OPS':<7}")
        print("-" * 120)
        
        # Calculate career totals
        total_g = total_ab = total_r = total_h = total_2b = total_3b = total_hr = total_rbi = total_sb = 0
        
        for year, stats_text in career_stats:
            # Parse the stats from the formatted text
            # This is a simplified parser - in reality we'd need to handle the actual format
            print(f"{year:<6} [Stats would be parsed and displayed here]")
            
        # Would calculate and display career totals here


if __name__ == "__main__":
    asyncio.run(main())