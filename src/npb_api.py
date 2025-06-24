"""NPB API interface for MCP server integration."""

from typing import List, Optional
from npb.sources import get_source
from npb.models import NPBPlayer, NPBPlayerStats, NPBTeam, NPBLeague
from data_utils import get_with_default


# Initialize NPB data aggregator
npb_aggregator = None

def _get_npb_aggregator():
    """Get or initialize NPB data aggregator."""
    global npb_aggregator
    if npb_aggregator is None:
        # Import here to avoid circular imports
        from npb.aggregator import NPBDataAggregator
        # Import sources to ensure registration
        from npb.sources import npb_official
        try:
            from npb.sources import fangraphs
        except:
            pass  # FanGraphs source may not be fully implemented
        
        # Let aggregator use all registered sources
        npb_aggregator = NPBDataAggregator()
    return npb_aggregator


def format_npb_player(player: NPBPlayer) -> str:
    """Format NPB player data for display."""
    team_info = ""
    if player.team:
        team_info = f"\n    Team: {player.team.name_english} ({player.team.league.value if player.team.league else 'Unknown'})"
    
    return f"""NPB Player Information:
    ID: {player.id}
    Name: {player.name_english}
    {f'Name (Japanese): {player.name_japanese}' if player.name_japanese else ''}{team_info}
    {f'Jersey Number: {player.jersey_number}' if player.jersey_number else ''}
    {f'Position: {player.position}' if player.position else ''}
    
    Source: {player.source}"""


def format_npb_stats(stats: NPBPlayerStats) -> str:
    """Format NPB player statistics for display."""
    result = f"""NPB Player Statistics:
    Player ID: {stats.player_id}
    Season: {stats.season}
    Type: {stats.stats_type}
    {f'Team: {stats.team.name_english}' if stats.team else ''}
    Games: {stats.games or 'N/A'}
    """
    
    if stats.stats_type == "batting":
        result += f"""
    Batting Statistics:
    AVG: {stats.batting_average or 'N/A'}
    HR: {stats.home_runs or 'N/A'}
    RBI: {stats.rbi or 'N/A'}
    H: {stats.hits or 'N/A'}
    2B: {stats.doubles or 'N/A'}
    3B: {stats.triples or 'N/A'}
    SB: {stats.stolen_bases or 'N/A'}
    BB: {stats.walks or 'N/A'}
    SO: {stats.strikeouts or 'N/A'}
    OBP: {stats.on_base_percentage or 'N/A'}
    SLG: {stats.slugging_percentage or 'N/A'}
    OPS: {stats.ops or 'N/A'}"""
    else:  # pitching
        result += f"""
    Pitching Statistics:
    W-L: {stats.wins or 0}-{stats.losses or 0}
    ERA: {stats.era or 'N/A'}
    SV: {stats.saves or 'N/A'}
    IP: {stats.innings_pitched or 'N/A'}
    SO: {stats.strikeouts_pitched or 'N/A'}
    BB: {stats.walks_allowed or 'N/A'}
    WHIP: {stats.whip or 'N/A'}"""
    
    # Add advanced stats if available
    if stats.war is not None:
        result += f"\n    WAR: {stats.war}"
    if stats.wrc_plus is not None:
        result += f"\n    wRC+: {stats.wrc_plus}"
    if stats.fip is not None:
        result += f"\n    FIP: {stats.fip}"
    
    result += f"\n\n    Source: {stats.source}"
    result += f"\n    Last Updated: {stats.last_updated}"
    
    return result


def format_npb_team(team: NPBTeam) -> str:
    """Format NPB team data for display."""
    return f"""NPB Team Information:
    ID: {team.id}
    Name: {team.name_english}
    {f'Name (Japanese): {team.name_japanese}' if team.name_japanese else ''}
    Abbreviation: {team.abbreviation or 'N/A'}
    League: {team.league.value if team.league else 'Unknown'}
    {f'City: {team.city}' if team.city else ''}
    {f'Stadium: {team.stadium}' if team.stadium else ''}
    {f'Founded: {team.founded}' if team.founded else ''}
    
    Source: {team.source}"""


async def search_npb_player(name: str) -> str:
    """Search for NPB players by name.
    
    Args:
        name: Player name to search for
        
    Returns:
        Formatted player search results
    """
    try:
        aggregator = _get_npb_aggregator()
        players = await aggregator.search_player(name)
        
        if not players:
            return f"No NPB players found matching '{name}'"
        
        results = [format_npb_player(player) for player in players]
        return "\n---\n".join(results)
        
    except Exception as e:
        return f"Error searching for NPB player '{name}': {str(e)}"


async def get_npb_player_stats(
    player_id: str,
    season: Optional[int] = None,
    stats_type: str = "batting"
) -> str:
    """Get NPB player statistics.
    
    Args:
        player_id: Player ID
        season: Season year (None for current)
        stats_type: "batting" or "pitching"
        
    Returns:
        Formatted player statistics
    """
    try:
        aggregator = _get_npb_aggregator()
        stats = await aggregator.get_player_stats(player_id, season, stats_type)
        
        if not stats:
            return f"No statistics found for NPB player ID '{player_id}'"
        
        return format_npb_stats(stats)
        
    except Exception as e:
        return f"Error retrieving NPB player stats: {str(e)}"


async def get_npb_teams(season: Optional[int] = None) -> str:
    """Get all NPB teams.
    
    Args:
        season: Season year (None for current)
        
    Returns:
        Formatted team list
    """
    try:
        aggregator = _get_npb_aggregator()
        teams = await aggregator.get_teams(season)
        
        if not teams:
            return "No NPB teams found"
        
        # Group by league
        central_teams = [t for t in teams if t.league == NPBLeague.CENTRAL]
        pacific_teams = [t for t in teams if t.league == NPBLeague.PACIFIC]
        
        result = "NPB Teams:\n\nCentral League:\n"
        for team in central_teams:
            result += f"  - {team.name_english} ({team.abbreviation})\n"
        
        result += "\nPacific League:\n"
        for team in pacific_teams:
            result += f"  - {team.name_english} ({team.abbreviation})\n"
        
        return result
        
    except Exception as e:
        return f"Error retrieving NPB teams: {str(e)}"


async def get_npb_team_roster(
    team_id: str,
    season: Optional[int] = None
) -> str:
    """Get NPB team roster.
    
    Args:
        team_id: Team ID
        season: Season year (None for current)
        
    Returns:
        Formatted team roster
    """
    try:
        aggregator = _get_npb_aggregator()
        # Use the primary source for rosters
        source_name = aggregator.source_priorities.get('team_roster', ['npb_official'])[0]
        if source_name in aggregator.sources:
            roster = await aggregator.sources[source_name].get_team_roster(team_id, season)
        else:
            return f"No source available for team rosters"
        
        if not roster:
            return f"No roster found for NPB team ID '{team_id}'"
        
        result = f"NPB Team Roster ({len(roster)} players):\n\n"
        for player in roster:
            result += f"  #{player.jersey_number or 'N/A'} {player.name_english}"
            if player.position:
                result += f" - {player.position}"
            result += "\n"
        
        return result
        
    except Exception as e:
        return f"Error retrieving NPB team roster: {str(e)}"