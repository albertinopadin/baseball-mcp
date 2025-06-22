from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from datetime import datetime, timedelta
import asyncio
from data_utils import (
    format_player_data,
    format_team_data,
    format_roster_data,
    format_player_stats,
    format_schedule_data,
    format_game_data,
    format_standings_data,
    format_live_game_data,
    format_statcast_batting_data,
    format_statcast_pitching_data
)
from cache_utils import cache_result

# Import pybaseball for Statcast data
try:
    from pybaseball import statcast_batter, statcast_pitcher, playerid_lookup
    import pandas as pd
    PYBASEBALL_AVAILABLE = True
except ImportError:
    PYBASEBALL_AVAILABLE = False

try:
    from importlib.metadata import version
    VERSION = version("baseball-mcp")
except Exception:
    VERSION = "0.0.3"  # Fallback version
    
BASE_URL = "https://statsapi.mlb.com/api/v1"
USER_AGENT = "baseball-mcp-server/1.0"

mcp = FastMCP("BaseballMcp")

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
        

@mcp.tool()
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


@mcp.tool()
async def get_player(person_id: int, season: str | None = None, accent: bool = True) -> str:
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


@mcp.tool()
async def get_player_stats(
    person_id: int,
    stats: str,
    season: str | None = None,
    sport_id: int = 1,
    group: str | None = None
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


@mcp.tool()
async def search_teams(
    season: str | None = None,
    sport_id: int = 1,
    active_status: str = "Y",
    league_id: int | None = None,
    division_id: int | None = None
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


@mcp.tool()
async def get_team(team_id: int, season: str | None = None) -> str:
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


@mcp.tool()
async def get_team_roster(
    team_id: int,
    roster_type: str = "active",
    season: str | None = None,
    date: str | None = None
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


@mcp.tool()
async def get_schedule(
    sport_id: int = 1,
    season: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    team_id: int | None = None,
    game_type: str | None = None
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


@mcp.tool()
async def get_game_info(game_pk: int) -> str:
    """Get detailed information about a specific game.
    
    Args:
        game_pk: Unique Primary Key representing a game
    """
    url = f"{BASE_URL}/game/{game_pk}/boxscore"
    
    data = await make_mlb_stats_request(url)
    
    if not data:
        return f"Unable to retrieve game information for game {game_pk}."
    
    return format_game_data(data)


@mcp.tool()
async def get_standings(
    league_id: int,
    season: str | None = None,
    standings_type: str = "regularSeason",
    date: str | None = None
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
        return "Unable to retrieve standings."
    
    return format_standings_data(data["records"])


@mcp.tool()
async def get_live_game_feed(game_pk: int) -> str:
    """Get live feed data for an ongoing game.
    
    Args:
        game_pk: Unique Primary Key representing a game
    """
    url = f"{BASE_URL}.1/game/{game_pk}/feed/live"
    
    data = await make_mlb_stats_request(url)
    
    if not data:
        return f"Unable to retrieve live feed for game {game_pk}."
    
    return format_live_game_data(data)


@mcp.tool()
async def get_player_statcast_batting(
    player_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    season: str | None = None
) -> str:
    """Get Statcast batting metrics for a player including exit velocity, launch angle, and barrel rate.
    
    Args:
        player_name: Full name of the player (e.g., "Aaron Judge")
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
        season: Season year (e.g., "2024"). If not provided with dates, defaults to current season
    """
    if not PYBASEBALL_AVAILABLE:
        return "Statcast data is not available. The pybaseball library is not installed."
    
    # Set default dates if not provided
    if not start_date and not end_date:
        if season:
            start_date = f"{season}-03-20"
            end_date = f"{season}-10-05"
        else:
            # Default to current season
            current_year = datetime.now().year
            start_date = f"{current_year}-03-20"
            end_date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # Parse the player name
        names = player_name.strip().split()
        if len(names) < 2:
            return f"Please provide a full name (first and last name) for {player_name}"
        
        first_name = names[0]
        last_name = " ".join(names[1:])  # Handle names with multiple parts
        
        # Look up player ID using pybaseball
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        player_lookup = await loop.run_in_executor(
            None, 
            playerid_lookup, 
            last_name, 
            first_name
        )
        
        if player_lookup.empty:
            return f"No player found matching '{player_name}'"
        
        # Get the first match (most relevant)
        player_id = int(player_lookup.iloc[0]['key_mlbam'])
        
        # Cache the statcast data retrieval
        @cache_result(ttl_hours=24)
        def get_cached_statcast_batter(player_id: int, start: str, end: str):
            return statcast_batter(start, end, player_id)
        
        # Get Statcast data
        statcast_data = await loop.run_in_executor(
            None,
            get_cached_statcast_batter,
            player_id,
            start_date,
            end_date
        )
        
        if statcast_data is None or statcast_data.empty:
            return f"No Statcast batting data available for {player_name} from {start_date} to {end_date}"
        
        # Format the data
        return format_statcast_batting_data(statcast_data)
        
    except Exception as e:
        return f"Error retrieving Statcast data for {player_name}: {str(e)}"


@mcp.tool()
async def get_player_statcast_pitching(
    player_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    season: str | None = None
) -> str:
    """Get Statcast pitching metrics for a player including spin rate, velocity, and pitch movement.
    
    Args:
        player_name: Full name of the player (e.g., "Gerrit Cole")
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
        season: Season year (e.g., "2024"). If not provided with dates, defaults to current season
    """
    if not PYBASEBALL_AVAILABLE:
        return "Statcast data is not available. The pybaseball library is not installed."
    
    # Set default dates if not provided
    if not start_date and not end_date:
        if season:
            start_date = f"{season}-03-20"
            end_date = f"{season}-10-05"
        else:
            # Default to current season
            current_year = datetime.now().year
            start_date = f"{current_year}-03-20"
            end_date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # Parse the player name
        names = player_name.strip().split()
        if len(names) < 2:
            return f"Please provide a full name (first and last name) for {player_name}"
        
        first_name = names[0]
        last_name = " ".join(names[1:])  # Handle names with multiple parts
        
        # Look up player ID using pybaseball
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        player_lookup = await loop.run_in_executor(
            None, 
            playerid_lookup, 
            last_name, 
            first_name
        )
        
        if player_lookup.empty:
            return f"No player found matching '{player_name}'"
        
        # Get the first match (most relevant)
        player_id = int(player_lookup.iloc[0]['key_mlbam'])
        
        # Cache the statcast data retrieval
        @cache_result(ttl_hours=24)
        def get_cached_statcast_pitcher(player_id: int, start: str, end: str):
            return statcast_pitcher(start, end, player_id)
        
        # Get Statcast data
        statcast_data = await loop.run_in_executor(
            None,
            get_cached_statcast_pitcher,
            player_id,
            start_date,
            end_date
        )
        
        if statcast_data is None or statcast_data.empty:
            return f"No Statcast pitching data available for {player_name} from {start_date} to {end_date}"
        
        # Format the data
        return format_statcast_pitching_data(statcast_data)
        
    except Exception as e:
        return f"Error retrieving Statcast data for {player_name}: {str(e)}"


if __name__ == "__main__":
    print(f"Baseball Stats MCP Server v{VERSION}")
    # Initialize and run the server
    mcp.run(transport='stdio')