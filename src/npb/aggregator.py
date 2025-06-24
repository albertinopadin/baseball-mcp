"""NPB data aggregator for combining multiple sources."""

from typing import List, Optional, Dict, Any
from collections import defaultdict

from .base import AbstractNPBDataSource
from .models import NPBPlayer, NPBPlayerStats, NPBTeam
from .sources import get_source, list_sources


class NPBDataAggregator:
    """Aggregates data from multiple NPB sources with priority and fallback."""
    
    def __init__(self, sources: Optional[List[AbstractNPBDataSource]] = None):
        """Initialize aggregator with data sources.
        
        Args:
            sources: List of data sources (if None, uses all registered sources)
        """
        if sources is None:
            # Load all registered sources
            self.sources = {}
            for source_name in list_sources():
                source_class = get_source(source_name)
                if source_class:
                    self.sources[source_name] = source_class()
        else:
            # Find registered name for each source
            self.sources = {}
            source_names = list_sources()
            for source in sources:
                # Match source by class type
                for name in source_names:
                    source_class = get_source(name)
                    if source_class and isinstance(source, source_class):
                        self.sources[name] = source
                        break
                else:
                    # If not registered, use class name
                    self.sources[source.__class__.__name__.lower()] = source
        
        # Default source priorities
        self.source_priorities = {
            'player_search': ['baseball_reference', 'npb_official', 'fangraphs'],
            'player_stats': ['baseball_reference', 'npb_official', 'fangraphs'],
            'player_stats_current': ['npb_official', 'fangraphs', 'baseball_reference'],
            'player_stats_historical': ['baseball_reference'],
            'teams': ['npb_official'],
            'team_roster': ['npb_official']
        }
    
    def set_priorities(self, operation: str, sources: List[str]):
        """Set source priorities for a specific operation.
        
        Args:
            operation: Operation name (e.g., 'player_search')
            sources: Ordered list of source names
        """
        self.source_priorities[operation] = sources
    
    async def search_player(
        self, 
        name: str, 
        source: Optional[str] = None
    ) -> List[NPBPlayer]:
        """Search for players across sources.
        
        Args:
            name: Player name to search
            source: Specific source to use (optional)
            
        Returns:
            List of matching players
        """
        if source:
            # Use specific source
            if source in self.sources:
                try:
                    return await self.sources[source].search_player(name)
                except Exception as e:
                    print(f"Error searching in {source}: {e}")
                    return []
            else:
                return []
        
        # Try sources by priority
        all_players = []
        seen_ids = set()
        
        for source_name in self.source_priorities.get('player_search', []):
            if source_name not in self.sources:
                continue
            
            try:
                players = await self.sources[source_name].search_player(name)
                
                # Merge results, avoiding duplicates
                for player in players:
                    if player.id not in seen_ids:
                        seen_ids.add(player.id)
                        all_players.append(player)
                
                # If we found players in primary source, we can stop
                if all_players and source_name == self.source_priorities['player_search'][0]:
                    break
                    
            except Exception as e:
                print(f"Error searching in {source_name}: {e}")
                continue
        
        return all_players
    
    async def get_player_stats(
        self,
        player_id: str,
        season: Optional[int] = None,
        stats_type: str = "batting",
        source: Optional[str] = None
    ) -> Optional[NPBPlayerStats]:
        """Get player statistics from sources.
        
        Args:
            player_id: Player ID
            season: Season year
            stats_type: Type of stats
            source: Specific source to use
            
        Returns:
            Player statistics (combined from sources if needed)
        """
        if source:
            # Use specific source
            if source in self.sources:
                try:
                    return await self.sources[source].get_player_stats(
                        player_id, season, stats_type
                    )
                except Exception as e:
                    print(f"Error getting stats from {source}: {e}")
                    return None
            else:
                return None
        
        # Try sources by priority
        base_stats = None
        
        for source_name in self.source_priorities.get('player_stats', []):
            if source_name not in self.sources:
                continue
            
            try:
                stats = await self.sources[source_name].get_player_stats(
                    player_id, season, stats_type
                )
                
                if stats:
                    if not base_stats:
                        base_stats = stats
                    else:
                        # Merge advanced stats if available
                        base_stats = self._merge_stats(base_stats, stats)
                    
                    # If we have all the data we need, stop
                    if base_stats and base_stats.war is not None:
                        break
                        
            except Exception as e:
                print(f"Error getting stats from {source_name}: {e}")
                continue
        
        return base_stats
    
    def _merge_stats(
        self, 
        primary: NPBPlayerStats, 
        secondary: NPBPlayerStats
    ) -> NPBPlayerStats:
        """Merge statistics from two sources.
        
        Args:
            primary: Primary stats object
            secondary: Secondary stats object
            
        Returns:
            Merged stats object
        """
        # Start with primary stats
        merged = primary
        
        # Add any missing advanced stats from secondary
        if secondary.war is not None and primary.war is None:
            merged.war = secondary.war
        if secondary.wrc_plus is not None and primary.wrc_plus is None:
            merged.wrc_plus = secondary.wrc_plus
        if secondary.xwoba is not None and primary.xwoba is None:
            merged.xwoba = secondary.xwoba
        if secondary.fip is not None and primary.fip is None:
            merged.fip = secondary.fip
        if secondary.xfip is not None and primary.xfip is None:
            merged.xfip = secondary.xfip
        
        # Update source to indicate merged data
        merged.source = f"{primary.source}+{secondary.source}"
        
        return merged
    
    async def get_teams(
        self, 
        season: Optional[int] = None,
        source: Optional[str] = None
    ) -> List[NPBTeam]:
        """Get all NPB teams.
        
        Args:
            season: Season year
            source: Specific source to use
            
        Returns:
            List of teams
        """
        if source:
            if source in self.sources:
                try:
                    return await self.sources[source].get_teams(season)
                except Exception:
                    return []
            else:
                return []
        
        # Use primary source for teams
        for source_name in self.source_priorities.get('teams', []):
            if source_name in self.sources:
                try:
                    teams = await self.sources[source_name].get_teams(season)
                    if teams:
                        return teams
                except Exception:
                    continue
        
        return []
    
    async def health_check(self) -> Dict[str, bool]:
        """Check health of all sources.
        
        Returns:
            Dictionary of source name to health status
        """
        health_status = {}
        
        for source_name, source in self.sources.items():
            try:
                health_status[source_name] = await source.health_check()
            except Exception:
                health_status[source_name] = False
        
        return health_status