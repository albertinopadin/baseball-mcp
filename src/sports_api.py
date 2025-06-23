"""Sports endpoint utilities for MLB Stats API"""
from typing import Any
import httpx
from sports_constants import SPORT_INFO
from mlb_stats_api import BASE_URL, make_mlb_stats_request

async def get_available_sports() -> str:
    """Get list of all available sports/leagues in the MLB Stats API.
    
    Returns information about all available sports including MLB, Minor Leagues,
    International leagues, and other baseball organizations.
    """
    url = f"{BASE_URL}/sports"
    data = await make_mlb_stats_request(url)
    
    if not data or "sports" not in data:
        # Fall back to our known sports list
        result = ["Available Sports/Leagues:"]
        result.append("=" * 50)
        
        # Group sports by category
        mlb_sports = []
        minor_leagues = []
        international = []
        other = []
        
        for sport_id, info in sorted(SPORT_INFO.items()):
            sport_line = f"ID {sport_id}: {info['name']} ({info['abbreviation']})"
            
            if sport_id == 1:
                mlb_sports.append(sport_line)
            elif sport_id in [11, 12, 13, 14, 15, 16, 21]:
                minor_leagues.append(sport_line)
            elif sport_id in [31, 32, 51, 509, 510, 6005]:
                international.append(sport_line)
            else:
                other.append(sport_line)
        
        result.append("\nMajor League Baseball:")
        result.extend([f"  - {s}" for s in mlb_sports])
        
        result.append("\nMinor Leagues:")
        result.extend([f"  - {s}" for s in minor_leagues])
        
        result.append("\nInternational:")
        result.extend([f"  - {s}" for s in international])
        
        result.append("\nOther Leagues:")
        result.extend([f"  - {s}" for s in other])
        
        result.append("\nNote: Use these sport IDs with player stats, team search, and schedule functions to get data for specific leagues.")
        
        return "\n".join(result)
    
    # Format API response
    result = ["Available Sports/Leagues:"]
    result.append("=" * 50)
    
    # Group sports by category
    sports_by_category = {
        "Major League": [],
        "Minor Leagues": [],
        "International": [],
        "Other": []
    }
    
    for sport in data["sports"]:
        sport_id = sport.get("id")
        name = sport.get("name", "Unknown")
        code = sport.get("code", "N/A")
        abbreviation = sport.get("abbreviation", code.upper())
        
        sport_line = f"ID {sport_id}: {name} ({abbreviation})"
        
        # Categorize
        if sport_id == 1:
            sports_by_category["Major League"].append(sport_line)
        elif "Minor" in name or "Triple" in name or "Double" in name or "Single" in name or "Rookie" in name or "High-A" in name:
            sports_by_category["Minor Leagues"].append(sport_line)
        elif "International" in name or "Nippon" in name or "Korean" in name:
            sports_by_category["International"].append(sport_line)
        else:
            sports_by_category["Other"].append(sport_line)
    
    for category, sports in sports_by_category.items():
        if sports:
            result.append(f"\n{category}:")
            result.extend([f"  - {s}" for s in sorted(sports)])
    
    result.append("\nNote: Use these sport IDs with player stats, team search, and schedule functions to get data for specific leagues.")
    
    return "\n".join(result)