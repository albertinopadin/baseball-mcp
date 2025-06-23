"""Live demonstration of Shohei Ohtani's NPB Statistics using the baseball-mcp server"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from npb.api import NPBAPI


async def main():
    """Retrieve and display Ohtani's NPB statistics."""
    
    print("\n" + "="*80)
    print(" "*20 + "⚾ SHOHEI OHTANI NPB CAREER STATISTICS ⚾")
    print("="*80 + "\n")
    
    # Initialize NPB API
    api = NPBAPI()
    
    # Search for Ohtani
    print("🔍 Searching for Shohei Ohtani in NPB database...")
    players = await api.search_player("Shohei Ohtani")
    
    if not players:
        print("❌ Player not found!")
        return
    
    # Get the first match
    player = players[0]
    print(f"✅ Found: {player['name_english']} (ID: {player['id']})")
    
    # Get 2017 stats (his final NPB season)
    print("\n📊 Retrieving 2017 season statistics...")
    stats_data = await api.get_player_stats(player['id'], 2017)
    
    if 'error' in stats_data:
        print(f"❌ Error: {stats_data['error']}")
        return
    
    # Stats are already formatted from the API
    
    # Extract batting and pitching stats
    batting_stats = None
    pitching_stats = None
    
    if stats_data.get('stats'):
        for stat in stats_data['stats']:
            if 'batting_average' in stat:
                batting_stats = stat
            elif 'era' in stat:
                pitching_stats = stat
    
    # Display player info
    print("\n╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                              PLAYER INFORMATION                              ║")
    print("╠══════════════════════════════════════════════════════════════════════════════╣")
    print("║  Name: Shohei Ohtani (大谷 翔平)                                            ║")
    print("║  Team: Hokkaido Nippon-Ham Fighters (2013-2017)                             ║")
    print("║  Position: Pitcher / Designated Hitter / Outfielder                         ║")
    print("║  Final NPB Season: 2017                                                      ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    
    # Display batting stats if available
    if batting_stats:
        print("\n╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                          BATTING STATISTICS - 2017                           ║")
        print("╠═══════╤═════╤═════╤═════╤═════╤═════╤═════╤═════╤═════╤═══════╤═══════╤═════╣")
        print("║ Team  │  G  │  AB │  R  │  H  │ 2B  │ 3B  │ HR  │ RBI │  AVG  │  OBP  │ OPS ║")
        print("╟───────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼───────┼─────╢")
        print(f"║  {batting_stats.get('team', 'F'):^3s}  │ {batting_stats.get('games', 0):3d} │ {batting_stats.get('at_bats', 0):3d} │ {batting_stats.get('runs', 0):3d} │ {batting_stats.get('hits', 0):3d} │ {batting_stats.get('doubles', 0):3d} │ {batting_stats.get('triples', 0):3d} │ {batting_stats.get('home_runs', 0):3d} │ {batting_stats.get('rbis', 0):3d} │ {batting_stats.get('batting_average', 0):.3f} │ {batting_stats.get('on_base_percentage', 0):.3f} │{batting_stats.get('ops', 0):.3f}║")
        print("╚═══════╧═════╧═════╧═════╧═════╧═════╧═════╧═════╧═════╧═══════╧═══════╧═════╝")
        
        # Additional batting stats
        print("\n  📈 Additional Batting Metrics:")
        print(f"     • Slugging Percentage: {batting_stats.get('slugging_percentage', 0):.3f}")
        print(f"     • Walks: {batting_stats.get('walks', 0)}")
        print(f"     • Strikeouts: {batting_stats.get('strikeouts', 0)}")
        print(f"     • Stolen Bases: {batting_stats.get('stolen_bases', 0)}")
    
    # Display pitching stats if available
    if pitching_stats:
        print("\n╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                         PITCHING STATISTICS - 2017                           ║")
        print("╠═══════╤═════╤═════╤═══════╤═══════╤═════╤═════╤═════╤═════╤════════╤═══╤═══╣")
        print("║ Team  │  G  │ W-L │  ERA  │   IP  │  H  │ HR  │ BB  │  K  │  WHIP  │CG │SHO║")
        print("╟───────┼─────┼─────┼───────┼───────┼─────┼─────┼─────┼─────┼────────┼───┼───╢")
        print(f"║  {pitching_stats.get('team', 'F'):^3s}  │ {pitching_stats.get('games', 0):3d} │{pitching_stats.get('wins', 0):2d}-{pitching_stats.get('losses', 0):<2d}│ {pitching_stats.get('era', 0):5.2f} │ {pitching_stats.get('innings_pitched', 0):5.1f} │ {pitching_stats.get('hits_allowed', 0):3d} │ {pitching_stats.get('home_runs_allowed', 0):3d} │ {pitching_stats.get('walks', 0):3d} │ {pitching_stats.get('strikeouts', 0):3d} │ {pitching_stats.get('whip', 0):6.3f} │ {pitching_stats.get('complete_games', 0):1d} │ {pitching_stats.get('shutouts', 0):1d} ║")
        print("╚═══════╧═════╧═════╧═══════╧═══════╧═════╧═════╧═════╧═════╧════════╧═══╧═══╝")
        
        # Additional pitching stats
        print("\n  📈 Additional Pitching Metrics:")
        print(f"     • Games Started: {pitching_stats.get('games_started', 0)}")
        print(f"     • Saves: {pitching_stats.get('saves', 0)}")
        print(f"     • Holds: {pitching_stats.get('holds', 0)}")
        if pitching_stats.get('innings_pitched', 0) > 0:
            k_per_9 = (pitching_stats.get('strikeouts', 0) * 9) / pitching_stats.get('innings_pitched', 0)
            bb_per_9 = (pitching_stats.get('walks', 0) * 9) / pitching_stats.get('innings_pitched', 0)
            print(f"     • K/9: {k_per_9:.1f}")
            print(f"     • BB/9: {bb_per_9:.1f}")
    
    # Career highlights
    print("\n╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                         NPB CAREER HIGHLIGHTS (2013-2017)                    ║")
    print("╠══════════════════════════════════════════════════════════════════════════════╣")
    print("║  🏆 2016 Pacific League MVP                                                  ║")
    print("║  🏆 2015 & 2016 Best Nine Award (Designated Hitter)                          ║")
    print("║  🏆 2015 All-Star Game MVP                                                   ║")
    print("║  ⚾ First NPB player to record 10+ wins and 10+ home runs in a season       ║")
    print("║  ⚡ Fastest pitch: 165 km/h (102.5 mph)                                     ║")
    print("║  🎯 Career NPB Record: 42-15, 2.52 ERA, 624 K in 543 IP                     ║")
    print("║  🏏 Career NPB Batting: .286 AVG, 48 HR, 166 RBI in 403 games               ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    
    print("\n" + "="*80)
    print(" "*25 + f"Generated on {datetime.now().strftime('%B %d, %Y')}")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())