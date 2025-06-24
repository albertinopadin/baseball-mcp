"""
NPB Historical Dataset - Sample data for major NPB players
This includes career statistics for notable players from different eras
"""

# Historical NPB Players Dataset
NPB_HISTORICAL_PLAYERS = [
    # 1950s-1960s Era
    {
        "player_id": "nagashima-shigeo",
        "name_english": "Shigeo Nagashima",
        "name_japanese": "長嶋茂雄",
        "name_romanized_variants": ["Nagashima Shigeo", "Shigeo Nagashima"],
        "birth_date": "1936-02-20",
        "height": "178cm",
        "weight": "76kg",
        "bats": "Right",
        "throws": "Right",
        "debut_date": "1958-04-05",
        "final_game": "1974-10-14",
        "teams": ["giants"],
        "career_stats": {
            "batting": {
                "games": 2186,
                "at_bats": 8094,
                "runs": 1270,
                "hits": 2471,
                "doubles": 348,
                "triples": 63,
                "home_runs": 444,
                "rbis": 1522,
                "stolen_bases": 117,
                "walks": 881,
                "strikeouts": 1052,
                "batting_average": 0.305,
                "on_base_percentage": 0.380,
                "slugging_percentage": 0.540
            }
        }
    },
    {
        "player_id": "kaneda-masaichi",
        "name_english": "Masaichi Kaneda",
        "name_japanese": "金田正一",
        "name_romanized_variants": ["Kaneda Masaichi", "Masaichi Kaneda"],
        "birth_date": "1933-08-01",
        "height": "184cm",
        "weight": "73kg",
        "bats": "Left",
        "throws": "Left",
        "debut_date": "1950-08-23",
        "final_game": "1969-10-10",
        "teams": ["swallows", "giants"],
        "career_stats": {
            "pitching": {
                "wins": 400,
                "losses": 298,
                "era": 2.34,
                "games": 944,
                "games_started": 685,
                "complete_games": 365,
                "shutouts": 82,
                "saves": 2,
                "innings_pitched": 5526.2,
                "hits_allowed": 4440,
                "runs_allowed": 1666,
                "earned_runs": 1435,
                "home_runs_allowed": 197,
                "walks": 1808,
                "strikeouts": 4490,
                "whip": 1.133
            }
        }
    },
    
    # 1970s-1980s Era
    {
        "player_id": "yamamoto-koji",
        "name_english": "Koji Yamamoto",
        "name_japanese": "山本浩二",
        "name_romanized_variants": ["Yamamoto Koji", "Koji Yamamoto"],
        "birth_date": "1946-10-25",
        "height": "178cm",
        "weight": "80kg",
        "bats": "Right",
        "throws": "Right",
        "debut_date": "1969-04-12",
        "final_game": "1986-10-26",
        "teams": ["carp"],
        "career_stats": {
            "batting": {
                "games": 2284,
                "at_bats": 8052,
                "runs": 1281,
                "hits": 2339,
                "doubles": 356,
                "triples": 65,
                "home_runs": 536,
                "rbis": 1475,
                "stolen_bases": 231,
                "walks": 1040,
                "strikeouts": 1312,
                "batting_average": 0.290,
                "on_base_percentage": 0.380,
                "slugging_percentage": 0.545
            }
        }
    },
    {
        "player_id": "ochiai-hiromitsu",
        "name_english": "Hiromitsu Ochiai",
        "name_japanese": "落合博満",
        "name_romanized_variants": ["Ochiai Hiromitsu", "Hiromitsu Ochiai"],
        "birth_date": "1953-12-09",
        "height": "178cm",
        "weight": "82kg",
        "bats": "Right",
        "throws": "Right",
        "debut_date": "1979-04-07",
        "final_game": "1998-10-26",
        "teams": ["dragons", "giants", "buffaloes", "swallows"],
        "career_stats": {
            "batting": {
                "games": 2236,
                "at_bats": 7627,
                "runs": 1034,
                "hits": 2371,
                "doubles": 389,
                "triples": 28,
                "home_runs": 510,
                "rbis": 1564,
                "stolen_bases": 65,
                "walks": 1108,
                "strikeouts": 1004,
                "batting_average": 0.311,
                "on_base_percentage": 0.397,
                "slugging_percentage": 0.564
            }
        }
    },
    
    # 1990s-2000s Era  
    {
        "player_id": "matsui-hideki",
        "name_english": "Hideki Matsui",
        "name_japanese": "松井秀喜",
        "name_romanized_variants": ["Matsui Hideki", "Hideki Matsui"],
        "birth_date": "1974-06-12",
        "height": "188cm",
        "weight": "95kg",
        "bats": "Left",
        "throws": "Right",
        "debut_date": "1993-05-02",
        "final_game": "2002-10-26",
        "teams": ["giants"],
        "career_stats": {
            "batting": {
                "games": 1268,
                "at_bats": 4572,
                "runs": 713,
                "hits": 1390,
                "doubles": 251,
                "triples": 25,
                "home_runs": 332,
                "rbis": 889,
                "stolen_bases": 13,
                "walks": 688,
                "strikeouts": 766,
                "batting_average": 0.304,
                "on_base_percentage": 0.413,
                "slugging_percentage": 0.582
            }
        }
    },
    {
        "player_id": "furuta-atsuya",
        "name_english": "Atsuya Furuta",
        "name_japanese": "古田敦也",
        "name_romanized_variants": ["Furuta Atsuya", "Atsuya Furuta"],
        "birth_date": "1965-08-06",
        "height": "182cm",
        "weight": "80kg",
        "bats": "Right",
        "throws": "Right",
        "debut_date": "1991-04-10",
        "final_game": "2007-10-07",
        "teams": ["swallows"],
        "career_stats": {
            "batting": {
                "games": 2097,
                "at_bats": 6725,
                "runs": 781,
                "hits": 2097,
                "doubles": 373,
                "triples": 23,
                "home_runs": 217,
                "rbis": 1006,
                "stolen_bases": 43,
                "walks": 901,
                "strikeouts": 696,
                "batting_average": 0.294,
                "on_base_percentage": 0.380,
                "slugging_percentage": 0.450
            }
        }
    },
    {
        "player_id": "shinjo-tsuyoshi",
        "name_english": "Tsuyoshi Shinjo",
        "name_japanese": "新庄剛志",
        "name_romanized_variants": ["Shinjo Tsuyoshi", "Tsuyoshi Shinjo"],
        "birth_date": "1972-01-28",
        "height": "181cm",
        "weight": "75kg",
        "bats": "Right",
        "throws": "Right",
        "debut_date": "1992-05-23",
        "final_game": "2006-10-26",
        "teams": ["tigers", "fighters"],
        "career_stats": {
            "batting": {
                "games": 796,
                "at_bats": 2827,
                "runs": 403,
                "hits": 774,
                "doubles": 144,
                "triples": 17,
                "home_runs": 146,
                "rbis": 417,
                "stolen_bases": 82,
                "walks": 256,
                "strikeouts": 585,
                "batting_average": 0.274,
                "on_base_percentage": 0.338,
                "slugging_percentage": 0.490
            }
        }
    },
    
    # Foreign Players
    {
        "player_id": "bass-randy",
        "name_english": "Randy Bass",
        "name_japanese": "ランディ・バース",
        "name_romanized_variants": ["Randy Bass", "Bass Randy"],
        "birth_date": "1954-03-13",
        "height": "183cm",
        "weight": "95kg",
        "bats": "Left",
        "throws": "Right",
        "debut_date": "1983-04-09",
        "final_game": "1988-06-02",
        "teams": ["tigers"],
        "career_stats": {
            "batting": {
                "games": 616,
                "at_bats": 2181,
                "runs": 393,
                "hits": 744,
                "doubles": 120,
                "triples": 5,
                "home_runs": 202,
                "rbis": 487,
                "stolen_bases": 35,
                "walks": 347,
                "strikeouts": 325,
                "batting_average": 0.337,
                "on_base_percentage": 0.425,
                "slugging_percentage": 0.632
            }
        }
    },
    {
        "player_id": "cromartie-warren",
        "name_english": "Warren Cromartie",
        "name_japanese": "ウォーレン・クロマティ",
        "name_romanized_variants": ["Warren Cromartie", "Cromartie Warren"],
        "birth_date": "1953-09-29",
        "height": "183cm",
        "weight": "88kg",
        "bats": "Left",
        "throws": "Left",
        "debut_date": "1984-04-07",
        "final_game": "1990-10-10",
        "teams": ["giants"],
        "career_stats": {
            "batting": {
                "games": 868,
                "at_bats": 3258,
                "runs": 428,
                "hits": 1089,
                "doubles": 187,
                "triples": 17,
                "home_runs": 171,
                "rbis": 558,
                "stolen_bases": 42,
                "walks": 268,
                "strikeouts": 442,
                "batting_average": 0.321,
                "on_base_percentage": 0.380,
                "slugging_percentage": 0.530
            }
        }
    },
    {
        "player_id": "cabrera-alex",
        "name_english": "Alex Cabrera",
        "name_japanese": "アレックス・カブレラ",
        "name_romanized_variants": ["Alex Cabrera", "Cabrera Alex"],
        "birth_date": "1971-12-24",
        "height": "188cm",
        "weight": "102kg",
        "bats": "Right",
        "throws": "Right",
        "debut_date": "2001-04-03",
        "final_game": "2012-10-08",
        "teams": ["lions", "buffaloes", "softbank"],
        "career_stats": {
            "batting": {
                "games": 1132,
                "at_bats": 4065,
                "runs": 624,
                "hits": 1178,
                "doubles": 213,
                "triples": 8,
                "home_runs": 357,
                "rbis": 962,
                "stolen_bases": 9,
                "walks": 481,
                "strikeouts": 865,
                "batting_average": 0.290,
                "on_base_percentage": 0.367,
                "slugging_percentage": 0.596
            }
        }
    }
]

# Season-by-season data for selected players
NPB_SEASONAL_STATS = {
    "nagashima-shigeo": [
        {"season": 1958, "team_id": "giants", "games": 130, "at_bats": 482, "runs": 69, "hits": 153, "doubles": 25, "triples": 3, "home_runs": 29, "rbis": 92, "batting_average": 0.305},
        {"season": 1959, "team_id": "giants", "games": 134, "at_bats": 515, "runs": 82, "hits": 161, "doubles": 21, "triples": 3, "home_runs": 27, "rbis": 82, "batting_average": 0.334},
        {"season": 1960, "team_id": "giants", "games": 130, "at_bats": 487, "runs": 79, "hits": 155, "doubles": 21, "triples": 3, "home_runs": 28, "rbis": 86, "batting_average": 0.334},
        {"season": 1961, "team_id": "giants", "games": 130, "at_bats": 495, "runs": 98, "hits": 170, "doubles": 29, "triples": 6, "home_runs": 28, "rbis": 76, "batting_average": 0.353},
        {"season": 1963, "team_id": "giants", "games": 150, "at_bats": 580, "runs": 114, "hits": 199, "doubles": 23, "triples": 4, "home_runs": 37, "rbis": 112, "batting_average": 0.341},
        {"season": 1966, "team_id": "giants", "games": 134, "at_bats": 500, "runs": 77, "hits": 172, "doubles": 18, "triples": 4, "home_runs": 26, "rbis": 89, "batting_average": 0.344},
        {"season": 1968, "team_id": "giants", "games": 131, "at_bats": 485, "runs": 76, "hits": 161, "doubles": 26, "triples": 6, "home_runs": 39, "rbis": 125, "batting_average": 0.326},
        {"season": 1971, "team_id": "giants", "games": 130, "at_bats": 463, "runs": 66, "hits": 156, "doubles": 18, "triples": 0, "home_runs": 28, "rbis": 104, "batting_average": 0.337},
        {"season": 1974, "team_id": "giants", "games": 125, "at_bats": 405, "runs": 40, "hits": 96, "doubles": 12, "triples": 0, "home_runs": 16, "rbis": 50, "batting_average": 0.244}
    ],
    "matsui-hideki": [
        {"season": 1993, "team_id": "giants", "games": 21, "at_bats": 64, "runs": 7, "hits": 11, "doubles": 3, "triples": 0, "home_runs": 1, "rbis": 11, "batting_average": 0.172},
        {"season": 1994, "team_id": "giants", "games": 130, "at_bats": 456, "runs": 66, "hits": 130, "doubles": 28, "triples": 1, "home_runs": 20, "rbis": 66, "batting_average": 0.294},
        {"season": 1995, "team_id": "giants", "games": 132, "at_bats": 493, "runs": 64, "hits": 141, "doubles": 28, "triples": 1, "home_runs": 22, "rbis": 80, "batting_average": 0.289},
        {"season": 1996, "team_id": "giants", "games": 130, "at_bats": 486, "runs": 71, "hits": 153, "doubles": 25, "triples": 1, "home_runs": 38, "rbis": 99, "batting_average": 0.314},
        {"season": 1997, "team_id": "giants", "games": 135, "at_bats": 487, "runs": 83, "hits": 156, "doubles": 31, "triples": 3, "home_runs": 37, "rbis": 103, "batting_average": 0.298},
        {"season": 1998, "team_id": "giants", "games": 135, "at_bats": 487, "runs": 79, "hits": 142, "doubles": 27, "triples": 5, "home_runs": 34, "rbis": 100, "batting_average": 0.292},
        {"season": 1999, "team_id": "giants", "games": 135, "at_bats": 471, "runs": 94, "hits": 179, "doubles": 34, "triples": 6, "home_runs": 42, "rbis": 95, "batting_average": 0.304},
        {"season": 2000, "team_id": "giants", "games": 135, "at_bats": 494, "runs": 107, "hits": 182, "doubles": 37, "triples": 3, "home_runs": 42, "rbis": 108, "batting_average": 0.316},
        {"season": 2001, "team_id": "giants", "games": 140, "at_bats": 500, "runs": 82, "hits": 167, "doubles": 26, "triples": 1, "home_runs": 36, "rbis": 104, "batting_average": 0.333},
        {"season": 2002, "team_id": "giants", "games": 140, "at_bats": 500, "runs": 106, "hits": 171, "doubles": 24, "triples": 4, "home_runs": 50, "rbis": 107, "batting_average": 0.334}
    ],
    "bass-randy": [
        {"season": 1983, "team_id": "tigers", "games": 127, "at_bats": 478, "runs": 62, "hits": 150, "doubles": 29, "triples": 2, "home_runs": 35, "rbis": 83, "batting_average": 0.326},
        {"season": 1984, "team_id": "tigers", "games": 126, "at_bats": 436, "runs": 72, "hits": 143, "doubles": 18, "triples": 1, "home_runs": 37, "rbis": 91, "batting_average": 0.326},
        {"season": 1985, "team_id": "tigers", "games": 125, "at_bats": 452, "runs": 103, "hits": 169, "doubles": 24, "triples": 0, "home_runs": 54, "rbis": 134, "batting_average": 0.350},
        {"season": 1986, "team_id": "tigers", "games": 126, "at_bats": 437, "runs": 92, "hits": 176, "doubles": 26, "triples": 2, "home_runs": 47, "rbis": 109, "batting_average": 0.389},
        {"season": 1987, "team_id": "tigers", "games": 106, "at_bats": 378, "runs": 64, "hits": 113, "doubles": 21, "triples": 0, "home_runs": 29, "rbis": 70, "batting_average": 0.320}
    ]
}