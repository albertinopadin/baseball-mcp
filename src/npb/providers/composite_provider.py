"""Composite provider that combines historical and modern NPB data."""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

from .base import NPBDataProvider
from .historical_provider import HistoricalDataProvider
from .scraper_provider import ScraperProvider

logger = logging.getLogger(__name__)


class CompositeProvider(NPBDataProvider):
    """Combines historical database with modern web scraping.
    
    Uses historical provider for data before 2005 and scraper provider
    for 2005 and later, providing seamless access to all NPB data.
    """
    
    HISTORICAL_CUTOFF_YEAR = 2005  # NPB official site has data from ~2005
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize composite provider.
        
        Args:
            db_path: Path to historical database
        """
        self.historical_provider = HistoricalDataProvider(db_path)
        self.scraper_provider = ScraperProvider()
        self.current_year = datetime.now().year
    
    async def search_player(self, name: str) -> List[Dict[str, Any]]:
        """Search for players across both historical and modern data.
        
        Args:
            name: Player name to search for
            
        Returns:
            Combined list of player dictionaries
        """
        # Search both providers
        historical_results = await self.historical_provider.search_player(name)
        modern_results = await self.scraper_provider.search_player(name)
        
        # Combine results, avoiding duplicates
        all_results = []
        seen_ids = set()
        
        # Add historical results first
        for player in historical_results:
            player['source'] = 'historical'
            all_results.append(player)
            seen_ids.add(player.get('id'))
        
        # Add modern results if not already in historical
        for player in modern_results:
            player_id = player.get('id')
            if player_id and player_id not in seen_ids:
                player['source'] = 'modern'
                all_results.append(player)
        
        return all_results
    
    async def get_player_stats(
        self, 
        player_id: str, 
        season: Optional[int] = None,
        stats_type: str = "season"
    ) -> Dict[str, Any]:
        """Get player statistics from appropriate source based on year.
        
        Args:
            player_id: Unique player identifier
            season: Season year (None for career)
            stats_type: Type of stats ("season" or "career")
            
        Returns:
            Dictionary with player stats
        """
        # If specific season requested, route to appropriate provider
        if season:
            if season < self.HISTORICAL_CUTOFF_YEAR:
                return await self.historical_provider.get_player_stats(player_id, season, stats_type)
            else:
                return await self.scraper_provider.get_player_stats(player_id, season, stats_type)
        
        # For career stats, we need to check both sources
        # First try historical
        historical_stats = await self.historical_provider.get_player_stats(player_id, None, stats_type)
        
        # If found in historical, check if player also has modern stats
        if "error" not in historical_stats:
            # Check if player continued after cutoff year
            if historical_stats.get("stats"):
                last_year = max(stat.get("season", 0) for stat in historical_stats["stats"])
                
                if last_year >= self.HISTORICAL_CUTOFF_YEAR - 1:
                    # Player might have modern stats too
                    try:
                        modern_stats = await self.scraper_provider.get_player_stats(player_id, None, stats_type)
                        if "error" not in modern_stats and modern_stats.get("stats"):
                            # Combine stats
                            all_stats = historical_stats["stats"] + modern_stats["stats"]
                            
                            # Remove duplicates (same year)
                            seen_years = set()
                            unique_stats = []
                            for stat in sorted(all_stats, key=lambda x: x.get("season", 0)):
                                year = stat.get("season")
                                if year not in seen_years:
                                    unique_stats.append(stat)
                                    seen_years.add(year)
                            
                            historical_stats["stats"] = unique_stats
                            historical_stats["source"] = "combined"
                            
                            # Recalculate career totals
                            if historical_stats.get("stats_type") == "batting":
                                historical_stats["career_totals"] = self._calculate_batting_totals(unique_stats)
                            elif historical_stats.get("stats_type") == "pitching":
                                historical_stats["career_totals"] = self._calculate_pitching_totals(unique_stats)
                    except Exception as e:
                        logger.debug(f"No modern stats found for {player_id}: {e}")
            
            return historical_stats
        
        # Not in historical, try modern
        return await self.scraper_provider.get_player_stats(player_id, season, stats_type)
    
    def _calculate_batting_totals(self, stats_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate career batting totals from season stats."""
        totals = {
            "seasons": len(stats_list),
            "games": sum(s.get("games", 0) for s in stats_list),
            "at_bats": sum(s.get("at_bats", 0) for s in stats_list),
            "runs": sum(s.get("runs", 0) for s in stats_list),
            "hits": sum(s.get("hits", 0) for s in stats_list),
            "doubles": sum(s.get("doubles", 0) for s in stats_list),
            "triples": sum(s.get("triples", 0) for s in stats_list),
            "home_runs": sum(s.get("home_runs", 0) for s in stats_list),
            "rbis": sum(s.get("rbis", 0) for s in stats_list),
            "stolen_bases": sum(s.get("stolen_bases", 0) for s in stats_list),
            "walks": sum(s.get("walks", 0) for s in stats_list),
            "strikeouts": sum(s.get("strikeouts", 0) for s in stats_list),
        }
        
        # Calculate averages
        if totals["at_bats"] > 0:
            totals["batting_average"] = round(totals["hits"] / totals["at_bats"], 3)
        else:
            totals["batting_average"] = 0.0
        
        return totals
    
    def _calculate_pitching_totals(self, stats_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate career pitching totals from season stats."""
        totals = {
            "seasons": len(stats_list),
            "wins": sum(s.get("wins", 0) for s in stats_list),
            "losses": sum(s.get("losses", 0) for s in stats_list),
            "games": sum(s.get("games", 0) for s in stats_list),
            "games_started": sum(s.get("games_started", 0) for s in stats_list),
            "complete_games": sum(s.get("complete_games", 0) for s in stats_list),
            "shutouts": sum(s.get("shutouts", 0) for s in stats_list),
            "saves": sum(s.get("saves", 0) for s in stats_list),
            "innings_pitched": sum(s.get("innings_pitched", 0) for s in stats_list),
            "hits_allowed": sum(s.get("hits_allowed", 0) for s in stats_list),
            "earned_runs": sum(s.get("earned_runs", 0) for s in stats_list),
            "walks": sum(s.get("walks", 0) for s in stats_list),
            "strikeouts": sum(s.get("strikeouts", 0) for s in stats_list),
        }
        
        # Calculate rates
        if totals["innings_pitched"] > 0:
            totals["era"] = round((totals["earned_runs"] * 9) / totals["innings_pitched"], 2)
            totals["whip"] = round((totals["hits_allowed"] + totals["walks"]) / totals["innings_pitched"], 3)
        else:
            totals["era"] = 0.0
            totals["whip"] = 0.0
        
        return totals
    
    async def get_team_roster(
        self, 
        team_id: str, 
        season: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get team roster from appropriate source.
        
        Args:
            team_id: Team identifier
            season: Season year
            
        Returns:
            List of player dictionaries on the roster
        """
        if season and season < self.HISTORICAL_CUTOFF_YEAR:
            return await self.historical_provider.get_team_roster(team_id, season)
        elif season:
            return await self.scraper_provider.get_team_roster(team_id, season)
        else:
            # Get all-time roster from historical
            return await self.historical_provider.get_team_roster(team_id, None)
    
    async def get_standings(
        self, 
        league: Optional[str] = None,
        season: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get league standings (only available for modern seasons).
        
        Args:
            league: "central", "pacific", or None for both
            season: Season year
            
        Returns:
            Dictionary with standings data
        """
        # Standings only available from scraper
        if season and season < self.HISTORICAL_CUTOFF_YEAR:
            return {
                "error": f"Standings data not available for {season}",
                "message": "Historical standings are not included in the database"
            }
        
        return await self.scraper_provider.get_standings(league, season)
    
    async def get_teams(self) -> List[Dict[str, Any]]:
        """Get all NPB teams.
        
        Returns:
            List of team dictionaries
        """
        # Use scraper for current teams, historical for defunct teams
        current_teams = await self.scraper_provider.get_teams()
        historical_teams = await self.historical_provider.get_teams()
        
        # Merge, preferring current data
        teams_dict = {}
        
        # Add historical first
        for team in historical_teams:
            teams_dict[team.get('id')] = team
        
        # Override with current
        for team in current_teams:
            teams_dict[team.get('id')] = team
        
        return list(teams_dict.values())