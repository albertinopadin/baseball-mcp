"""Abstract base class for NPB data sources."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from .models import NPBPlayer, NPBPlayerStats, NPBTeam


class AbstractNPBDataSource(ABC):
    """Abstract base class for all NPB data sources."""
    
    def __init__(self, base_url: str, cache_ttl: int = 86400):
        """Initialize the data source.
        
        Args:
            base_url: Base URL for the data source
            cache_ttl: Cache time-to-live in seconds (default: 24 hours)
        """
        self.base_url = base_url
        self.cache_ttl = cache_ttl
        self.name = self.__class__.__name__
    
    @abstractmethod
    async def search_player(self, name: str) -> List[NPBPlayer]:
        """Search for players by name.
        
        Args:
            name: Player name to search for (English or Japanese)
            
        Returns:
            List of matching players
        """
        pass
    
    @abstractmethod
    async def get_player_stats(
        self, 
        player_id: str, 
        season: Optional[int] = None,
        stats_type: str = "batting"
    ) -> Optional[NPBPlayerStats]:
        """Get player statistics.
        
        Args:
            player_id: Unique player identifier for this source
            season: Season year (None for current season)
            stats_type: Type of stats ("batting" or "pitching")
            
        Returns:
            Player statistics or None if not found
        """
        pass
    
    @abstractmethod
    async def get_teams(self, season: Optional[int] = None) -> List[NPBTeam]:
        """Get all NPB teams.
        
        Args:
            season: Season year (None for current season)
            
        Returns:
            List of NPB teams
        """
        pass
    
    @abstractmethod
    async def get_team_roster(
        self, 
        team_id: str, 
        season: Optional[int] = None
    ) -> List[NPBPlayer]:
        """Get team roster.
        
        Args:
            team_id: Unique team identifier for this source
            season: Season year (None for current season)
            
        Returns:
            List of players on the team
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the data source is available.
        
        Returns:
            True if source is healthy, False otherwise
        """
        pass
    
    def get_cache_key(self, method: str, *args, **kwargs) -> str:
        """Generate a cache key for a method call.
        
        Args:
            method: Method name
            *args: Method arguments
            **kwargs: Method keyword arguments
            
        Returns:
            Cache key string
        """
        # Convert args and kwargs to a string representation
        args_str = "_".join(str(arg) for arg in args)
        kwargs_str = "_".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
        components = [self.name, method, args_str, kwargs_str]
        return "_".join(c for c in components if c)
    
    async def get_player(self, player_id: str) -> Optional[NPBPlayer]:
        """Get detailed player information.
        
        Default implementation uses search, but sources can override.
        
        Args:
            player_id: Unique player identifier
            
        Returns:
            Player information or None if not found
        """
        # Default: search and filter
        # Sources can override with more efficient implementation
        return None