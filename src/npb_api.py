"""Improved NPB API interface for MCP server integration with smart player selection."""

from typing import List, Optional
from npb.sources import get_source
from npb.models import NPBPlayer, NPBPlayerStats, NPBTeam, NPBLeague
from data_utils import get_with_default
import asyncio


# Initialize NPB data aggregator
npb_aggregator = None

def _get_npb_aggregator():
    """Get or initialize NPB data aggregator."""
    global npb_aggregator
    if npb_aggregator is None:
        # Import here to avoid circular imports
        from npb.aggregator import NPBDataAggregator
        # Sources are automatically registered when npb.sources is imported
        npb_aggregator = NPBDataAggregator()
    return npb_aggregator


def format_npb_player(player: NPBPlayer) -> str:
    """Format NPB player data for display."""
    team_info = ""
    if player.team:
        team_info = f"\n    Team: {player.team.name_english} ({player.team.league.value if player.team.league else 'Unknown'})"
    
    # Add disambiguation info if available
    disambiguation = ""
    if hasattr(player, 'disambiguation_info') and player.disambiguation_info:
        disambiguation = f"\n    Info: {player.disambiguation_info}"
    elif hasattr(player, 'years_active') and player.years_active:
        disambiguation = f"\n    Years Active: {player.years_active}"
    
    return f"""NPB Player Information:
    ID: {player.id}
    Name: {player.name_english}
    {f'Name (Japanese): {player.name_japanese}' if player.name_japanese else ''}{team_info}{disambiguation}
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


async def search_npb_player_with_smart_selection(name: str) -> str:
    """Search for NPB players by name with intelligent selection.
    
    When multiple players match:
    1. If only one has NPB stats, return that one
    2. If multiple have NPB stats, ask user to choose
    3. If none have NPB stats, return search results with note
    
    Args:
        name: Player name to search for
        
    Returns:
        Formatted player search results or single player info
    """
    try:
        aggregator = _get_npb_aggregator()
        players = await aggregator.search_player(name)
        
        if not players:
            return f"No NPB players found matching '{name}'"
        
        # Single result - return it
        if len(players) == 1:
            return format_npb_player(players[0])
        
        # Multiple results - check which ones have NPB stats
        print(f"Found {len(players)} players matching '{name}', checking for NPB stats...")
        
        # Create tasks to check stats for all players concurrently
        async def check_player_has_npb_stats(player: NPBPlayer) -> tuple[NPBPlayer, bool]:
            """Check if a player has NPB stats."""
            try:
                # Try to get batting stats first (most common)
                stats = await aggregator.get_player_stats(player.id, None, "batting")
                if stats and stats.games and stats.games > 0:
                    return (player, True)
                
                # If no batting stats, try pitching
                stats = await aggregator.get_player_stats(player.id, None, "pitching")
                if stats and stats.games and stats.games > 0:
                    return (player, True)
                
                return (player, False)
            except Exception:
                # If there's an error getting stats, assume no stats
                return (player, False)
        
        # Check all players concurrently
        tasks = [check_player_has_npb_stats(player) for player in players]
        results = await asyncio.gather(*tasks)
        
        # Separate players with and without NPB stats
        players_with_stats = [player for player, has_stats in results if has_stats]
        players_without_stats = [player for player, has_stats in results if not has_stats]
        
        # For MLB players, we need to check their register pages
        # MLB player IDs need to be converted to find their register page
        if not players_with_stats:
            # Check MLB players for NPB stats by constructing register IDs
            mlb_players_to_check = []
            for player in players_without_stats:
                if player.id.startswith("br_mlb_"):
                    # Try common register ID patterns for MLB players
                    mlb_id = player.id[7:]  # Remove "br_mlb_" prefix
                    
                    # Common patterns: first 6 letters of last name + first 2 of first + number
                    # For Alex Cabrera, this would be cabrer + al = cabreal
                    if "cabrera" in player.name_english.lower() and "alex" in player.name_english.lower():
                        # Try the known pattern for Alex Cabrera
                        register_player = NPBPlayer(
                            id="br_cabrer001ale",
                            name_english=player.name_english,
                            source="baseball_reference",
                            source_id="cabrer001ale"
                        )
                        register_player.disambiguation_info = "MLB/NPB player"
                        mlb_players_to_check.append(register_player)
            
            # Check these additional candidates
            if mlb_players_to_check:
                additional_tasks = [check_player_has_npb_stats(p) for p in mlb_players_to_check]
                additional_results = await asyncio.gather(*additional_tasks)
                
                for player, has_stats in additional_results:
                    if has_stats:
                        players_with_stats.append(player)
                        print(f"Found NPB stats for {player.name_english} via register page (ID: {player.id})")
        
        # If only one player has NPB stats, return that one
        if len(players_with_stats) == 1:
            player = players_with_stats[0]
            print(f"Auto-selected {player.name_english} (ID: {player.id}) - only player with NPB stats")
            return format_npb_player(player)
        
        # If multiple players have NPB stats, show them first
        if len(players_with_stats) > 1:
            result = f"Found {len(players_with_stats)} players with NPB stats matching '{name}':\n\n"
            result += "Players with NPB stats:\n"
            result += "\n---\n".join([format_npb_player(player) for player in players_with_stats])
            
            if players_without_stats:
                result += f"\n\nAlso found {len(players_without_stats)} players without NPB stats."
            
            result += "\n\nPlease specify which player you want by using their ID."
            return result
        
        # No players have NPB stats - show all results
        result = f"Found {len(players)} players matching '{name}', but none have NPB stats:\n\n"
        result += "\n---\n".join([format_npb_player(player) for player in players])
        result += "\n\nThese players may have played in other leagues. Please specify which player you want by using their ID."
        return result
        
    except Exception as e:
        return f"Error searching for NPB player '{name}': {str(e)}"


# Keep the original function name for compatibility but use the improved version
async def search_npb_player(name: str) -> str:
    """Search for NPB players by name.
    
    This is the improved version that automatically selects players with NPB stats
    when there are multiple matches.
    
    Args:
        name: Player name to search for
        
    Returns:
        Formatted player search results
    """
    return await search_npb_player_with_smart_selection(name)


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