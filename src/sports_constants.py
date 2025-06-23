"""Sport ID constants for MLB Stats API"""

# Major League
MLB = 1

# Minor Leagues
TRIPLE_A = 11
DOUBLE_A = 12
HIGH_A = 13
SINGLE_A = 14
SHORT_SEASON_A = 15
ROOKIE = 16
MINOR_LEAGUE_GENERAL = 21

# Other Leagues
WINTER_LEAGUES = 17
INDEPENDENT_LEAGUES = 23
NEGRO_LEAGUE = 61
KOREAN_BASEBALL = 32
NIPPON_PROFESSIONAL = 31
INTERNATIONAL = 51
INTERNATIONAL_18U = 509
INTERNATIONAL_16U = 510
INTERNATIONAL_AMATEUR = 6005
COLLEGE = 22
HIGH_SCHOOL = 586
WOMENS_SOFTBALL = 576

# Sport info mapping
SPORT_INFO = {
    MLB: {"name": "Major League Baseball", "code": "mlb", "abbreviation": "MLB"},
    TRIPLE_A: {"name": "Triple-A", "code": "aaa", "abbreviation": "AAA"},
    DOUBLE_A: {"name": "Double-A", "code": "aax", "abbreviation": "AA"},
    HIGH_A: {"name": "High-A", "code": "afa", "abbreviation": "A+"},
    SINGLE_A: {"name": "Single-A", "code": "afx", "abbreviation": "A"},
    SHORT_SEASON_A: {"name": "Class A Short Season", "code": "asx", "abbreviation": "A-"},
    ROOKIE: {"name": "Rookie", "code": "rok", "abbreviation": "R"},
    MINOR_LEAGUE_GENERAL: {"name": "Minor League Baseball", "code": "min", "abbreviation": "MiLB"},
    WINTER_LEAGUES: {"name": "Winter Leagues", "code": "win", "abbreviation": "WIN"},
    INDEPENDENT_LEAGUES: {"name": "Independent Leagues", "code": "ind", "abbreviation": "IND"},
    NEGRO_LEAGUE: {"name": "Negro League Baseball", "code": "nlb", "abbreviation": "NLB"},
    KOREAN_BASEBALL: {"name": "Korean Baseball Organization", "code": "kor", "abbreviation": "KBO"},
    NIPPON_PROFESSIONAL: {"name": "Nippon Professional Baseball", "code": "jml", "abbreviation": "NPB"},
    INTERNATIONAL: {"name": "International Baseball", "code": "int", "abbreviation": "INT"},
    COLLEGE: {"name": "College Baseball", "code": "bbc", "abbreviation": "COL"},
    HIGH_SCHOOL: {"name": "High School Baseball", "code": "hsb", "abbreviation": "HS"},
    WOMENS_SOFTBALL: {"name": "Women's Professional Softball", "code": "wps", "abbreviation": "WPS"}
}

# Minor league sport IDs for easy reference
MINOR_LEAGUE_IDS = [TRIPLE_A, DOUBLE_A, HIGH_A, SINGLE_A, SHORT_SEASON_A, ROOKIE]

def get_sport_name(sport_id: int) -> str:
    """Get the name of a sport by its ID"""
    return SPORT_INFO.get(sport_id, {}).get("name", f"Unknown Sport (ID: {sport_id})")

def get_sport_abbreviation(sport_id: int) -> str:
    """Get the abbreviation of a sport by its ID"""
    return SPORT_INFO.get(sport_id, {}).get("abbreviation", "UNK")

def is_minor_league(sport_id: int) -> bool:
    """Check if a sport ID represents a minor league"""
    return sport_id in MINOR_LEAGUE_IDS