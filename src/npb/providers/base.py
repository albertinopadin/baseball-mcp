"""Base provider interface for NPB data sources."""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class NPBDataProvider(ABC):
    """Abstract base class for NPB data providers.
    
    This interface allows switching between different data sources
    (web scraping, commercial APIs, etc.) without changing client code.
    """
    
    @abstractmethod
    async def search_player(self, name: str) -> List[Dict[str, Any]]:
        """Search for players by name.
        
        Args:
            name: Player name to search for (English or romanized Japanese)
            
        Returns:
            List of player dictionaries with at least:
            - id: Unique identifier for the player
            - name_english: Player name in English
            - name_japanese: Player name in Japanese (if available)
            - team: Current or last team
            - position: Player position
        """
        pass
    
    @abstractmethod
    async def get_player_stats(
        self, 
        player_id: str, 
        season: Optional[int] = None,
        stats_type: str = "season"
    ) -> Dict[str, Any]:
        """Get player statistics.
        
        Args:
            player_id: Unique player identifier
            season: Season year (None for current/latest)
            stats_type: Type of stats ("season", "career")
            
        Returns:
            Dictionary with player stats including traditional and advanced metrics
        """
        pass
    
    @abstractmethod
    async def get_team_roster(
        self, 
        team_id: str, 
        season: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get team roster.
        
        Args:
            team_id: Team identifier
            season: Season year (None for current)
            
        Returns:
            List of player dictionaries on the roster
        """
        pass
    
    @abstractmethod
    async def get_standings(
        self, 
        league: Optional[str] = None,
        season: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get league standings.
        
        Args:
            league: "central", "pacific", or None for both
            season: Season year (None for current)
            
        Returns:
            Dictionary with standings data by league
        """
        pass
    
    @abstractmethod
    async def get_teams(self) -> List[Dict[str, Any]]:
        """Get all NPB teams.
        
        Returns:
            List of team dictionaries with:
            - id: Team identifier
            - name_english: Team name in English
            - name_japanese: Team name in Japanese
            - league: "central" or "pacific"
            - city: Team city/location
        """
        pass