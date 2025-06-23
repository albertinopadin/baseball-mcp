"""Comprehensive Shohei Ohtani NPB Career Statistics (2013-2017)"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from npb.scrapers.npb_official import NPBOfficialScraper


async def get_ohtani_stats_for_year(scraper, year):
    """Get Ohtani's stats for a specific year."""
    # Get batting stats
    batting_stats = await scraper.get_player_stats_by_year(year, "batting")
    
    # Get pitching stats
    pitching_stats = await scraper.get_player_stats_by_year(year, "pitching")
    
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
    
    return ohtani_batting, ohtani_pitching


async def main():
    """Retrieve and display Ohtani's complete NPB career statistics."""
    
    print("\n" + "="*120)
    print(" "*40 + "⚾ SHOHEI OHTANI NPB CAREER STATISTICS (2013-2017) ⚾")
    print("="*120 + "\n")
    
    # Initialize scraper
    scraper = NPBOfficialScraper()
    
    # Career totals accumulators
    career_batting = {
        'games': 0, 'plate_appearances': 0, 'at_bats': 0, 'runs': 0, 'hits': 0,
        'doubles': 0, 'triples': 0, 'home_runs': 0, 'rbis': 0, 'walks': 0,
        'strikeouts': 0, 'stolen_bases': 0, 'total_bases': 0
    }
    
    career_pitching = {
        'games': 0, 'games_started': 0, 'wins': 0, 'losses': 0, 'saves': 0,
        'innings_pitched': 0, 'hits_allowed': 0, 'runs_allowed': 0, 'earned_runs': 0,
        'home_runs_allowed': 0, 'walks': 0, 'strikeouts': 0, 'complete_games': 0,
        'shutouts': 0
    }
    
    async with scraper:
        print("📊 SEASON-BY-SEASON BATTING STATISTICS")
        print("="*120)
        print(f"{'Year':<6} {'Team':<20} {'G':<5} {'PA':<5} {'AB':<5} {'R':<5} {'H':<5} {'2B':<5} {'3B':<5} {'HR':<5} {'RBI':<5} {'BB':<5} {'SO':<5} {'SB':<5} {'AVG':<7} {'OBP':<7} {'SLG':<7} {'OPS':<7}")
        print("-"*120)
        
        # Get stats for each year
        for year in range(2013, 2018):
            batting, pitching = await get_ohtani_stats_for_year(scraper, year)
            
            if batting:
                # Extract batting stats
                g = batting.get('games', 0)
                pa = batting.get('plate_appearances', 0)
                ab = batting.get('at_bats', 0)
                r = batting.get('runs', 0)
                h = batting.get('hits', 0)
                doubles = batting.get('doubles', 0)
                triples = batting.get('triples', 0)
                hr = batting.get('home_runs', 0)
                rbi = batting.get('rbis', 0)
                bb = batting.get('walks', 0)
                so = batting.get('strikeouts', 0)
                sb = batting.get('stolen_bases', 0)
                avg = batting.get('batting_average', 0)
                obp = batting.get('on_base_percentage', 0)
                slg = batting.get('slugging_percentage', 0)
                ops = batting.get('ops', 0)
                
                print(f"{year:<6} {'Nippon-Ham Fighters':<20} {g:<5} {pa:<5} {ab:<5} {r:<5} {h:<5} {doubles:<5} {triples:<5} {hr:<5} {rbi:<5} {bb:<5} {so:<5} {sb:<5} {avg:<7.3f} {obp:<7.3f} {slg:<7.3f} {ops:<7.3f}")
                
                # Add to career totals
                career_batting['games'] += g
                career_batting['plate_appearances'] += pa
                career_batting['at_bats'] += ab
                career_batting['runs'] += r
                career_batting['hits'] += h
                career_batting['doubles'] += doubles
                career_batting['triples'] += triples
                career_batting['home_runs'] += hr
                career_batting['rbis'] += rbi
                career_batting['walks'] += bb
                career_batting['strikeouts'] += so
                career_batting['stolen_bases'] += sb
                career_batting['total_bases'] += h + doubles + (2 * triples) + (3 * hr)
            else:
                print(f"{year:<6} {'Nippon-Ham Fighters':<20} {'--':<5} {'--':<5} {'--':<5} {'--':<5} {'--':<5} {'--':<5} {'--':<5} {'--':<5} {'--':<5} {'--':<5} {'--':<5} {'--':<5} {'--':<7} {'--':<7} {'--':<7} {'--':<7}")
        
        print("-"*120)
        
        # Calculate career batting averages
        if career_batting['at_bats'] > 0:
            career_avg = career_batting['hits'] / career_batting['at_bats']
            career_obp = (career_batting['hits'] + career_batting['walks']) / career_batting['plate_appearances'] if career_batting['plate_appearances'] > 0 else 0
            career_slg = career_batting['total_bases'] / career_batting['at_bats']
            career_ops = career_obp + career_slg
        else:
            career_avg = career_obp = career_slg = career_ops = 0
        
        print(f"{'TOTAL':<6} {'':<20} {career_batting['games']:<5} {career_batting['plate_appearances']:<5} {career_batting['at_bats']:<5} {career_batting['runs']:<5} {career_batting['hits']:<5} {career_batting['doubles']:<5} {career_batting['triples']:<5} {career_batting['home_runs']:<5} {career_batting['rbis']:<5} {career_batting['walks']:<5} {career_batting['strikeouts']:<5} {career_batting['stolen_bases']:<5} {career_avg:<7.3f} {career_obp:<7.3f} {career_slg:<7.3f} {career_ops:<7.3f}")
        
        print("\n\n📊 SEASON-BY-SEASON PITCHING STATISTICS")
        print("="*120)
        print(f"{'Year':<6} {'Team':<20} {'G':<5} {'GS':<5} {'W':<5} {'L':<5} {'SV':<5} {'IP':<7} {'H':<5} {'R':<5} {'ER':<5} {'HR':<5} {'BB':<5} {'SO':<5} {'ERA':<7} {'WHIP':<7} {'K/9':<7} {'BB/9':<7}")
        print("-"*120)
        
        # Get pitching stats for each year
        for year in range(2013, 2018):
            batting, pitching = await get_ohtani_stats_for_year(scraper, year)
            
            if pitching:
                # Extract pitching stats
                g = pitching.get('games', 0)
                gs = pitching.get('games_started', 0)
                w = pitching.get('wins', 0)
                l = pitching.get('losses', 0)
                sv = pitching.get('saves', 0)
                ip = pitching.get('innings_pitched', 0)
                h_allowed = pitching.get('hits_allowed', 0)
                r_allowed = pitching.get('runs_allowed', 0)
                er = pitching.get('earned_runs', 0)
                hr_allowed = pitching.get('home_runs_allowed', 0)
                bb = pitching.get('walks', 0)
                k = pitching.get('strikeouts', 0)
                era = pitching.get('era', 0)
                whip = pitching.get('whip', 0)
                
                # Calculate K/9 and BB/9
                k_per_9 = (k * 9) / ip if ip > 0 else 0
                bb_per_9 = (bb * 9) / ip if ip > 0 else 0
                
                print(f"{year:<6} {'Nippon-Ham Fighters':<20} {g:<5} {gs:<5} {w:<5} {l:<5} {sv:<5} {ip:<7.1f} {h_allowed:<5} {r_allowed:<5} {er:<5} {hr_allowed:<5} {bb:<5} {k:<5} {era:<7.2f} {whip:<7.3f} {k_per_9:<7.1f} {bb_per_9:<7.1f}")
                
                # Add to career totals
                career_pitching['games'] += g
                career_pitching['games_started'] += gs
                career_pitching['wins'] += w
                career_pitching['losses'] += l
                career_pitching['saves'] += sv
                career_pitching['innings_pitched'] += ip
                career_pitching['hits_allowed'] += h_allowed
                career_pitching['runs_allowed'] += r_allowed
                career_pitching['earned_runs'] += er
                career_pitching['home_runs_allowed'] += hr_allowed
                career_pitching['walks'] += bb
                career_pitching['strikeouts'] += k
            else:
                print(f"{year:<6} {'Nippon-Ham Fighters':<20} {'--':<5} {'--':<5} {'--':<5} {'--':<5} {'--':<5} {'--':<7} {'--':<5} {'--':<5} {'--':<5} {'--':<5} {'--':<5} {'--':<5} {'--':<7} {'--':<7} {'--':<7} {'--':<7}")
        
        print("-"*120)
        
        # Calculate career pitching averages
        if career_pitching['innings_pitched'] > 0:
            career_era = (career_pitching['earned_runs'] * 9) / career_pitching['innings_pitched']
            career_whip = (career_pitching['hits_allowed'] + career_pitching['walks']) / career_pitching['innings_pitched']
            career_k9 = (career_pitching['strikeouts'] * 9) / career_pitching['innings_pitched']
            career_bb9 = (career_pitching['walks'] * 9) / career_pitching['innings_pitched']
        else:
            career_era = career_whip = career_k9 = career_bb9 = 0
        
        print(f"{'TOTAL':<6} {'':<20} {career_pitching['games']:<5} {career_pitching['games_started']:<5} {career_pitching['wins']:<5} {career_pitching['losses']:<5} {career_pitching['saves']:<5} {career_pitching['innings_pitched']:<7.1f} {career_pitching['hits_allowed']:<5} {career_pitching['runs_allowed']:<5} {career_pitching['earned_runs']:<5} {career_pitching['home_runs_allowed']:<5} {career_pitching['walks']:<5} {career_pitching['strikeouts']:<5} {career_era:<7.2f} {career_whip:<7.3f} {career_k9:<7.1f} {career_bb9:<7.1f}")
    
    # NPB Achievements
    print("\n\n🏆 NPB CAREER ACHIEVEMENTS")
    print("="*120)
    print("• 2016 Pacific League MVP")
    print("• 2x Best Nine Award (DH) - 2015, 2016")
    print("• 2015 All-Star Game MVP")
    print("• First NPB player with 10+ wins and 10+ home runs in a season (2014)")
    print("• First NPB player with 15+ wins and 100+ strikeouts while batting .280+ (2015)")
    print("• Fastest pitch: 165 km/h (102.5 mph) - NPB record at the time")
    print("• 2016 Japan Series Champion with Nippon-Ham Fighters")
    
    print("\n" + "="*120)
    print(" "*45 + f"Generated on {datetime.now().strftime('%B %d, %Y')}")
    print("="*120 + "\n")


if __name__ == "__main__":
    asyncio.run(main())