#!/usr/bin/env python3
"""
Import NPB historical data into SQLite database.
This script processes various data sources and imports them into the NPB database.
"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "src"))

from npb.data.database import NPBDatabase
from npb.data.import_dir.npb_historical_dataset import NPB_HISTORICAL_PLAYERS, NPB_SEASONAL_STATS


def clear_database(db):
    """Clear existing data from database."""
    print("Clearing existing database...")
    with db.get_connection() as conn:
        cursor = conn.cursor()
        # Clear in correct order due to foreign keys
        cursor.execute("DELETE FROM batting_stats")
        cursor.execute("DELETE FROM pitching_stats")
        cursor.execute("DELETE FROM players")
        cursor.execute("DELETE FROM teams")
        conn.commit()
    print("Database cleared.")


def import_teams(db):
    """Import NPB teams into database."""
    print("\nImporting NPB teams...")
    
    teams = [
        # Central League
        {"team_id": "giants", "name_english": "Yomiuri Giants", "name_japanese": "読売ジャイアンツ", 
         "abbreviation": "YG", "league": "Central", "city": "Tokyo", "founded_year": 1934},
        {"team_id": "tigers", "name_english": "Hanshin Tigers", "name_japanese": "阪神タイガース", 
         "abbreviation": "HT", "league": "Central", "city": "Nishinomiya", "founded_year": 1935},
        {"team_id": "dragons", "name_english": "Chunichi Dragons", "name_japanese": "中日ドラゴンズ", 
         "abbreviation": "CD", "league": "Central", "city": "Nagoya", "founded_year": 1936},
        {"team_id": "carp", "name_english": "Hiroshima Toyo Carp", "name_japanese": "広島東洋カープ", 
         "abbreviation": "HC", "league": "Central", "city": "Hiroshima", "founded_year": 1949},
        {"team_id": "swallows", "name_english": "Tokyo Yakult Swallows", "name_japanese": "東京ヤクルトスワローズ", 
         "abbreviation": "YS", "league": "Central", "city": "Tokyo", "founded_year": 1950},
        {"team_id": "baystars", "name_english": "Yokohama DeNA BayStars", "name_japanese": "横浜DeNAベイスターズ", 
         "abbreviation": "DB", "league": "Central", "city": "Yokohama", "founded_year": 1950},
        
        # Pacific League
        {"team_id": "fighters", "name_english": "Hokkaido Nippon-Ham Fighters", "name_japanese": "北海道日本ハムファイターズ", 
         "abbreviation": "HF", "league": "Pacific", "city": "Sapporo", "founded_year": 1946},
        {"team_id": "lions", "name_english": "Saitama Seibu Lions", "name_japanese": "埼玉西武ライオンズ", 
         "abbreviation": "SL", "league": "Pacific", "city": "Tokorozawa", "founded_year": 1950},
        {"team_id": "marines", "name_english": "Chiba Lotte Marines", "name_japanese": "千葉ロッテマリーンズ", 
         "abbreviation": "LM", "league": "Pacific", "city": "Chiba", "founded_year": 1950},
        {"team_id": "buffaloes", "name_english": "Orix Buffaloes", "name_japanese": "オリックス・バファローズ", 
         "abbreviation": "OB", "league": "Pacific", "city": "Osaka", "founded_year": 1936},
        {"team_id": "hawks", "name_english": "Fukuoka SoftBank Hawks", "name_japanese": "福岡ソフトバンクホークス", 
         "abbreviation": "SH", "league": "Pacific", "city": "Fukuoka", "founded_year": 1938},
        {"team_id": "eagles", "name_english": "Tohoku Rakuten Golden Eagles", "name_japanese": "東北楽天ゴールデンイーグルス", 
         "abbreviation": "RE", "league": "Pacific", "city": "Sendai", "founded_year": 2004},
        
        # Historical teams (for data consistency)
        {"team_id": "orix", "name_english": "Orix BlueWave", "name_japanese": "オリックス・ブルーウェーブ", 
         "abbreviation": "OBW", "league": "Pacific", "city": "Kobe", "founded_year": 1991},
        {"team_id": "kintetsu", "name_english": "Kintetsu Buffaloes", "name_japanese": "近鉄バファローズ", 
         "abbreviation": "KB", "league": "Pacific", "city": "Osaka", "founded_year": 1950},
        {"team_id": "softbank", "name_english": "Fukuoka SoftBank Hawks", "name_japanese": "福岡ソフトバンクホークス", 
         "abbreviation": "SBH", "league": "Pacific", "city": "Fukuoka", "founded_year": 1938}
    ]
    
    count = 0
    for team in teams:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            fields = list(team.keys())
            placeholders = ['?' for _ in fields]
            values = [team[field] for field in fields]
            
            query = f"""
                INSERT OR REPLACE INTO teams ({', '.join(fields)})
                VALUES ({', '.join(placeholders)})
            """
            cursor.execute(query, values)
            conn.commit()
            count += 1
    
    print(f"Imported {count} teams.")


def import_players(db):
    """Import historical players into database."""
    print("\nImporting historical players...")
    
    count = 0
    for player in NPB_HISTORICAL_PLAYERS:
        # Extract player info (without career stats)
        player_data = {
            "player_id": player["player_id"],
            "name_english": player["name_english"],
            "name_japanese": player.get("name_japanese"),
            "name_romanized_variants": json.dumps(player.get("name_romanized_variants", [])),
            "birth_date": player.get("birth_date"),
            "birth_place": player.get("birth_place"),
            "height": player.get("height"),
            "weight": player.get("weight"),
            "bats": player.get("bats"),
            "throws": player.get("throws"),
            "debut_date": player.get("debut_date"),
            "final_game": player.get("final_game")
        }
        
        db.insert_player(player_data)
        count += 1
        print(f"  - {player['name_english']}")
    
    # Also import players from historical_data.py
    from npb.data.historical_data import HISTORICAL_PLAYERS
    for player_key, player_data in HISTORICAL_PLAYERS.items():
        player_data["name_romanized_variants"] = json.dumps(player_data.get("name_romanized_variants", []))
        db.insert_player(player_data)
        count += 1
        print(f"  - {player_data['name_english']}")
    
    print(f"Imported {count} players.")


def import_batting_stats(db):
    """Import batting statistics."""
    print("\nImporting batting statistics...")
    
    count = 0
    
    # Import season-by-season stats
    for player_id, seasons in NPB_SEASONAL_STATS.items():
        for season_stats in seasons:
            stats = season_stats.copy()
            stats['player_id'] = player_id
            stats['data_source'] = 'historical_import'
            stats['data_quality'] = 'complete'
            
            # Calculate missing percentages if we have the data
            if 'on_base_percentage' not in stats and stats.get('at_bats', 0) > 0:
                # Simple OBP calculation (would need walks/HBP for accurate)
                stats['on_base_percentage'] = stats.get('batting_average', 0.0)
            
            if 'slugging_percentage' not in stats and stats.get('at_bats', 0) > 0:
                # Calculate SLG
                total_bases = (stats.get('hits', 0) - stats.get('doubles', 0) - stats.get('triples', 0) - stats.get('home_runs', 0) +
                              2 * stats.get('doubles', 0) + 3 * stats.get('triples', 0) + 4 * stats.get('home_runs', 0))
                stats['slugging_percentage'] = round(total_bases / stats['at_bats'], 3)
            
            if 'ops' not in stats:
                stats['ops'] = round(stats.get('on_base_percentage', 0) + stats.get('slugging_percentage', 0), 3)
            
            db.insert_batting_stats(stats)
            count += 1
    
    # Import career totals as aggregated seasonal data (for players without seasonal breakdowns)
    for player in NPB_HISTORICAL_PLAYERS:
        if player["player_id"] not in NPB_SEASONAL_STATS and "batting" in player.get("career_stats", {}):
            # Create a single "career" entry
            career = player["career_stats"]["batting"]
            
            # For now, we'll skip players without seasonal data
            # In a real implementation, we'd try to find seasonal data from other sources
            print(f"  - Skipping career-only data for {player['name_english']} (need seasonal breakdown)")
    
    # Import from historical_data.py
    from npb.data.historical_data import (
        ICHIRO_BATTING_STATS, OH_BATTING_STATS, KAWAKAMI_BATTING_STATS, RHODES_BATTING_STATS
    )
    
    for stats in ICHIRO_BATTING_STATS:
        stats['player_id'] = 'suzuki-ichiro'
        stats['data_source'] = 'historical_import'
        stats['data_quality'] = 'complete'
        db.insert_batting_stats(stats)
        count += 1
    
    for stats in OH_BATTING_STATS:
        stats['player_id'] = 'oh-sadaharu'
        stats['data_source'] = 'historical_import'
        stats['data_quality'] = 'complete'
        db.insert_batting_stats(stats)
        count += 1
    
    for stats in KAWAKAMI_BATTING_STATS:
        stats['player_id'] = 'kawakami-tetsuharu'
        stats['data_source'] = 'historical_import'
        stats['data_quality'] = 'complete'
        db.insert_batting_stats(stats)
        count += 1
    
    for stats in RHODES_BATTING_STATS:
        stats['player_id'] = 'rhodes-tuffy'
        stats['data_source'] = 'historical_import'
        stats['data_quality'] = 'complete'
        db.insert_batting_stats(stats)
        count += 1
    
    print(f"Imported {count} batting stat records.")


def import_pitching_stats(db):
    """Import pitching statistics."""
    print("\nImporting pitching statistics...")
    
    # For now, only Kaneda has pitching stats in our dataset
    # In a real implementation, we'd have more pitchers
    
    # Sample data for Kaneda Masaichi
    kaneda_seasons = [
        {"season": 1950, "team_id": "swallows", "wins": 8, "losses": 16, "era": 5.13, "games": 33, "innings_pitched": 187.0, "strikeouts": 71},
        {"season": 1951, "team_id": "swallows", "wins": 9, "losses": 19, "era": 3.65, "games": 35, "innings_pitched": 223.0, "strikeouts": 97},
        {"season": 1952, "team_id": "swallows", "wins": 9, "losses": 19, "era": 3.05, "games": 39, "innings_pitched": 256.0, "strikeouts": 143},
        {"season": 1957, "team_id": "swallows", "wins": 28, "losses": 16, "era": 1.63, "games": 53, "innings_pitched": 344.0, "strikeouts": 306},
        {"season": 1958, "team_id": "swallows", "wins": 31, "losses": 14, "era": 1.30, "games": 52, "innings_pitched": 373.0, "strikeouts": 311},
        {"season": 1964, "team_id": "swallows", "wins": 27, "losses": 9, "era": 1.84, "games": 40, "innings_pitched": 323.0, "strikeouts": 237},
        {"season": 1965, "team_id": "giants", "wins": 14, "losses": 17, "era": 2.08, "games": 33, "innings_pitched": 247.0, "strikeouts": 152},
        {"season": 1969, "team_id": "giants", "wins": 4, "losses": 11, "era": 3.51, "games": 23, "innings_pitched": 138.0, "strikeouts": 71}
    ]
    
    count = 0
    for stats in kaneda_seasons:
        stats['player_id'] = 'kaneda-masaichi'
        stats['data_source'] = 'historical_import'
        stats['data_quality'] = 'partial'  # We don't have complete stats
        
        db.insert_pitching_stats(stats)
        count += 1
    
    print(f"Imported {count} pitching stat records.")


def verify_import(db):
    """Verify the imported data."""
    print("\nVerifying imported data...")
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Count players
        cursor.execute("SELECT COUNT(*) FROM players")
        player_count = cursor.fetchone()[0]
        print(f"  - Total players: {player_count}")
        
        # Count teams
        cursor.execute("SELECT COUNT(*) FROM teams")
        team_count = cursor.fetchone()[0]
        print(f"  - Total teams: {team_count}")
        
        # Count batting stats
        cursor.execute("SELECT COUNT(*) FROM batting_stats")
        batting_count = cursor.fetchone()[0]
        print(f"  - Total batting stat records: {batting_count}")
        
        # Count pitching stats
        cursor.execute("SELECT COUNT(*) FROM pitching_stats")
        pitching_count = cursor.fetchone()[0]
        print(f"  - Total pitching stat records: {pitching_count}")
        
        # Sample some players
        cursor.execute("""
            SELECT p.name_english, COUNT(bs.season) as seasons, SUM(bs.home_runs) as total_hrs
            FROM players p
            LEFT JOIN batting_stats bs ON p.player_id = bs.player_id
            GROUP BY p.player_id
            ORDER BY total_hrs DESC NULLS LAST
            LIMIT 10
        """)
        
        print("\n  Top 10 home run hitters:")
        for row in cursor.fetchall():
            name, seasons, hrs = row
            if hrs:
                print(f"    - {name}: {hrs} HRs in {seasons} seasons")


def main():
    """Main import function."""
    print("NPB Historical Data Import")
    print("=" * 50)
    
    # Initialize database
    db = NPBDatabase()
    
    # Clear existing data
    clear_database(db)
    
    # Import data
    import_teams(db)
    import_players(db)
    import_batting_stats(db)
    import_pitching_stats(db)
    
    # Verify
    verify_import(db)
    
    print("\nImport completed successfully!")


if __name__ == "__main__":
    main()