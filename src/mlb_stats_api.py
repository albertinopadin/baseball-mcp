"""MLB Stats API client for accessing player, team, and game data."""
from typing import Any, Optional
import httpx
from data_utils import (
    format_player_data,
    format_team_data,
    format_roster_data,
    format_player_stats,
    format_schedule_data,
    format_game_data,
    format_standings_data,
    format_live_game_data
)

BASE_URL = "https://statsapi.mlb.com/api/v1"
USER_AGENT = "baseball-mcp-server/1.0"


async def make_mlb_stats_request(url: str) -> dict[str, Any] | None:
    """Make a request to the MLB Stats API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


async def search_player(search_str: str) -> str:
    """Search for MLB player.

    Args:
        search_str: Name of player to search for
    """
    url = f"{BASE_URL}/people/search?names={search_str}"
    data = await make_mlb_stats_request(url)

    if not data or "people" not in data:
        return f"Unable to search for {search_str} or no player found."

    if not data["people"]:
        return f"No player found for search string: {search_str}"

    player_results = [format_player_data(player) for player in data["people"]]
    return "\n---\n".join(player_results)


async def get_player(person_id: int, season: Optional[str] = None, accent: bool = True) -> str:
    """Get detailed information about a specific MLB player.
    
    Args:
        person_id: Unique Player Identifier (e.g., 434538, 429665)
        season: Season of play (optional)
        accent: Include accent marks in player names (default: True)
    """
    params = {"accent": accent}
    if season:
        params["season"] = season
        
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    url = f"{BASE_URL}/people/{person_id}?{query_string}"
    
    data = await make_mlb_stats_request(url)
    
    if not data or "people" not in data or not data["people"]:
        return f"Unable to find player with ID {person_id}."
    
    return format_player_data(data["people"][0])


async def get_player_stats(
    person_id: int,
    stats: str,
    season: Optional[str] = None,
    sport_id: int = 1,
    group: Optional[str] = None
) -> str:
    """Get statistics for a specific MLB player.
    
    Args:
        person_id: Unique Player Identifier
        stats: Type of statistics (e.g., 'season', 'career', 'yearByYear', 'gameLog')
        season: Season of play (optional)
        sport_id: Sport ID (default: 1 for MLB)
        group: Stat group (e.g., 'hitting', 'pitching', 'fielding')
    """
    params = {"stats": stats, "sportId": sport_id}
    if season:
        params["season"] = season
    if group:
        params["group"] = group
        
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    url = f"{BASE_URL}/people/{person_id}/stats?{query_string}"
    
    data = await make_mlb_stats_request(url)
    
    if not data or "stats" not in data:
        return f"Unable to retrieve stats for player ID {person_id}."
    
    return format_player_stats(data["stats"])


async def search_teams(
    season: Optional[str] = None,
    sport_id: int = 1,
    active_status: str = "Y",
    league_id: Optional[int] = None,
    division_id: Optional[int] = None
) -> str:
    """Search for MLB teams.
    
    Args:
        season: Season of play (optional)
        sport_id: Sport ID (default: 1 for MLB)
        active_status: 'Y' for active, 'N' for inactive, 'B' for both
        league_id: League ID (optional)
        division_id: Division ID (optional)
    """
    params = {"sportId": sport_id, "activeStatus": active_status}
    if season:
        params["season"] = season
    if league_id:
        params["leagueId"] = league_id
    if division_id:
        params["divisionId"] = division_id
        
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    url = f"{BASE_URL}/teams?{query_string}"
    
    data = await make_mlb_stats_request(url)
    
    if not data or "teams" not in data:
        return "Unable to retrieve teams."
    
    team_results = [format_team_data(team) for team in data["teams"]]
    return "\n---\n".join(team_results)


async def get_team(team_id: int, season: Optional[str] = None) -> str:
    """Get detailed information about a specific MLB team.
    
    Args:
        team_id: Unique Team Identifier (e.g., 141, 147)
        season: Season of play (optional)
    """
    params = {}
    if season:
        params["season"] = season
        
    query_string = "&".join([f"{k}={v}" for k, v in params.items()]) if params else ""
    url = f"{BASE_URL}/teams/{team_id}"
    if query_string:
        url += f"?{query_string}"
    
    data = await make_mlb_stats_request(url)
    
    if not data or "teams" not in data or not data["teams"]:
        return f"Unable to find team with ID {team_id}."
    
    return format_team_data(data["teams"][0])


async def get_team_roster(
    team_id: int,
    roster_type: str = "active",
    season: Optional[str] = None,
    date: Optional[str] = None
) -> str:
    """Get roster for a specific MLB team.
    
    Args:
        team_id: Unique Team Identifier
        roster_type: Type of roster (e.g., 'active', '40Man', 'fullSeason')
        season: Season of play (optional)
        date: Specific date for roster (format: 'YYYY-MM-DD')
    """
    params = {}
    if season:
        params["season"] = season
    if date:
        params["date"] = date
        
    query_string = "&".join([f"{k}={v}" for k, v in params.items()]) if params else ""
    url = f"{BASE_URL}/teams/{team_id}/roster/{roster_type}"
    if query_string:
        url += f"?{query_string}"
    
    data = await make_mlb_stats_request(url)
    
    if not data or "roster" not in data:
        return f"Unable to retrieve roster for team ID {team_id}."
    
    return format_roster_data(data["roster"])


async def get_schedule(
    sport_id: int = 1,
    season: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    team_id: Optional[int] = None,
    game_type: Optional[str] = None
) -> str:
    """Get MLB game schedule.
    
    Args:
        sport_id: Sport ID (default: 1 for MLB)
        season: Season of play (optional)
        start_date: Start date (format: 'YYYY-MM-DD')
        end_date: End date (format: 'YYYY-MM-DD')
        team_id: Filter by specific team (optional)
        game_type: Type of games (e.g., 'R' for regular season, 'P' for postseason)
    """
    params = {"sportId": sport_id}
    if season:
        params["season"] = season
    if start_date:
        params["startDate"] = start_date
    if end_date:
        params["endDate"] = end_date
    if team_id:
        params["teamId"] = team_id
    if game_type:
        params["gameType"] = game_type
        
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    url = f"{BASE_URL}/schedule?{query_string}"
    
    data = await make_mlb_stats_request(url)
    
    if not data or "dates" not in data:
        return "Unable to retrieve schedule."
    
    return format_schedule_data(data["dates"])


async def get_game_info(game_pk: int) -> str:
    """Get detailed information about a specific game.
    
    Args:
        game_pk: Unique Primary Key representing a game
    """
    url = f"{BASE_URL}/game/{game_pk}/boxscore"
    data = await make_mlb_stats_request(url)
    
    if not data:
        return f"Unable to retrieve information for game {game_pk}."
    
    return format_game_data(data)


async def get_standings(
    league_id: int,
    season: Optional[str] = None,
    standings_type: str = "regularSeason",
    date: Optional[str] = None
) -> str:
    """Get league standings.
    
    Args:
        league_id: League ID (103 for AL, 104 for NL)
        season: Season of play (optional)
        standings_type: Type of standings (e.g., 'regularSeason', 'wildCard', 'divisionLeaders')
        date: Specific date for standings (format: 'YYYY-MM-DD')
    """
    params = {"leagueId": league_id}
    if season:
        params["season"] = season
    if date:
        params["date"] = date
        
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    url = f"{BASE_URL}/standings/{standings_type}?{query_string}"
    
    data = await make_mlb_stats_request(url)
    
    if not data or "records" not in data:
        return f"Unable to retrieve standings for league {league_id}."
    
    return format_standings_data(data["records"])


async def get_live_game_feed(game_pk: int) -> str:
    """Get live feed data for an ongoing game.
    
    Args:
        game_pk: Unique Primary Key representing a game
    """
    url = f"{BASE_URL}/game/{game_pk}/feed/live"
    data = await make_mlb_stats_request(url)
    
    if not data:
        return f"Unable to retrieve live feed for game {game_pk}."
    
    return format_live_game_data(data)