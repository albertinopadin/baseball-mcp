"""Web scraping implementation of NPB data provider."""

from typing import Optional, List, Dict, Any
import logging

from .base import NPBDataProvider
from ..scrapers.baseball_reference import BaseballReferenceNPBScraper
from ..scrapers.npb_official import NPBOfficialScraper
from ..constants import NPB_TEAMS, NPBLeague, get_teams_by_league

logger = logging.getLogger(__name__)


class ScraperProvider(NPBDataProvider):
    """NPB data provider using web scraping."""
    
    def __init__(self):
        # Use NPB official as primary, Baseball-Reference as fallback
        self.npb_scraper = NPBOfficialScraper()
        self.br_scraper = BaseballReferenceNPBScraper()
    
    async def search_player(self, name: str) -> List[Dict[str, Any]]:
        """Search for players by name using web scraping.
        
        Args:
            name: Player name to search for
            
        Returns:
            List of player dictionaries
        """
        # Try NPB official site first
        async with self.npb_scraper:
            results = await self.npb_scraper.search_players_by_stats(name)
            
            if results:
                # Enhance results with additional info if needed
                for result in results:
                    # Ensure required fields
                    if "name_japanese" not in result:
                        result["name_japanese"] = None
                return results
        
        # Fallback to Baseball-Reference (though it has Cloudflare issues)
        logger.info("No results from NPB official, trying Baseball-Reference")
        async with self.br_scraper:
            results = await self.br_scraper.search_players(name)
            
            # Enhance results with additional info if needed
            for result in results:
                # Ensure required fields
                if "name_japanese" not in result:
                    result["name_japanese"] = None
                if "team" not in result:
                    result["team"] = None
                if "position" not in result:
                    result["position"] = None
            
            return results
    
    async def get_player_stats(
        self, 
        player_id: str, 
        season: Optional[int] = None,
        stats_type: str = "season"
    ) -> Dict[str, Any]:
        """Get player statistics using web scraping.
        
        Args:
            player_id: Player ID
            season: Season year (None for current season)
            stats_type: Type of stats (currently only "season" supported)
            
        Returns:
            Dictionary with player stats
        """
        # For NPB official site, we need to get stats by year
        # and filter by player name/ID
        async with self.npb_scraper:
            if not season:
                season = await self.npb_scraper.get_current_season()
            
            # Try to determine if player is a batter or pitcher
            # For now, we'll try both and see which has data
            batting_stats = await self.npb_scraper.get_player_stats_by_year(season, "batting")
            pitching_stats = await self.npb_scraper.get_player_stats_by_year(season, "pitching")
            
            # Find the player in the stats
            player_batting = None
            player_pitching = None
            
            # Handle name variations and ID format differences
            player_id_lower = player_id.lower()
            player_id_variations = [player_id_lower]
            
            # Handle different ID formats
            # "otani-000sho" -> try "otani,_shohei" format
            if "-" in player_id_lower:
                # Extract the name part before the dash
                name_part = player_id_lower.split("-")[0]
                # Try common firstname variations
                if name_part == "otani" or name_part == "ohtani":
                    player_id_variations.extend([
                        "otani,_shohei",
                        "ohtani,_shohei",
                        "otani_shohei",
                        "ohtani_shohei"
                    ])
            
            # Also handle direct comma format
            if "," in player_id_lower:
                player_id_variations.append(player_id_lower.replace(",_", "_"))
                player_id_variations.append(player_id_lower.replace(",", "_"))
            
            # Handle ohtani/otani variations
            if "ohtani" in player_id_lower:
                player_id_variations.append(player_id_lower.replace("ohtani", "otani"))
            elif "otani" in player_id_lower:
                player_id_variations.append(player_id_lower.replace("otani", "ohtani"))
            
            for stat in batting_stats:
                stat_name_lower = stat.get("player_name", "").lower().replace(" ", "_")
                stat_id_lower = stat.get("player_id", "").lower()
                
                for pid_var in player_id_variations:
                    if stat_id_lower == pid_var or pid_var in stat_name_lower:
                        player_batting = stat
                        break
                if player_batting:
                    break
            
            for stat in pitching_stats:
                stat_name_lower = stat.get("player_name", "").lower().replace(" ", "_")
                stat_id_lower = stat.get("player_id", "").lower()
                
                for pid_var in player_id_variations:
                    if stat_id_lower == pid_var or pid_var in stat_name_lower:
                        player_pitching = stat
                        break
                if player_pitching:
                    break
            
            if player_batting:
                return {
                    "player_id": player_id,
                    "player_info": {
                        "name_english": player_batting.get("player_name", ""),
                        "team": player_batting.get("team", "")
                    },
                    "stats_type": "batting",
                    "season": season,
                    "stats": [player_batting]
                }
            elif player_pitching:
                return {
                    "player_id": player_id,
                    "player_info": {
                        "name_english": player_pitching.get("player_name", ""),
                        "team": player_pitching.get("team", "")
                    },
                    "stats_type": "pitching", 
                    "season": season,
                    "stats": [player_pitching]
                }
        
        # Fallback to Baseball-Reference (though it has issues)
        logger.info("No stats from NPB official, trying Baseball-Reference")
        async with self.br_scraper:
            stats_data = await self.br_scraper.get_player_stats(player_id, season)
            
            if not stats_data:
                return {
                    "error": f"No stats found for player {player_id}"
                }
            
            # Format response
            response = {
                "player_id": player_id,
                "player_info": stats_data.get("player", {}),
                "stats_type": stats_data.get("stats_type", "unknown"),
                "season": season,
                "stats": stats_data.get("stats", [])
            }
            
            # Calculate career totals if no specific season
            if not season and len(response["stats"]) > 1:
                response["career_totals"] = self._calculate_career_totals(
                    response["stats"], 
                    response["stats_type"]
                )
            
            return response
    
    async def get_team_roster(
        self, 
        team_id: str, 
        season: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get team roster.
        
        Note: This is a placeholder implementation.
        Full roster scraping will be implemented in a future update.
        
        Args:
            team_id: Team identifier
            season: Season year
            
        Returns:
            List of player dictionaries on the roster
        """
        # TODO: Implement roster scraping from Baseball-Reference
        logger.warning(f"Team roster scraping not yet implemented for {team_id}")
        return []
    
    async def get_standings(
        self, 
        league: Optional[str] = None,
        season: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get league standings.
        
        Args:
            league: "central", "pacific", or None for both
            season: Season year
            
        Returns:
            Dictionary with standings data by league
        """
        async with self.npb_scraper:
            standings_data = await self.npb_scraper.get_team_standings(season)
            
            if not standings_data:
                return {
                    "error": "Failed to retrieve standings data"
                }
            
            # Filter by league if specified
            if league and league in standings_data:
                return {
                    league: standings_data[league]
                }
            
            return standings_data
    
    async def get_teams(self) -> List[Dict[str, Any]]:
        """Get all NPB teams.
        
        Returns:
            List of team dictionaries
        """
        teams = []
        for team_id, team_data in NPB_TEAMS.items():
            teams.append({
                "id": team_id,
                "name_english": team_data["name_english"],
                "name_japanese": team_data["name_japanese"],
                "league": team_data["league"].value,
                "city": team_data["city"],
                "abbreviation": team_data["abbreviation"]
            })
        return teams
    
    def _calculate_career_totals(
        self, 
        stats_list: List[Dict[str, Any]], 
        stats_type: str
    ) -> Dict[str, Any]:
        """Calculate career totals from season stats.
        
        Args:
            stats_list: List of season statistics
            stats_type: "batting" or "pitching"
            
        Returns:
            Dictionary with career totals
        """
        if not stats_list:
            return {}
        
        if stats_type == "batting":
            totals = {
                "games": 0,
                "plate_appearances": 0,
                "at_bats": 0,
                "runs": 0,
                "hits": 0,
                "doubles": 0,
                "triples": 0,
                "home_runs": 0,
                "rbis": 0,
                "stolen_bases": 0,
                "caught_stealing": 0,
                "walks": 0,
                "strikeouts": 0
            }
            
            for season in stats_list:
                for key in totals:
                    totals[key] += season.get(key, 0)
            
            # Calculate averages
            if totals["at_bats"] > 0:
                totals["batting_average"] = totals["hits"] / totals["at_bats"]
            else:
                totals["batting_average"] = 0.0
            
            if totals["plate_appearances"] > 0:
                totals["on_base_percentage"] = (
                    (totals["hits"] + totals["walks"]) / totals["plate_appearances"]
                )
            else:
                totals["on_base_percentage"] = 0.0
            
            if totals["at_bats"] > 0:
                total_bases = (
                    totals["hits"] + totals["doubles"] + 
                    (totals["triples"] * 2) + (totals["home_runs"] * 3)
                )
                totals["slugging_percentage"] = total_bases / totals["at_bats"]
            else:
                totals["slugging_percentage"] = 0.0
            
            totals["ops"] = totals["on_base_percentage"] + totals["slugging_percentage"]
            
        elif stats_type == "pitching":
            totals = {
                "games": 0,
                "games_started": 0,
                "complete_games": 0,
                "shutouts": 0,
                "wins": 0,
                "losses": 0,
                "saves": 0,
                "innings_pitched": 0.0,
                "hits_allowed": 0,
                "runs_allowed": 0,
                "earned_runs": 0,
                "home_runs_allowed": 0,
                "walks": 0,
                "strikeouts": 0
            }
            
            for season in stats_list:
                for key in totals:
                    totals[key] += season.get(key, 0)
            
            # Calculate rates
            if totals["innings_pitched"] > 0:
                totals["era"] = (totals["earned_runs"] * 9) / totals["innings_pitched"]
                totals["whip"] = (
                    (totals["hits_allowed"] + totals["walks"]) / totals["innings_pitched"]
                )
                totals["strikeouts_per_nine"] = (totals["strikeouts"] * 9) / totals["innings_pitched"]
                totals["walks_per_nine"] = (totals["walks"] * 9) / totals["innings_pitched"]
            else:
                totals["era"] = 0.0
                totals["whip"] = 0.0
                totals["strikeouts_per_nine"] = 0.0
                totals["walks_per_nine"] = 0.0
        
        else:
            totals = {}
        
        return totals