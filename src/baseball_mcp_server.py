from mcp.server.fastmcp import FastMCP
import mlb_stats_api
import statcast_api
import sports_api
import npb_api
from sports_constants import MLB, TRIPLE_A, DOUBLE_A, HIGH_A, SINGLE_A, ROOKIE, NIPPON_PROFESSIONAL as NPB

try:
    from importlib.metadata import version
    VERSION = version("baseball-mcp")
except Exception:
    VERSION = "0.0.11"  # Fallback version

mcp = FastMCP("BaseballMcp")


# Sports/League information
@mcp.tool()
async def get_available_sports() -> str:
    """Get list of all available sports/leagues in the MLB Stats API.
    
    Returns information about all available sports including:
    - MLB (sport_id: 1)
    - Minor Leagues: Triple-A (11), Double-A (12), High-A (13), Single-A (14), Rookie (16)
    - International leagues (KBO, NPB, etc.)
    - Other baseball organizations
    
    Use these sport IDs with player stats, team search, and schedule functions.
    """
    return await sports_api.get_available_sports()


# MLB Stats API tools
@mcp.tool()
async def search_player(search_str: str, sport_id: int = 1) -> str:
    """Search for baseball players across all leagues (MLB, Minor Leagues, and NPB).

    Args:
        search_str: Name of player to search for
        sport_id: Sport ID (1 for MLB/MiLB, 31 for NPB)
    
    Note: Returns players from all levels. Use get_player_stats with specific 
    sport_id to get minor league or NPB statistics.
    """
    if sport_id == NPB:
        return await npb_api.search_npb_player(search_str)
    return await mlb_stats_api.search_player(search_str)


@mcp.tool()
async def get_player(person_id: int, season: str | None = None, accent: bool = True) -> str:
    """Get detailed information about a specific MLB player.
    
    Args:
        person_id: Unique Player Identifier (e.g., 434538, 429665)
        season: Season of play (optional)
        accent: Include accent marks in player names (default: True)
    """
    return await mlb_stats_api.get_player(person_id, season, accent)


@mcp.tool()
async def get_player_stats(
    person_id: int | str,
    stats: str,
    season: str | None = None,
    sport_id: int = 1,
    group: str | None = None
) -> str:
    """Get statistics for a specific player (MLB, Minor Leagues, or NPB).
    
    Args:
        person_id: Unique Player Identifier (int for MLB/MiLB, str for NPB)
        stats: Type of statistics:
               - MLB/MiLB: 'season', 'career', 'yearByYear', 'gameLog'
               - NPB: 'batting', 'pitching', or 'yearByYear' (for season-by-season breakdown)
        season: Season of play (optional)
        sport_id: Sport ID - Use 1 for MLB (default), minor league IDs, or:
                  - 11: Triple-A (AAA)
                  - 12: Double-A (AA)
                  - 13: High-A (A+)
                  - 14: Single-A (A)
                  - 16: Rookie (R)
                  - 31: NPB (Nippon Professional Baseball)
        group: Stat group (e.g., 'hitting', 'pitching', 'fielding') - MLB/MiLB only
    
    Note: For minor league stats, you must specify the exact sport_id for the level.
    Career stats only available for MLB (sport_id=1).
    For NPB, use string player_id. Use stats='yearByYear' to get season-by-season NPB stats.
    """
    if sport_id == NPB:
        if isinstance(person_id, int):
            person_id = str(person_id)
        # Map MLB stats types to NPB stats types
        npb_stats_type = "batting" if group != "pitching" else "pitching"
        if stats in ["batting", "pitching"]:
            npb_stats_type = stats
        
        # Check for special year-by-year request
        if stats == "yearByYear":
            return await npb_api.get_npb_player_year_by_year_stats(person_id, npb_stats_type)
        
        return await npb_api.get_npb_player_stats(person_id, int(season) if season else None, npb_stats_type)
    return await mlb_stats_api.get_player_stats(person_id, stats, season, sport_id, group)


@mcp.tool()
async def search_teams(
    season: str | None = None,
    sport_id: int = 1,
    active_status: str = "Y",
    league_id: int | None = None,
    division_id: int | None = None
) -> str:
    """Search for baseball teams (MLB, Minor Leagues, or NPB).
    
    Args:
        season: Season of play (optional)
        sport_id: Sport ID - Use 1 for MLB (default), minor league IDs, or:
                  - 11: Triple-A (AAA) - 30 teams
                  - 12: Double-A (AA) - 30 teams
                  - 13: High-A (A+) - 30 teams
                  - 14: Single-A (A) - 30 teams
                  - 16: Rookie (R)
                  - 31: NPB - 12 teams (6 Central, 6 Pacific)
        active_status: 'Y' for active, 'N' for inactive, 'B' for both
        league_id: League ID (optional) - Note: Minor leagues don't use AL/NL structure
        division_id: Division ID (optional)
    
    Example: To get all Triple-A teams, use sport_id=11
    Example: To get NPB teams, use sport_id=31
    """
    if sport_id == NPB:
        return await npb_api.get_npb_teams(int(season) if season else None)
    return await mlb_stats_api.search_teams(season, sport_id, active_status, league_id, division_id)


@mcp.tool()
async def get_team(team_id: int, season: str | None = None) -> str:
    """Get detailed information about a specific MLB team.
    
    Args:
        team_id: Unique Team Identifier (e.g., 141, 147)
        season: Season of play (optional)
    """
    return await mlb_stats_api.get_team(team_id, season)


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
    return await mlb_stats_api.get_team_roster(team_id, roster_type, season, date)


@mcp.tool()
async def get_schedule(
    sport_id: int = 1,
    season: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    team_id: int | None = None,
    game_type: str | None = None
) -> str:
    """Get baseball game schedule (MLB or Minor Leagues).
    
    Args:
        sport_id: Sport ID - Use 1 for MLB (default), or minor league IDs:
                  - 11: Triple-A (AAA)
                  - 12: Double-A (AA)
                  - 13: High-A (A+)
                  - 14: Single-A (A)
                  - 16: Rookie (R)
        season: Season of play (optional)
        start_date: Start date (format: 'YYYY-MM-DD')
        end_date: End date (format: 'YYYY-MM-DD')
        team_id: Filter by specific team (optional)
        game_type: Type of games (e.g., 'R' for regular season, 'P' for postseason)
    
    Example: To get Triple-A games for a date range, use sport_id=11
    """
    return await mlb_stats_api.get_schedule(sport_id, season, start_date, end_date, team_id, game_type)


@mcp.tool()
async def get_game_info(game_pk: int) -> str:
    """Get detailed information about a specific game (MLB or Minor Leagues).
    
    Args:
        game_pk: Unique Primary Key representing a game
    
    Note: Works for both MLB and minor league games. Get game_pk from schedule.
    Minor league games have boxscore data but not live feed data.
    """
    return await mlb_stats_api.get_game_info(game_pk)


@mcp.tool()
async def get_standings(
    league_id: int,
    season: str | None = None,
    standings_type: str = "regularSeason",
    date: str | None = None
) -> str:
    """Get league standings (MLB only - not available for minor leagues).
    
    Args:
        league_id: League ID (103 for AL, 104 for NL)
        season: Season of play (optional)
        standings_type: Type of standings (e.g., 'regularSeason', 'wildCard', 'divisionLeaders')
        date: Specific date for standings (format: 'YYYY-MM-DD')
    
    Note: Standings are only available for MLB. Minor leagues use different
    organizational structures and standings are not available via this API.
    """
    return await mlb_stats_api.get_standings(league_id, season, standings_type, date)


@mcp.tool()
async def get_live_game_feed(game_pk: int) -> str:
    """Get live feed data for an ongoing game (MLB only).
    
    Args:
        game_pk: Unique Primary Key representing a game
    
    Note: Live feeds are only available for MLB games. Minor league games
    will return a 404 error. Use get_game_info for minor league boxscores.
    """
    return await mlb_stats_api.get_live_game_feed(game_pk)


# Statcast tools
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
    return await statcast_api.get_player_statcast_batting(player_name, start_date, end_date, season)


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
    return await statcast_api.get_player_statcast_pitching(player_name, start_date, end_date, season)


def main():
    """Entry point for the baseball-mcp server."""
    print(f"Baseball Stats MCP Server v{VERSION}")
    # Initialize and run the server
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()