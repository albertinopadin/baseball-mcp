"""NPB Historical Database Manager."""

import sqlite3
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class NPBDatabase:
    """Manages the NPB historical SQLite database."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize the database manager.
        
        Args:
            db_path: Path to the SQLite database file. 
                    Defaults to src/npb/data/npb_historical.db
        """
        if db_path is None:
            self.db_path = Path(__file__).parent / "npb_historical.db"
        else:
            self.db_path = Path(db_path)
        
        # Ensure directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with schema."""
        schema_path = Path(__file__).parent / "schema.sql"
        
        if not schema_path.exists():
            logger.error(f"Schema file not found: {schema_path}")
            return
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Read and execute schema
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            
            cursor.executescript(schema_sql)
            conn.commit()
            
        logger.info(f"Database initialized at {self.db_path}")
    
    @contextmanager
    def get_connection(self):
        """Get a database connection context manager."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()
    
    def insert_player(self, player_data: Dict[str, Any]) -> Optional[str]:
        """Insert or update a player record.
        
        Args:
            player_data: Dictionary with player information
            
        Returns:
            Player ID if successful, None otherwise
        """
        required_fields = ['player_id', 'name_english']
        if not all(field in player_data for field in required_fields):
            logger.error(f"Missing required fields. Required: {required_fields}")
            return None
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Handle name variants as JSON
            if 'name_romanized_variants' in player_data and isinstance(player_data['name_romanized_variants'], list):
                player_data['name_romanized_variants'] = json.dumps(player_data['name_romanized_variants'])
            
            # Prepare fields and values
            fields = list(player_data.keys())
            placeholders = ['?' for _ in fields]
            values = [player_data[field] for field in fields]
            
            # Use INSERT OR REPLACE to handle updates
            query = f"""
                INSERT OR REPLACE INTO players ({', '.join(fields)})
                VALUES ({', '.join(placeholders)})
            """
            
            try:
                cursor.execute(query, values)
                conn.commit()
                logger.debug(f"Inserted/updated player: {player_data['player_id']}")
                return player_data['player_id']
            except sqlite3.Error as e:
                logger.error(f"Error inserting player: {e}")
                conn.rollback()
                return None
    
    def insert_batting_stats(self, stats_data: Dict[str, Any]) -> bool:
        """Insert or update batting statistics.
        
        Args:
            stats_data: Dictionary with batting statistics
            
        Returns:
            True if successful, False otherwise
        """
        required_fields = ['player_id', 'season', 'data_source']
        if not all(field in stats_data for field in required_fields):
            logger.error(f"Missing required fields. Required: {required_fields}")
            return False
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Calculate derived stats if not provided
            if 'at_bats' in stats_data and stats_data['at_bats'] > 0:
                if 'batting_average' not in stats_data and 'hits' in stats_data:
                    stats_data['batting_average'] = round(stats_data['hits'] / stats_data['at_bats'], 3)
                
                if 'slugging_percentage' not in stats_data and all(k in stats_data for k in ['hits', 'doubles', 'triples', 'home_runs']):
                    total_bases = stats_data['hits'] + stats_data['doubles'] + (2 * stats_data['triples']) + (3 * stats_data['home_runs'])
                    stats_data['slugging_percentage'] = round(total_bases / stats_data['at_bats'], 3)
            
            # Calculate OBP if possible
            if all(k in stats_data for k in ['hits', 'walks', 'hit_by_pitch', 'at_bats', 'sacrifice_flies']):
                pa_denominator = stats_data['at_bats'] + stats_data['walks'] + stats_data['hit_by_pitch'] + stats_data['sacrifice_flies']
                if pa_denominator > 0:
                    stats_data['on_base_percentage'] = round(
                        (stats_data['hits'] + stats_data['walks'] + stats_data['hit_by_pitch']) / pa_denominator, 3
                    )
            
            # Calculate OPS
            if 'on_base_percentage' in stats_data and 'slugging_percentage' in stats_data:
                stats_data['ops'] = round(stats_data['on_base_percentage'] + stats_data['slugging_percentage'], 3)
            
            # Prepare fields and values
            fields = list(stats_data.keys())
            placeholders = ['?' for _ in fields]
            values = [stats_data[field] for field in fields]
            
            # Use INSERT OR REPLACE
            query = f"""
                INSERT OR REPLACE INTO batting_stats ({', '.join(fields)})
                VALUES ({', '.join(placeholders)})
            """
            
            try:
                cursor.execute(query, values)
                conn.commit()
                logger.debug(f"Inserted batting stats for {stats_data['player_id']} ({stats_data['season']})")
                return True
            except sqlite3.Error as e:
                logger.error(f"Error inserting batting stats: {e}")
                conn.rollback()
                return False
    
    def insert_pitching_stats(self, stats_data: Dict[str, Any]) -> bool:
        """Insert or update pitching statistics.
        
        Args:
            stats_data: Dictionary with pitching statistics
            
        Returns:
            True if successful, False otherwise
        """
        required_fields = ['player_id', 'season', 'data_source']
        if not all(field in stats_data for field in required_fields):
            logger.error(f"Missing required fields. Required: {required_fields}")
            return False
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Calculate WHIP if not provided
            if 'innings_pitched' in stats_data and stats_data['innings_pitched'] > 0:
                if 'whip' not in stats_data and all(k in stats_data for k in ['hits_allowed', 'walks']):
                    stats_data['whip'] = round(
                        (stats_data['hits_allowed'] + stats_data['walks']) / stats_data['innings_pitched'], 3
                    )
                
                # Calculate K/9 and BB/9
                if 'strikeouts' in stats_data:
                    stats_data['strikeouts_per_nine'] = round((stats_data['strikeouts'] * 9) / stats_data['innings_pitched'], 1)
                if 'walks' in stats_data:
                    stats_data['walks_per_nine'] = round((stats_data['walks'] * 9) / stats_data['innings_pitched'], 1)
            
            # Prepare fields and values
            fields = list(stats_data.keys())
            placeholders = ['?' for _ in fields]
            values = [stats_data[field] for field in fields]
            
            # Use INSERT OR REPLACE
            query = f"""
                INSERT OR REPLACE INTO pitching_stats ({', '.join(fields)})
                VALUES ({', '.join(placeholders)})
            """
            
            try:
                cursor.execute(query, values)
                conn.commit()
                logger.debug(f"Inserted pitching stats for {stats_data['player_id']} ({stats_data['season']})")
                return True
            except sqlite3.Error as e:
                logger.error(f"Error inserting pitching stats: {e}")
                conn.rollback()
                return False
    
    def get_player_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a player by name (handles romanization variants).
        
        Args:
            name: Player name to search for
            
        Returns:
            Player record if found, None otherwise
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # First try exact match
            cursor.execute(
                "SELECT * FROM players WHERE LOWER(name_english) = LOWER(?)",
                (name,)
            )
            result = cursor.fetchone()
            
            if result:
                return dict(result)
            
            # Try fuzzy match
            cursor.execute(
                "SELECT * FROM players WHERE LOWER(name_english) LIKE LOWER(?)",
                (f"%{name}%",)
            )
            results = cursor.fetchall()
            
            if results:
                # If multiple matches, try to find best match
                for row in results:
                    player = dict(row)
                    # Check romanized variants
                    if player.get('name_romanized_variants'):
                        variants = json.loads(player['name_romanized_variants'])
                        if any(name.lower() in variant.lower() for variant in variants):
                            return player
                
                # Return first match if no variant match
                return dict(results[0])
            
            return None
    
    def get_player_batting_stats(self, player_id: str, season: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get batting statistics for a player.
        
        Args:
            player_id: Player ID
            season: Optional specific season
            
        Returns:
            List of batting statistics
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if season:
                cursor.execute(
                    "SELECT * FROM batting_stats WHERE player_id = ? AND season = ? ORDER BY season",
                    (player_id, season)
                )
            else:
                cursor.execute(
                    "SELECT * FROM batting_stats WHERE player_id = ? ORDER BY season",
                    (player_id,)
                )
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_player_pitching_stats(self, player_id: str, season: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get pitching statistics for a player.
        
        Args:
            player_id: Player ID
            season: Optional specific season
            
        Returns:
            List of pitching statistics
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if season:
                cursor.execute(
                    "SELECT * FROM pitching_stats WHERE player_id = ? AND season = ? ORDER BY season",
                    (player_id, season)
                )
            else:
                cursor.execute(
                    "SELECT * FROM pitching_stats WHERE player_id = ? ORDER BY season",
                    (player_id,)
                )
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_player_career_totals(self, player_id: str, stats_type: str = "batting") -> Optional[Dict[str, Any]]:
        """Get career totals for a player.
        
        Args:
            player_id: Player ID
            stats_type: "batting" or "pitching"
            
        Returns:
            Career totals if found
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if stats_type == "batting":
                cursor.execute(
                    "SELECT * FROM batting_career_totals WHERE player_id = ?",
                    (player_id,)
                )
            else:
                cursor.execute(
                    "SELECT * FROM pitching_career_totals WHERE player_id = ?",
                    (player_id,)
                )
            
            result = cursor.fetchone()
            return dict(result) if result else None