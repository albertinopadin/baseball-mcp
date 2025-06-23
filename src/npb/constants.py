"""NPB constants and configurations."""

from enum import Enum
from typing import Optional, Dict, List


class NPBLeague(Enum):
    """NPB League enumeration."""
    CENTRAL = "central"
    PACIFIC = "pacific"


# NPB Teams with their various identifiers and names
NPB_TEAMS = {
    # Central League
    "giants": {
        "id": "giants",
        "name_english": "Yomiuri Giants",
        "name_japanese": "読売ジャイアンツ",
        "league": NPBLeague.CENTRAL,
        "city": "Tokyo",
        "abbreviation": "YG",
        "br_id": "yomiuri-giants"  # Baseball-Reference ID
    },
    "tigers": {
        "id": "tigers",
        "name_english": "Hanshin Tigers",
        "name_japanese": "阪神タイガース",
        "league": NPBLeague.CENTRAL,
        "city": "Nishinomiya",
        "abbreviation": "HT",
        "br_id": "hanshin-tigers"
    },
    "dragons": {
        "id": "dragons",
        "name_english": "Chunichi Dragons",
        "name_japanese": "中日ドラゴンズ",
        "league": NPBLeague.CENTRAL,
        "city": "Nagoya",
        "abbreviation": "CD",
        "br_id": "chunichi-dragons"
    },
    "baystars": {
        "id": "baystars",
        "name_english": "Yokohama DeNA BayStars",
        "name_japanese": "横浜DeNAベイスターズ",
        "league": NPBLeague.CENTRAL,
        "city": "Yokohama",
        "abbreviation": "DB",
        "br_id": "yokohama-baystars"
    },
    "carp": {
        "id": "carp",
        "name_english": "Hiroshima Toyo Carp",
        "name_japanese": "広島東洋カープ",
        "league": NPBLeague.CENTRAL,
        "city": "Hiroshima",
        "abbreviation": "HC",
        "br_id": "hiroshima-carp"
    },
    "swallows": {
        "id": "swallows",
        "name_english": "Tokyo Yakult Swallows",
        "name_japanese": "東京ヤクルトスワローズ",
        "league": NPBLeague.CENTRAL,
        "city": "Tokyo",
        "abbreviation": "YS",
        "br_id": "yakult-swallows"
    },
    
    # Pacific League
    "hawks": {
        "id": "hawks",
        "name_english": "Fukuoka SoftBank Hawks",
        "name_japanese": "福岡ソフトバンクホークス",
        "league": NPBLeague.PACIFIC,
        "city": "Fukuoka",
        "abbreviation": "SH",
        "br_id": "softbank-hawks"
    },
    "fighters": {
        "id": "fighters",
        "name_english": "Hokkaido Nippon-Ham Fighters",
        "name_japanese": "北海道日本ハムファイターズ",
        "league": NPBLeague.PACIFIC,
        "city": "Sapporo",
        "abbreviation": "NF",
        "br_id": "nippon-ham-fighters"
    },
    "marines": {
        "id": "marines",
        "name_english": "Chiba Lotte Marines",
        "name_japanese": "千葉ロッテマリーンズ",
        "league": NPBLeague.PACIFIC,
        "city": "Chiba",
        "abbreviation": "LM",
        "br_id": "lotte-marines"
    },
    "lions": {
        "id": "lions",
        "name_english": "Saitama Seibu Lions",
        "name_japanese": "埼玉西武ライオンズ",
        "league": NPBLeague.PACIFIC,
        "city": "Tokorozawa",
        "abbreviation": "SL",
        "br_id": "seibu-lions"
    },
    "eagles": {
        "id": "eagles",
        "name_english": "Tohoku Rakuten Golden Eagles",
        "name_japanese": "東北楽天ゴールデンイーグルス",
        "league": NPBLeague.PACIFIC,
        "city": "Sendai",
        "abbreviation": "RE",
        "br_id": "rakuten-eagles"
    },
    "buffaloes": {
        "id": "buffaloes",
        "name_english": "Orix Buffaloes",
        "name_japanese": "オリックス・バファローズ",
        "league": NPBLeague.PACIFIC,
        "city": "Osaka",
        "abbreviation": "OB",
        "br_id": "orix-buffaloes"
    }
}

# Helper functions for team lookups
def get_team_by_name(name: str) -> Optional[Dict]:
    """Find team by partial name match (case-insensitive)."""
    name_lower = name.lower()
    for team_id, team_data in NPB_TEAMS.items():
        if (name_lower in team_data["name_english"].lower() or
            name_lower in team_data["city"].lower() or
            name_lower == team_data["abbreviation"].lower()):
            return {**team_data, "id": team_id}
    return None


def get_teams_by_league(league: NPBLeague) -> List[Dict]:
    """Get all teams in a specific league."""
    teams = []
    for team_id, team_data in NPB_TEAMS.items():
        if team_data["league"] == league:
            teams.append({**team_data, "id": team_id})
    return teams


# Baseball-Reference NPB base URL
BR_NPB_BASE_URL = "https://www.baseball-reference.com"

# Common position mappings
POSITION_MAPPINGS = {
    "P": "Pitcher",
    "C": "Catcher",
    "1B": "First Base",
    "2B": "Second Base",
    "3B": "Third Base",
    "SS": "Shortstop",
    "LF": "Left Field",
    "CF": "Center Field",
    "RF": "Right Field",
    "OF": "Outfield",
    "DH": "Designated Hitter",
    "IF": "Infield",
    "UT": "Utility"
}