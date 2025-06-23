"""Historical NPB player data for testing and initial database population."""

# Test data for three legendary NPB players
HISTORICAL_PLAYERS = {
    "ichiro": {
        "player_id": "suzuki-ichiro",
        "name_english": "Ichiro Suzuki",
        "name_japanese": "鈴木一朗",
        "name_romanized_variants": ["Suzuki Ichiro", "Ichiro", "Suzuki, Ichiro"],
        "birth_date": "1973-10-22",
        "birth_place": "Kasugai, Aichi, Japan",
        "height": "180cm",
        "weight": "79kg",
        "bats": "Left",
        "throws": "Right",
        "debut_date": "1992-07-11",
        "final_game": "2000-10-09"  # NPB final game
    },
    "oh": {
        "player_id": "oh-sadaharu",
        "name_english": "Sadaharu Oh",
        "name_japanese": "王貞治",
        "name_romanized_variants": ["Oh Sadaharu", "Wang Chen-chih", "O Sadaharu"],
        "birth_date": "1940-05-20",
        "birth_place": "Tokyo, Japan",
        "height": "177cm",
        "weight": "79kg",
        "bats": "Left",
        "throws": "Left",
        "debut_date": "1959-04-11",
        "final_game": "1980-10-12"
    },
    "kawakami": {
        "player_id": "kawakami-tetsuharu",
        "name_english": "Tetsuharu Kawakami",
        "name_japanese": "川上哲治",
        "name_romanized_variants": ["Kawakami Tetsuharu", "Kawakami, Tetsuharu"],
        "birth_date": "1920-03-23",
        "birth_place": "Hitoyoshi, Kumamoto, Japan",
        "height": "174cm",
        "weight": "72kg",
        "bats": "Left",
        "throws": "Right",
        "debut_date": "1938-04-29",
        "final_game": "1958-10-23"
    }
}

# Ichiro's NPB batting statistics (1992-2000)
ICHIRO_BATTING_STATS = [
    {"season": 1992, "team_id": "orix", "games": 58, "at_bats": 95, "runs": 9, "hits": 24, "doubles": 5, "triples": 0, "home_runs": 0, "rbis": 5, "stolen_bases": 3, "walks": 6, "strikeouts": 16, "batting_average": 0.253},
    {"season": 1993, "team_id": "orix", "games": 43, "at_bats": 64, "runs": 4, "hits": 12, "doubles": 1, "triples": 0, "home_runs": 0, "rbis": 3, "stolen_bases": 2, "walks": 2, "strikeouts": 8, "batting_average": 0.188},
    {"season": 1994, "team_id": "orix", "games": 130, "at_bats": 546, "runs": 111, "hits": 210, "doubles": 41, "triples": 5, "home_runs": 13, "rbis": 54, "stolen_bases": 29, "walks": 51, "strikeouts": 53, "batting_average": 0.385, "on_base_percentage": 0.445, "slugging_percentage": 0.549},
    {"season": 1995, "team_id": "orix", "games": 130, "at_bats": 524, "runs": 104, "hits": 179, "doubles": 23, "triples": 4, "home_runs": 25, "rbis": 80, "stolen_bases": 49, "walks": 68, "strikeouts": 52, "batting_average": 0.342, "on_base_percentage": 0.432, "slugging_percentage": 0.544},
    {"season": 1996, "team_id": "orix", "games": 130, "at_bats": 542, "runs": 104, "hits": 193, "doubles": 24, "triples": 4, "home_runs": 16, "rbis": 84, "stolen_bases": 35, "walks": 62, "strikeouts": 43, "batting_average": 0.356, "on_base_percentage": 0.422, "slugging_percentage": 0.467},
    {"season": 1997, "team_id": "orix", "games": 135, "at_bats": 536, "runs": 94, "hits": 185, "doubles": 31, "triples": 2, "home_runs": 17, "rbis": 91, "stolen_bases": 39, "walks": 62, "strikeouts": 36, "batting_average": 0.345, "on_base_percentage": 0.414, "slugging_percentage": 0.502},
    {"season": 1998, "team_id": "orix", "games": 135, "at_bats": 506, "runs": 79, "hits": 181, "doubles": 36, "triples": 3, "home_runs": 13, "rbis": 71, "stolen_bases": 11, "walks": 43, "strikeouts": 43, "batting_average": 0.358, "on_base_percentage": 0.414, "slugging_percentage": 0.522},
    {"season": 1999, "team_id": "orix", "games": 103, "at_bats": 411, "runs": 80, "hits": 141, "doubles": 27, "triples": 2, "home_runs": 21, "rbis": 68, "stolen_bases": 12, "walks": 45, "strikeouts": 43, "batting_average": 0.343, "on_base_percentage": 0.412, "slugging_percentage": 0.572},
    {"season": 2000, "team_id": "orix", "games": 105, "at_bats": 395, "runs": 73, "hits": 153, "doubles": 22, "triples": 1, "home_runs": 12, "rbis": 73, "stolen_bases": 21, "walks": 54, "strikeouts": 30, "batting_average": 0.387, "on_base_percentage": 0.460, "slugging_percentage": 0.539}
]

# Sadaharu Oh's NPB batting statistics (selected seasons for testing)
# Full career: 1959-1980, 868 home runs (world record)
OH_BATTING_STATS = [
    {"season": 1959, "team_id": "giants", "games": 94, "at_bats": 229, "runs": 30, "hits": 37, "doubles": 2, "triples": 2, "home_runs": 7, "rbis": 27, "walks": 33, "strikeouts": 62, "batting_average": 0.161},
    {"season": 1960, "team_id": "giants", "games": 130, "at_bats": 427, "runs": 71, "hits": 113, "doubles": 12, "triples": 4, "home_runs": 17, "rbis": 71, "walks": 79, "strikeouts": 82, "batting_average": 0.265},
    {"season": 1962, "team_id": "giants", "games": 134, "at_bats": 472, "runs": 88, "hits": 147, "doubles": 17, "triples": 3, "home_runs": 38, "rbis": 85, "walks": 84, "strikeouts": 77, "batting_average": 0.311},
    {"season": 1963, "team_id": "giants", "games": 140, "at_bats": 481, "runs": 111, "hits": 153, "doubles": 14, "triples": 0, "home_runs": 40, "rbis": 106, "walks": 124, "strikeouts": 78, "batting_average": 0.318},
    {"season": 1964, "team_id": "giants", "games": 150, "at_bats": 520, "runs": 110, "hits": 161, "doubles": 18, "triples": 3, "home_runs": 55, "rbis": 119, "walks": 115, "strikeouts": 70, "batting_average": 0.310},
    {"season": 1966, "team_id": "giants", "games": 134, "at_bats": 442, "runs": 96, "hits": 148, "doubles": 15, "triples": 2, "home_runs": 48, "rbis": 108, "walks": 108, "strikeouts": 61, "batting_average": 0.335},
    {"season": 1973, "team_id": "giants", "games": 130, "at_bats": 434, "runs": 114, "hits": 140, "doubles": 16, "triples": 0, "home_runs": 51, "rbis": 114, "walks": 148, "strikeouts": 64, "batting_average": 0.323},
    {"season": 1974, "team_id": "giants", "games": 130, "at_bats": 385, "runs": 97, "hits": 128, "doubles": 15, "triples": 1, "home_runs": 49, "rbis": 107, "walks": 158, "strikeouts": 46, "batting_average": 0.332},
    {"season": 1977, "team_id": "giants", "games": 130, "at_bats": 453, "runs": 113, "hits": 149, "doubles": 16, "triples": 0, "home_runs": 50, "rbis": 124, "walks": 121, "strikeouts": 65, "batting_average": 0.329},
    {"season": 1980, "team_id": "giants", "games": 130, "at_bats": 416, "runs": 73, "hits": 103, "doubles": 10, "triples": 0, "home_runs": 30, "rbis": 84, "walks": 84, "strikeouts": 40, "batting_average": 0.248}
]

# Tetsuharu Kawakami's NPB batting statistics (selected seasons)
# Known as "God of Batting", first player to win batting title with .300+ average
KAWAKAMI_BATTING_STATS = [
    {"season": 1939, "team_id": "giants", "games": 96, "at_bats": 362, "runs": 46, "hits": 110, "doubles": 16, "triples": 5, "home_runs": 3, "rbis": 38, "batting_average": 0.304},
    {"season": 1940, "team_id": "giants", "games": 104, "at_bats": 402, "runs": 62, "hits": 138, "doubles": 18, "triples": 7, "home_runs": 9, "rbis": 59, "batting_average": 0.343},
    {"season": 1941, "team_id": "giants", "games": 86, "at_bats": 330, "runs": 56, "hits": 103, "doubles": 17, "triples": 4, "home_runs": 8, "rbis": 56, "batting_average": 0.312},
    {"season": 1951, "team_id": "giants", "games": 121, "at_bats": 420, "runs": 81, "hits": 156, "doubles": 31, "triples": 8, "home_runs": 8, "rbis": 85, "batting_average": 0.371},
    {"season": 1952, "team_id": "giants", "games": 119, "at_bats": 411, "runs": 70, "hits": 145, "doubles": 23, "triples": 4, "home_runs": 10, "rbis": 83, "batting_average": 0.353},
    {"season": 1953, "team_id": "giants", "games": 125, "at_bats": 457, "runs": 86, "hits": 158, "doubles": 29, "triples": 5, "home_runs": 18, "rbis": 92, "batting_average": 0.346},
    {"season": 1955, "team_id": "giants", "games": 138, "at_bats": 513, "runs": 89, "hits": 175, "doubles": 30, "triples": 3, "home_runs": 22, "rbis": 99, "batting_average": 0.341},
    {"season": 1956, "team_id": "giants", "games": 130, "at_bats": 482, "runs": 72, "hits": 162, "doubles": 29, "triples": 5, "home_runs": 16, "rbis": 87, "batting_average": 0.336},
    {"season": 1958, "team_id": "giants", "games": 125, "at_bats": 425, "runs": 58, "hits": 128, "doubles": 20, "triples": 1, "home_runs": 10, "rbis": 63, "batting_average": 0.301}
]

def populate_test_data(db):
    """Populate database with test data for our three legendary players."""
    # Insert players
    for player_key, player_data in HISTORICAL_PLAYERS.items():
        db.insert_player(player_data)
    
    # Insert batting statistics
    for stats in ICHIRO_BATTING_STATS:
        stats['player_id'] = 'suzuki-ichiro'
        stats['data_source'] = 'historical_import'
        stats['data_quality'] = 'complete'
        db.insert_batting_stats(stats)
    
    for stats in OH_BATTING_STATS:
        stats['player_id'] = 'oh-sadaharu'
        stats['data_source'] = 'historical_import'
        stats['data_quality'] = 'complete'
        db.insert_batting_stats(stats)
    
    for stats in KAWAKAMI_BATTING_STATS:
        stats['player_id'] = 'kawakami-tetsuharu'
        stats['data_source'] = 'historical_import'
        stats['data_quality'] = 'complete'
        db.insert_batting_stats(stats)
    
    # Insert NPB teams
    teams = [
        {"team_id": "giants", "name_english": "Yomiuri Giants", "name_japanese": "読売ジャイアンツ", 
         "abbreviation": "YG", "league": "Central", "city": "Tokyo"},
        {"team_id": "orix", "name_english": "Orix BlueWave/Buffaloes", "name_japanese": "オリックス", 
         "abbreviation": "ORX", "league": "Pacific", "city": "Kobe/Osaka"}
    ]
    
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