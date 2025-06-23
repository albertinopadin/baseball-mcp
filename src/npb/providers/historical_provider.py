"""Historical data provider for NPB statistics."""

import logging
from typing import Optional, List, Dict, Any

from .base import NPBDataProvider
from ..data.database import NPBDatabase
from ..data.historical_data import populate_test_data
from ..data.metrics.calculator import NPBMetricsCalculator

logger = logging.getLogger(__name__)


class HistoricalDataProvider(NPBDataProvider):
    """Provider for historical NPB data from local database."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize historical data provider.
        
        Args:
            db_path: Path to SQLite database. If None, uses default location.
        """
        self.db = NPBDatabase(db_path)
        
        # Check if database needs initial population
        self._ensure_data_populated()
    
    def _ensure_data_populated(self):
        """Ensure the database has some data."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM players")
            count = cursor.fetchone()[0]
            
            if count == 0:
                logger.info("Populating database with test data...")
                populate_test_data(self.db)
                logger.info("Test data populated successfully")
    
    async def search_player(self, name: str) -> List[Dict[str, Any]]:
        """Search for players by name in historical database.
        
        Args:
            name: Player name to search for
            
        Returns:
            List of player dictionaries
        """
        results = []
        
        # Search in database
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Search by name (case-insensitive, partial match)
            search_pattern = f"%{name}%"
            cursor.execute("""
                SELECT player_id, name_english, name_japanese, name_romanized_variants
                FROM players
                WHERE LOWER(name_english) LIKE LOWER(?)
                   OR LOWER(name_romanized_variants) LIKE LOWER(?)
                ORDER BY name_english
            """, (search_pattern, search_pattern))
            
            for row in cursor.fetchall():
                player = dict(row)
                
                # Parse romanized variants
                import json
                if player.get('name_romanized_variants'):
                    try:
                        variants = json.loads(player['name_romanized_variants'])
                        # Check if any variant matches
                        for variant in variants:
                            if name.lower() in variant.lower():
                                player['matched_variant'] = variant
                                break
                    except:
                        pass
                
                # Get years active
                cursor.execute("""
                    SELECT MIN(season) as first_year, MAX(season) as last_year
                    FROM (
                        SELECT season FROM batting_stats WHERE player_id = ?
                        UNION
                        SELECT season FROM pitching_stats WHERE player_id = ?
                    )
                """, (player['player_id'], player['player_id']))
                
                years = cursor.fetchone()
                if years and years['first_year']:
                    player['years_active'] = f"{years['first_year']}-{years['last_year']}"
                
                # Determine position
                cursor.execute("""
                    SELECT COUNT(*) as batting_count FROM batting_stats WHERE player_id = ?
                """, (player['player_id'],))
                batting_count = cursor.fetchone()['batting_count']
                
                cursor.execute("""
                    SELECT COUNT(*) as pitching_count FROM pitching_stats WHERE player_id = ?
                """, (player['player_id'],))
                pitching_count = cursor.fetchone()['pitching_count']
                
                if pitching_count > 0 and batting_count == 0:
                    player['position'] = "Pitcher"
                elif batting_count > 0 and pitching_count == 0:
                    player['position'] = "Position Player"
                elif batting_count > 0 and pitching_count > 0:
                    player['position'] = "Two-way Player"
                
                results.append({
                    'id': player['player_id'],
                    'name_english': player['name_english'],
                    'name_japanese': player.get('name_japanese'),
                    'years_active': player.get('years_active'),
                    'position': player.get('position', 'Unknown')
                })
        
        return results
    
    async def get_player_stats(
        self, 
        player_id: str, 
        season: Optional[int] = None,
        stats_type: str = "season"
    ) -> Dict[str, Any]:
        """Get player statistics from historical database.
        
        Args:
            player_id: Unique player identifier
            season: Season year (None for career)
            stats_type: Type of stats ("season" or "career")
            
        Returns:
            Dictionary with player stats
        """
        # Get player info
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM players WHERE player_id = ?", (player_id,))
            player_row = cursor.fetchone()
            
            if not player_row:
                return {"error": f"Player {player_id} not found in historical database"}
            
            player_info = dict(player_row)
        
        # Get stats
        batting_stats = self.db.get_player_batting_stats(player_id, season)
        pitching_stats = self.db.get_player_pitching_stats(player_id, season)
        
        # Determine primary stat type
        if batting_stats and not pitching_stats:
            stats_type_result = "batting"
            stats = batting_stats
        elif pitching_stats and not batting_stats:
            stats_type_result = "pitching"
            stats = pitching_stats
        elif batting_stats and pitching_stats:
            # Two-way player - return batting by default
            stats_type_result = "batting"
            stats = batting_stats
        else:
            return {
                "error": f"No statistics found for player {player_id}",
                "player_info": {
                    "name_english": player_info.get('name_english'),
                    "name_japanese": player_info.get('name_japanese')
                }
            }
        
        # Enhance stats with calculated metrics
        calculator = NPBMetricsCalculator()
        enhanced_stats = []
        for stat in stats:
            if stats_type_result == "batting":
                enhanced_stat = calculator.enhance_batting_stats(stat)
            else:
                enhanced_stat = calculator.enhance_pitching_stats(stat)
            enhanced_stats.append(enhanced_stat)
        
        # Format response
        response = {
            "player_id": player_id,
            "player_info": {
                "name_english": player_info.get('name_english'),
                "name_japanese": player_info.get('name_japanese'),
                "birth_date": player_info.get('birth_date'),
                "bats": player_info.get('bats'),
                "throws": player_info.get('throws'),
                "height": player_info.get('height'),
                "weight": player_info.get('weight')
            },
            "stats_type": stats_type_result,
            "stats": enhanced_stats
        }
        
        # Add career totals if no specific season requested
        if not season and len(stats) > 0:
            career_totals = self.db.get_player_career_totals(player_id, stats_type_result)
            if career_totals:
                response["career_totals"] = career_totals
        
        return response
    
    async def get_team_roster(
        self, 
        team_id: str, 
        season: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get team roster from historical database.
        
        Args:
            team_id: Team identifier
            season: Season year (None for all time)
            
        Returns:
            List of player dictionaries on the roster
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            if season:
                # Get players who played for this team in specific season
                query = """
                    SELECT DISTINCT p.player_id, p.name_english, p.name_japanese,
                           CASE 
                               WHEN ps.player_id IS NOT NULL THEN 'Pitcher'
                               ELSE 'Position Player'
                           END as position
                    FROM players p
                    LEFT JOIN batting_stats bs ON p.player_id = bs.player_id 
                        AND bs.team_id = ? AND bs.season = ?
                    LEFT JOIN pitching_stats ps ON p.player_id = ps.player_id 
                        AND ps.team_id = ? AND ps.season = ?
                    WHERE bs.player_id IS NOT NULL OR ps.player_id IS NOT NULL
                    ORDER BY p.name_english
                """
                cursor.execute(query, (team_id, season, team_id, season))
            else:
                # Get all players who ever played for this team
                query = """
                    SELECT DISTINCT p.player_id, p.name_english, p.name_japanese,
                           MIN(COALESCE(bs.season, ps.season)) as first_year,
                           MAX(COALESCE(bs.season, ps.season)) as last_year,
                           CASE 
                               WHEN COUNT(ps.season) > 0 AND COUNT(bs.season) = 0 THEN 'Pitcher'
                               WHEN COUNT(bs.season) > 0 AND COUNT(ps.season) = 0 THEN 'Position Player'
                               ELSE 'Two-way Player'
                           END as position
                    FROM players p
                    LEFT JOIN batting_stats bs ON p.player_id = bs.player_id AND bs.team_id = ?
                    LEFT JOIN pitching_stats ps ON p.player_id = ps.player_id AND ps.team_id = ?
                    WHERE bs.player_id IS NOT NULL OR ps.player_id IS NOT NULL
                    GROUP BY p.player_id
                    ORDER BY p.name_english
                """
                cursor.execute(query, (team_id, team_id))
            
            roster = []
            for row in cursor.fetchall():
                player = dict(row)
                roster.append({
                    "id": player['player_id'],
                    "name_english": player['name_english'],
                    "name_japanese": player.get('name_japanese'),
                    "position": player['position'],
                    "years_with_team": f"{player.get('first_year', '')}-{player.get('last_year', '')}" if player.get('first_year') else None
                })
            
            return roster
    
    async def get_standings(
        self, 
        league: Optional[str] = None,
        season: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get league standings (not available for historical data).
        
        Historical standings data is not currently available in the database.
        
        Args:
            league: "central", "pacific", or None for both
            season: Season year
            
        Returns:
            Dictionary indicating standings are not available
        """
        return {
            "error": "Historical standings data is not available in the current database.",
            "message": "Standings are only available for recent seasons through web scraping."
        }
    
    async def get_teams(self) -> List[Dict[str, Any]]:
        """Get all NPB teams from the database.
        
        Returns:
            List of team dictionaries
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT team_id as id, name_english, name_japanese, 
                       abbreviation, league, city
                FROM teams
                ORDER BY league, name_english
            """)
            
            teams = []
            for row in cursor.fetchall():
                team = dict(row)
                # Normalize league name to lowercase
                if team.get('league'):
                    team['league'] = team['league'].lower()
                teams.append(team)
            
            return teams