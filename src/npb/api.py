"""High-level NPB API for MCP integration."""

from typing import Optional, List, Dict, Any
import logging

from .providers.base import NPBDataProvider
from .providers.scraper_provider import ScraperProvider
from .providers.composite_provider import CompositeProvider
from cache_utils import cache_result

logger = logging.getLogger(__name__)


class NPBAPI:
    """High-level API for NPB data access."""
    
    def __init__(self, provider: Optional[NPBDataProvider] = None, use_historical: bool = True):
        """Initialize NPB API with a data provider.
        
        Args:
            provider: Data provider instance (defaults to CompositeProvider)
            use_historical: Whether to include historical data (default True)
        """
        if provider:
            self.provider = provider
        elif use_historical:
            self.provider = CompositeProvider()
        else:
            self.provider = ScraperProvider()
    
    @cache_result(ttl_hours=24)  # 24 hour cache
    async def search_player(self, name: str) -> str:
        """Search for NPB players by name.
        
        Args:
            name: Player name to search for
            
        Returns:
            Formatted string with search results
        """
        try:
            results = await self.provider.search_player(name)
            
            if not results:
                return f"No NPB players found matching '{name}'"
            
            # Format results
            output = [f"Found {len(results)} NPB player(s) matching '{name}':\n"]
            
            for i, player in enumerate(results, 1):
                output.append(f"{i}. {player['name_english']}")
                
                if player.get('name_japanese'):
                    output.append(f"   Japanese: {player['name_japanese']}")
                
                if player.get('id'):
                    output.append(f"   ID: {player['id']}")
                
                if player.get('position'):
                    output.append(f"   Position: {player['position']}")
                
                if player.get('team'):
                    output.append(f"   Team: {player['team']}")
                
                if player.get('years_active'):
                    output.append(f"   Years Active: {player['years_active']}")
                
                output.append("")  # Empty line between players
            
            return "\n".join(output)
            
        except Exception as e:
            logger.error(f"Error searching for player {name}: {e}")
            return f"Error searching for NPB players: {str(e)}"
    
    @cache_result(ttl_hours=24)  # 24 hour cache
    async def get_player_stats(
        self, 
        player_id: str, 
        season: Optional[str] = None,
        stats_type: str = "season"
    ) -> str:
        """Get NPB player statistics.
        
        Args:
            player_id: Player identifier
            season: Season year as string (None for career)
            stats_type: Type of stats (currently only "season" supported)
            
        Returns:
            Formatted string with player statistics
        """
        try:
            # Convert season to int if provided
            season_int = int(season) if season else None
            
            stats_data = await self.provider.get_player_stats(
                player_id, season_int, stats_type
            )
            
            if "error" in stats_data:
                return stats_data["error"]
            
            # Format player info
            player_info = stats_data.get("player_info", {})
            output = []
            
            if player_info.get("name_english"):
                output.append(f"NPB Player Statistics: {player_info['name_english']}")
                output.append("=" * 50)
                
                if player_info.get("position"):
                    output.append(f"Position: {player_info['position']}")
                if player_info.get("bats"):
                    output.append(f"Bats: {player_info['bats']} / Throws: {player_info.get('throws', 'Unknown')}")
                if player_info.get("height"):
                    output.append(f"Height: {player_info['height']} / Weight: {player_info.get('weight', 'Unknown')}")
                output.append("")
            
            # Format statistics
            stats_type = stats_data.get("stats_type", "unknown")
            stats_list = stats_data.get("stats", [])
            
            if not stats_list:
                output.append("No statistics available")
                return "\n".join(output)
            
            if season_int:
                output.append(f"{season} Season Statistics:")
            else:
                output.append("Career Statistics by Season:")
            
            output.append("")
            
            if stats_type == "batting":
                output.extend(self._format_batting_stats(stats_list))
            elif stats_type == "pitching":
                output.extend(self._format_pitching_stats(stats_list))
            
            # Add career totals if available
            if not season_int and "career_totals" in stats_data:
                output.append("\nCareer Totals:")
                output.append("-" * 40)
                if stats_type == "batting":
                    output.extend(self._format_batting_career(stats_data["career_totals"]))
                elif stats_type == "pitching":
                    output.extend(self._format_pitching_career(stats_data["career_totals"]))
            
            return "\n".join(output)
            
        except Exception as e:
            logger.error(f"Error getting player stats for {player_id}: {e}")
            return f"Error retrieving NPB player statistics: {str(e)}"
    
    async def get_teams(self) -> str:
        """Get all NPB teams.
        
        Returns:
            Formatted string with team information
        """
        try:
            teams = await self.provider.get_teams()
            
            output = ["NPB Teams (Nippon Professional Baseball)"]
            output.append("=" * 50)
            output.append("")
            
            # Group by league
            central_teams = [t for t in teams if t["league"] == "central"]
            pacific_teams = [t for t in teams if t["league"] == "pacific"]
            
            output.append("Central League:")
            output.append("-" * 20)
            for team in central_teams:
                output.append(f"• {team['name_english']} ({team['abbreviation']})")
                output.append(f"  {team['name_japanese']}")
                output.append(f"  City: {team['city']}")
                output.append("")
            
            output.append("Pacific League:")
            output.append("-" * 20)
            for team in pacific_teams:
                output.append(f"• {team['name_english']} ({team['abbreviation']})")
                output.append(f"  {team['name_japanese']}")
                output.append(f"  City: {team['city']}")
                output.append("")
            
            return "\n".join(output)
            
        except Exception as e:
            logger.error(f"Error getting teams: {e}")
            return f"Error retrieving NPB teams: {str(e)}"
    
    def _format_batting_stats(self, stats_list: List[Dict]) -> List[str]:
        """Format batting statistics for display."""
        output = []
        
        # Header
        output.append(f"{'Year':<6} {'Team':<10} {'G':<4} {'AB':<5} {'R':<4} {'H':<4} {'HR':<4} {'RBI':<4} {'AVG':<6} {'OBP':<6} {'SLG':<6} {'OPS':<6}")
        output.append("-" * 80)
        
        for stats in stats_list:
            year = stats.get("season", "")
            team = stats.get("team", "")[:10]  # Truncate long team names
            
            line = (
                f"{year:<6} {team:<10} "
                f"{stats.get('games', 0):<4} "
                f"{stats.get('at_bats', 0):<5} "
                f"{stats.get('runs', 0):<4} "
                f"{stats.get('hits', 0):<4} "
                f"{stats.get('home_runs', 0):<4} "
                f"{stats.get('rbis', 0):<4} "
                f"{stats.get('batting_average', 0):<6.3f} "
                f"{stats.get('on_base_percentage', 0):<6.3f} "
                f"{stats.get('slugging_percentage', 0):<6.3f} "
                f"{stats.get('ops', 0):<6.3f}"
            )
            output.append(line)
        
        return output
    
    def _format_pitching_stats(self, stats_list: List[Dict]) -> List[str]:
        """Format pitching statistics for display."""
        output = []
        
        # Header
        output.append(f"{'Year':<6} {'Team':<10} {'W':<3} {'L':<3} {'ERA':<6} {'G':<4} {'GS':<4} {'IP':<7} {'SO':<4} {'BB':<4} {'WHIP':<6}")
        output.append("-" * 80)
        
        for stats in stats_list:
            year = stats.get("season", "")
            team = stats.get("team", "")[:10]  # Truncate long team names
            
            line = (
                f"{year:<6} {team:<10} "
                f"{stats.get('wins', 0):<3} "
                f"{stats.get('losses', 0):<3} "
                f"{stats.get('era', 0):<6.2f} "
                f"{stats.get('games', 0):<4} "
                f"{stats.get('games_started', 0):<4} "
                f"{stats.get('innings_pitched', 0):<7.1f} "
                f"{stats.get('strikeouts', 0):<4} "
                f"{stats.get('walks', 0):<4} "
                f"{stats.get('whip', 0):<6.3f}"
            )
            output.append(line)
        
        return output
    
    def _format_batting_career(self, totals: Dict) -> List[str]:
        """Format career batting totals."""
        output = []
        output.append(f"Games: {totals.get('games', 0)}")
        output.append(f"At Bats: {totals.get('at_bats', 0)}")
        output.append(f"Hits: {totals.get('hits', 0)}")
        output.append(f"Home Runs: {totals.get('home_runs', 0)}")
        output.append(f"RBIs: {totals.get('rbis', 0)}")
        output.append(f"Batting Average: {totals.get('batting_average', 0):.3f}")
        output.append(f"OPS: {totals.get('ops', 0):.3f}")
        return output
    
    def _format_pitching_career(self, totals: Dict) -> List[str]:
        """Format career pitching totals."""
        output = []
        output.append(f"Games: {totals.get('games', 0)}")
        output.append(f"Wins-Losses: {totals.get('wins', 0)}-{totals.get('losses', 0)}")
        output.append(f"ERA: {totals.get('era', 0):.2f}")
        output.append(f"Innings Pitched: {totals.get('innings_pitched', 0):.1f}")
        output.append(f"Strikeouts: {totals.get('strikeouts', 0)}")
        output.append(f"WHIP: {totals.get('whip', 0):.3f}")
        return output