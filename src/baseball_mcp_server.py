from mcp.server.fastmcp import FastMCP
import mlb_stats_api
import statcast_api

try:
    from importlib.metadata import version
    VERSION = version("baseball-mcp")
except Exception:
    VERSION = "0.0.4"  # Fallback version

mcp = FastMCP("BaseballMcp")


# MLB Stats API tools
@mcp.tool()
async def search_player(search_str: str) -> str:
    """Search for MLB player.

    Args:
        search_str: Name of player to search for
    """
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
    return await mlb_stats_api.get_player_stats(person_id, stats, season, sport_id, group)


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
    """Get MLB game schedule.
    
    Args:
        sport_id: Sport ID (default: 1 for MLB)
        season: Season of play (optional)
        start_date: Start date (format: 'YYYY-MM-DD')
        end_date: End date (format: 'YYYY-MM-DD')
        team_id: Filter by specific team (optional)
        game_type: Type of games (e.g., 'R' for regular season, 'P' for postseason)
    """
    return await mlb_stats_api.get_schedule(sport_id, season, start_date, end_date, team_id, game_type)


@mcp.tool()
async def get_game_info(game_pk: int) -> str:
    """Get detailed information about a specific game.
    
    Args:
        game_pk: Unique Primary Key representing a game
    """
    return await mlb_stats_api.get_game_info(game_pk)


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
    return await mlb_stats_api.get_standings(league_id, season, standings_type, date)


@mcp.tool()
async def get_live_game_feed(game_pk: int) -> str:
    """Get live feed data for an ongoing game.
    
    Args:
        game_pk: Unique Primary Key representing a game
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