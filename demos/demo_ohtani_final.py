"""Final demonstration of Shohei Ohtani's 2017 NPB Statistics"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from npb.scrapers.npb_official import NPBOfficialScraper


async def main():
    """Retrieve and display Ohtani's NPB statistics with beautiful formatting."""
    
    print("\n" + "="*90)
    print(" "*25 + "⚾ SHOHEI OHTANI NPB STATISTICS ⚾")
    print("="*90 + "\n")
    
    # Initialize scraper
    scraper = NPBOfficialScraper()
    
    async with scraper:
        # Get 2017 stats directly
        print("📊 Retrieving Shohei Ohtani's 2017 NPB Season Statistics...\n")
        
        # Get batting stats
        batting_stats = await scraper.get_player_stats_by_year(2017, "batting")
        
        # Get pitching stats
        pitching_stats = await scraper.get_player_stats_by_year(2017, "pitching")
        
        # Find Ohtani's stats
        ohtani_batting = None
        ohtani_pitching = None
        
        for stat in batting_stats:
            if "otani" in stat.get("player_name", "").lower():
                ohtani_batting = stat
                break
        
        for stat in pitching_stats:
            if "otani" in stat.get("player_name", "").lower():
                ohtani_pitching = stat
                break
    
    if not ohtani_batting and not ohtani_pitching:
        print("❌ Could not find Shohei Ohtani's stats")
        return
    
    # Display player info
    print("╔════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                   PLAYER INFORMATION                                   ║")
    print("╠════════════════════════════════════════════════════════════════════════════════════════╣")
    print("║  Name: SHOHEI OHTANI (大谷 翔平)                                                      ║")
    print("║  Team: Hokkaido Nippon-Ham Fighters                                                   ║")
    print("║  Position: Pitcher / Designated Hitter / Outfielder                                   ║")
    print("║  NPB Career: 2013-2017 (5 seasons)                                                    ║")
    print("╚════════════════════════════════════════════════════════════════════════════════════════╝")
    
    # Display batting stats
    if ohtani_batting:
        print("\n╔════════════════════════════════════════════════════════════════════════════════════════╗")
        print("║                              2017 BATTING STATISTICS                                   ║")
        print("╠═════════╤═════╤═════╤═════╤═════╤═════╤═════╤═════╤═════╤═════╤═══════╤═══════╤═════╣")
        print("║  TEAM   │  G  │ PA  │ AB  │  R  │  H  │ 2B  │ 3B  │ HR  │ RBI │  BB   │  AVG  │ OPS ║")
        print("╟─────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼───────┼─────╢")
        
        g = ohtani_batting.get('games', 0)
        pa = ohtani_batting.get('plate_appearances', 0)
        ab = ohtani_batting.get('at_bats', 0)
        r = ohtani_batting.get('runs', 0)
        h = ohtani_batting.get('hits', 0)
        doubles = ohtani_batting.get('doubles', 0)
        triples = ohtani_batting.get('triples', 0)
        hr = ohtani_batting.get('home_runs', 0)
        rbi = ohtani_batting.get('rbis', 0)
        bb = ohtani_batting.get('walks', 0)
        avg = ohtani_batting.get('batting_average', 0)
        ops = ohtani_batting.get('ops', 0)
        
        print(f"║ FIGHTERS│ {g:3d} │ {pa:3d} │ {ab:3d} │ {r:3d} │ {h:3d} │ {doubles:3d} │ {triples:3d} │ {hr:3d} │ {rbi:3d} │  {bb:3d}  │ {avg:5.3f} │{ops:5.3f}║")
        print("╚═════════╧═════╧═════╧═════╧═════╧═════╧═════╧═════╧═════╧═════╧═══════╧═══════╧═════╝")
        
        # Additional batting details
        print("\n  📈 Batting Breakdown:")
        print(f"     • On-Base Percentage: {ohtani_batting.get('on_base_percentage', 0):.3f}")
        print(f"     • Slugging Percentage: {ohtani_batting.get('slugging_percentage', 0):.3f}")
        print(f"     • Strikeouts: {ohtani_batting.get('strikeouts', 0)}")
        print(f"     • Stolen Bases: {ohtani_batting.get('stolen_bases', 0)}")
    
    # Display pitching stats
    if ohtani_pitching:
        print("\n╔════════════════════════════════════════════════════════════════════════════════════════╗")
        print("║                              2017 PITCHING STATISTICS                                  ║")
        print("╠═════════╤═════╤═══════╤═══════╤═══════╤═════╤═════╤═════╤═════╤════════╤═════╤═════╣")
        print("║  TEAM   │  G  │  W-L  │  ERA  │   IP  │  H  │ HR  │ BB  │  K  │  WHIP  │ CG  │ SHO ║")
        print("╟─────────┼─────┼───────┼───────┼───────┼─────┼─────┼─────┼─────┼────────┼─────┼─────╢")
        
        g = ohtani_pitching.get('games', 0)
        w = ohtani_pitching.get('wins', 0)
        l = ohtani_pitching.get('losses', 0)
        era = ohtani_pitching.get('era', 0)
        ip = ohtani_pitching.get('innings_pitched', 0)
        h_allowed = ohtani_pitching.get('hits_allowed', 0)
        hr_allowed = ohtani_pitching.get('home_runs_allowed', 0)
        bb = ohtani_pitching.get('walks', 0)
        k = ohtani_pitching.get('strikeouts', 0)
        whip = ohtani_pitching.get('whip', 0)
        cg = ohtani_pitching.get('complete_games', 0)
        sho = ohtani_pitching.get('shutouts', 0)
        
        print(f"║ FIGHTERS│  {g:2d} │  {w:1d}-{l:1d}  │ {era:5.2f} │ {ip:5.1f} │ {h_allowed:3d} │ {hr_allowed:3d} │ {bb:3d} │ {k:3d} │ {whip:6.3f} │  {cg:1d}  │  {sho:1d}  ║")
        print("╚═════════╧═════╧═══════╧═══════╧═══════╧═════╧═════╧═════╧═════╧════════╧═════╧═════╝")
        
        # Additional pitching details
        print("\n  📈 Pitching Breakdown:")
        print(f"     • Games Started: {ohtani_pitching.get('games_started', 0)}")
        print(f"     • Saves: {ohtani_pitching.get('saves', 0)}")
        print(f"     • Holds: {ohtani_pitching.get('holds', 0)}")
        if ip > 0:
            k_per_9 = (k * 9) / ip
            bb_per_9 = (bb * 9) / ip
            print(f"     • K/9: {k_per_9:.1f}")
            print(f"     • BB/9: {bb_per_9:.1f}")
    
    # Season summary
    print("\n╔════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                 2017 SEASON SUMMARY                                    ║")
    print("╠════════════════════════════════════════════════════════════════════════════════════════╣")
    print("║  🏏 Limited to 65 games due to ankle injury (batting)                                  ║")
    print("║  ⚾ Only 5 pitching appearances due to injury recovery                                 ║")
    print("║  💪 Still managed elite performance when healthy:                                      ║")
    print("║     • .332 batting average (would have led Pacific League if qualified)               ║")
    print("║     • 3.20 ERA with 10.3 K/9 in limited innings                                       ║")
    print("║  🚀 Signed with Los Angeles Angels after the season                                    ║")
    print("╚════════════════════════════════════════════════════════════════════════════════════════╝")
    
    # NPB Career totals
    print("\n╔════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                              NPB CAREER TOTALS (2013-2017)                             ║")
    print("╠════════════════════════════════════════════════════════════════════════════════════════╣")
    print("║  BATTING:  403 Games │ .286 AVG │ 48 HR │ 166 RBI │ .859 OPS                          ║")
    print("║  PITCHING: 85 Games │ 42-15 W-L │ 2.52 ERA │ 543.0 IP │ 624 K │ 1.076 WHIP           ║")
    print("╠════════════════════════════════════════════════════════════════════════════════════════╣")
    print("║  🏆 ACHIEVEMENTS:                                                                      ║")
    print("║     • 2016 Pacific League MVP                                                          ║")
    print("║     • 2x Best Nine Award (DH) - 2015, 2016                                            ║")
    print("║     • 2015 All-Star Game MVP                                                          ║")
    print("║     • First NPB player with 10+ wins and 10+ home runs in a season (2014)             ║")
    print("║     • Fastest pitch: 165 km/h (102.5 mph) - NPB record at the time                    ║")
    print("╚════════════════════════════════════════════════════════════════════════════════════════╝")
    
    print("\n" + "="*90)
    print(" "*30 + f"Generated on {datetime.now().strftime('%B %d, %Y')}")
    print("="*90 + "\n")


if __name__ == "__main__":
    asyncio.run(main())