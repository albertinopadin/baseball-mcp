"""NPB Official website data source implementation."""

import re
from typing import List, Optional, Dict, Any
from datetime import datetime
import httpx
from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ..base import AbstractNPBDataSource
from ..models import NPBPlayer, NPBPlayerStats, NPBTeam, NPBLeague
from ..name_utils import normalize_name, match_name, generate_name_variants
from . import register_source
from cache_utils import cache_result


@register_source("npb_official")
class NPBOfficialSource(AbstractNPBDataSource):
    """Data source for official NPB website (npb.jp)."""
    
    def __init__(self):
        """Initialize NPB Official source."""
        super().__init__(
            base_url="https://npb.jp/bis/eng",
            cache_ttl=86400  # 24 hours
        )
        self.current_year = datetime.now().year
        
        # Team mappings for NPB official site
        self.team_mappings = {
            # Central League
            "G": ("Giants", "Yomiuri Giants", NPBLeague.CENTRAL),
            "T": ("Tigers", "Hanshin Tigers", NPBLeague.CENTRAL),
            "C": ("Carp", "Hiroshima Toyo Carp", NPBLeague.CENTRAL),
            "D": ("Dragons", "Chunichi Dragons", NPBLeague.CENTRAL),
            "DB": ("BayStars", "Yokohama DeNA BayStars", NPBLeague.CENTRAL),
            "S": ("Swallows", "Tokyo Yakult Swallows", NPBLeague.CENTRAL),
            # Pacific League
            "H": ("Hawks", "Fukuoka SoftBank Hawks", NPBLeague.PACIFIC),
            "M": ("Marines", "Chiba Lotte Marines", NPBLeague.PACIFIC),
            "L": ("Lions", "Saitama Seibu Lions", NPBLeague.PACIFIC),
            "E": ("Eagles", "Tohoku Rakuten Golden Eagles", NPBLeague.PACIFIC),
            "F": ("Fighters", "Hokkaido Nippon-Ham Fighters", NPBLeague.PACIFIC),
            "B": ("Buffaloes", "Orix Buffaloes", NPBLeague.PACIFIC),
        }
    
    async def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse an HTML page.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers={
                        "User-Agent": "baseball-mcp-server/1.0",
                        "Accept-Language": "en-US,en;q=0.9"
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def _normalize_name(self, name: str) -> str:
        """Normalize player name for searching.
        
        Args:
            name: Player name
            
        Returns:
            Normalized name
        """
        # Use the improved normalization from name_utils
        return normalize_name(name)
    
    def _parse_player_from_stats_row(self, row, team_abbr: str) -> Optional[NPBPlayer]:
        """Parse player information from a stats table row.
        
        Args:
            row: BeautifulSoup row element
            team_abbr: Team abbreviation
            
        Returns:
            NPBPlayer object or None
        """
        try:
            cells = row.find_all('td')
            if len(cells) < 3:
                return None
            
            # Extract player name (usually in first or second cell)
            name_cell = cells[1] if cells[0].text.strip().isdigit() else cells[0]
            name = name_cell.text.strip()
            
            if not name or name == "Player":
                return None
            
            # Extract jersey number if available
            jersey_number = None
            if cells[0].text.strip().isdigit():
                jersey_number = cells[0].text.strip()
            
            # Get team info
            team_info = self.team_mappings.get(team_abbr)
            team = None
            if team_info:
                team = NPBTeam(
                    id=f"npb_{team_abbr}",
                    name_english=team_info[1],
                    abbreviation=team_abbr,
                    league=team_info[2],
                    source="npb_official",
                    source_id=team_abbr
                )
            
            # Create player object
            player_id = f"npb_{name.lower().replace(' ', '_')}_{team_abbr}"
            return NPBPlayer(
                id=player_id,
                name_english=name,
                team=team,
                jersey_number=jersey_number,
                source="npb_official",
                source_id=player_id
            )
            
        except Exception as e:
            print(f"Error parsing player row: {e}")
            return None
    
    async def search_player(self, name: str) -> List[NPBPlayer]:
        """Search for players by name.
        
        Args:
            name: Player name to search for
            
        Returns:
            List of matching players
        """
        players = []
        found_players = set()  # Track found players to avoid duplicates
        
        # Search in current season first, then previous if needed
        for year in [self.current_year, self.current_year - 1]:
            # Parse both Central and Pacific league batting stats
            for league, league_code in [("Central", "c"), ("Pacific", "p")]:
                batting_url = f"{self.base_url}/{year}/stats/bat_{league_code}.html"
                players_in_league = await self._parse_batting_stats_page(
                    batting_url, name, year, league  # Pass original name, not normalized
                )
                
                # Add unique players only
                for player in players_in_league:
                    if player.id not in found_players:
                        found_players.add(player.id)
                        players.append(player)
            
            # If we found the player, no need to check previous year
            if players:
                break
        
        return players
    
    @cache_result(ttl_hours=24)
    async def _parse_batting_stats_page(
        self, url: str, search_name: str, year: int, league: str
    ) -> List[NPBPlayer]:
        """Parse a batting stats page for players.
        
        Args:
            url: URL of the batting stats page
            search_name: Normalized player name to search for
            year: Season year
            league: League name (Central or Pacific)
            
        Returns:
            List of matching players
        """
        page = await self._fetch_page(url)
        if not page:
            return []
        
        players = []
        
        # Find the main stats table (NPB site uses tables without classes)
        tables = page.find_all('table')
        
        # The stats table is usually the first large table
        for table in tables:
            rows = table.find_all('tr')
            
            # Skip if too few rows
            if len(rows) < 5:
                continue
            
            # Check if this is a stats table by looking at headers
            header_row = rows[0]
            headers = header_row.find_all(['td', 'th'])
            
            # Look for batting stats headers
            header_text = ' '.join([h.text.strip() for h in headers])
            if not any(stat in header_text for stat in ['AVG', 'G', 'PA', 'AB']):
                continue
            
            # Process data rows
            for row in rows[1:]:
                cells = row.find_all(['td'])
                if len(cells) < 10:  # Need enough columns for stats
                    continue
                
                # NPB stats table format: Rank, Player, AVG, G, PA, AB...
                # Player name is in column 1 (index 1)
                if len(cells) < 2:
                    continue
                    
                player_name = cells[1].text.strip()
                
                # Skip if not a valid player name
                if not player_name or player_name == "Player" or player_name.isdigit():
                    continue
                
                # Check if this player matches our search
                if not match_name(search_name, player_name):
                    continue
                
                # Extract team - NPB format has team abbreviation in parentheses in column 2
                team_abbr = None
                if len(cells) > 2:
                    team_cell = cells[2].text.strip()
                    # Remove parentheses
                    if team_cell.startswith('(') and team_cell.endswith(')'):
                        team_abbr = team_cell[1:-1]
                    elif team_cell in self.team_mappings:
                        team_abbr = team_cell
                
                # Create team object if we found team info
                team = None
                if team_abbr and team_abbr in self.team_mappings:
                    team_info = self.team_mappings[team_abbr]
                    team = NPBTeam(
                        id=f"npb_{team_abbr}",
                        name_english=team_info[1],
                        abbreviation=team_abbr,
                        league=NPBLeague.CENTRAL if league == "Central" else NPBLeague.PACIFIC,
                        source="npb_official",
                        source_id=team_abbr
                    )
                
                # Extract jersey number if available
                jersey_number = None
                if cells[0].text.strip().isdigit():
                    jersey_number = cells[0].text.strip()
                
                # Create player object
                player_id = f"npb_{player_name.lower().replace(' ', '_')}_{year}"
                player = NPBPlayer(
                    id=player_id,
                    name_english=player_name,
                    team=team,
                    jersey_number=jersey_number,
                    source="npb_official",
                    source_id=player_id
                )
                
                players.append(player)
        
        return players
    
    def _extract_team_from_table(self, table) -> Optional[str]:
        """Extract team abbreviation from a stats table.
        
        Args:
            table: BeautifulSoup table element
            
        Returns:
            Team abbreviation or None
        """
        # Look for team info in table caption or nearby elements
        # This is a simplified version - actual implementation would need
        # to handle the specific HTML structure of NPB site
        return None  # Placeholder
    
    async def get_player_stats(
        self,
        player_id: str,
        season: Optional[int] = None,
        stats_type: str = "batting"
    ) -> Optional[NPBPlayerStats]:
        """Get player statistics.
        
        Args:
            player_id: Player ID
            season: Season year
            stats_type: "batting" or "pitching"
            
        Returns:
            Player statistics or None
        """
        # Extract player name from ID for searching
        # ID format: npb_firstname_lastname_year
        parts = player_id.replace("npb_", "").rsplit("_", 1)
        if len(parts) < 2:
            return None
        
        player_name = parts[0].replace("_", " ")
        year = season or self.current_year
        
        # Search both leagues
        for league, league_code in [("Central", "c"), ("Pacific", "p")]:
            if stats_type == "batting":
                url = f"{self.base_url}/{year}/stats/bat_{league_code}.html"
            else:
                url = f"{self.base_url}/{year}/stats/pit_{league_code}.html"
            
            stats = await self._parse_stats_from_page(
                url, player_name, year, league, stats_type
            )
            
            if stats:
                return stats
        
        return None
    
    @cache_result(ttl_hours=24)
    async def _parse_stats_from_page(
        self, url: str, player_name: str, year: int, league: str, stats_type: str
    ) -> Optional[NPBPlayerStats]:
        """Parse player statistics from a stats page.
        
        Args:
            url: URL of the stats page
            player_name: Player name to search for
            year: Season year
            league: League name
            stats_type: "batting" or "pitching"
            
        Returns:
            Player statistics or None
        """
        page = await self._fetch_page(url)
        if not page:
            return None
        
        normalized_search = self._normalize_name(player_name)
        
        # Find stats tables
        tables = page.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            
            # Find header row to map column indices
            header_row = None
            for row in rows:
                headers = row.find_all(['th'])
                if len(headers) > 10:  # Stats table should have many columns
                    header_row = headers
                    break
            
            if not header_row:
                continue
            
            # Map column names to indices
            col_map = {}
            for i, header in enumerate(header_row):
                col_text = header.text.strip().upper()
                col_map[col_text] = i
            
            # Parse data rows
            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 10:
                    continue
                
                # Find player name
                player_cell = None
                for i in range(1, min(4, len(cells))):
                    cell_text = cells[i].text.strip()
                    if cell_text and not cell_text.isdigit():
                        if self._normalize_name(cell_text) == normalized_search:
                            player_cell = cells[i]
                            break
                
                if not player_cell:
                    continue
                
                # Extract team
                team = None
                team_abbr = None
                for cell in cells[:5]:
                    text = cell.text.strip()
                    if text in self.team_mappings:
                        team_abbr = text
                        team_info = self.team_mappings[team_abbr]
                        team = NPBTeam(
                            id=f"npb_{team_abbr}",
                            name_english=team_info[1],
                            abbreviation=team_abbr,
                            league=NPBLeague.CENTRAL if league == "Central" else NPBLeague.PACIFIC,
                            source="npb_official",
                            source_id=team_abbr
                        )
                        break
                
                # Parse statistics based on type
                if stats_type == "batting":
                    stats = self._parse_batting_stats(cells, col_map)
                else:
                    stats = self._parse_pitching_stats(cells, col_map)
                
                # Create stats object
                player_stats = NPBPlayerStats(
                    player_id=f"npb_{player_name.lower().replace(' ', '_')}_{year}",
                    season=year,
                    stats_type=stats_type,
                    team=team,
                    source="npb_official",
                    **stats
                )
                
                return player_stats
        
        return None
    
    def _parse_batting_stats(self, cells: list, col_map: dict) -> dict:
        """Parse batting statistics from table cells."""
        stats = {}
        
        # Helper to safely get cell value
        def get_stat(col_name, default=None, is_float=False):
            if col_name in col_map and col_map[col_name] < len(cells):
                try:
                    val = cells[col_map[col_name]].text.strip()
                    if val == "-" or not val:
                        return default
                    return float(val) if is_float else int(val)
                except (ValueError, IndexError):
                    return default
            return default
        
        # Traditional batting stats
        stats['games'] = get_stat('G') or get_stat('GP')
        stats['plate_appearances'] = get_stat('PA')
        stats['at_bats'] = get_stat('AB')
        stats['runs'] = get_stat('R')
        stats['hits'] = get_stat('H')
        stats['doubles'] = get_stat('2B')
        stats['triples'] = get_stat('3B')
        stats['home_runs'] = get_stat('HR')
        stats['rbi'] = get_stat('RBI')
        stats['stolen_bases'] = get_stat('SB')
        stats['caught_stealing'] = get_stat('CS')
        stats['walks'] = get_stat('BB')
        stats['strikeouts'] = get_stat('SO') or get_stat('K')
        stats['batting_average'] = get_stat('AVG', is_float=True) or get_stat('BA', is_float=True)
        stats['on_base_percentage'] = get_stat('OBP', is_float=True)
        stats['slugging_percentage'] = get_stat('SLG', is_float=True)
        stats['ops'] = get_stat('OPS', is_float=True)
        
        return stats
    
    def _parse_pitching_stats(self, cells: list, col_map: dict) -> dict:
        """Parse pitching statistics from table cells."""
        stats = {}
        
        # Helper to safely get cell value
        def get_stat(col_name, default=None, is_float=False):
            if col_name in col_map and col_map[col_name] < len(cells):
                try:
                    val = cells[col_map[col_name]].text.strip()
                    if val == "-" or not val:
                        return default
                    return float(val) if is_float else int(val)
                except (ValueError, IndexError):
                    return default
            return default
        
        # Traditional pitching stats
        stats['games'] = get_stat('G') or get_stat('GP')
        stats['wins'] = get_stat('W')
        stats['losses'] = get_stat('L')
        stats['saves'] = get_stat('SV') or get_stat('S')
        stats['holds'] = get_stat('HLD') or get_stat('H')
        stats['innings_pitched'] = get_stat('IP', is_float=True)
        stats['hits_allowed'] = get_stat('H')
        stats['runs_allowed'] = get_stat('R')
        stats['earned_runs'] = get_stat('ER')
        stats['home_runs_allowed'] = get_stat('HR')
        stats['walks_allowed'] = get_stat('BB')
        stats['strikeouts_pitched'] = get_stat('SO') or get_stat('K')
        stats['era'] = get_stat('ERA', is_float=True)
        stats['whip'] = get_stat('WHIP', is_float=True)
        
        return stats
    
    async def get_teams(self, season: Optional[int] = None) -> List[NPBTeam]:
        """Get all NPB teams.
        
        Args:
            season: Season year
            
        Returns:
            List of NPB teams
        """
        teams = []
        
        for abbr, (short_name, full_name, league) in self.team_mappings.items():
            team = NPBTeam(
                id=f"npb_{abbr}",
                name_english=full_name,
                abbreviation=abbr,
                league=league,
                source="npb_official",
                source_id=abbr
            )
            teams.append(team)
        
        return teams
    
    async def get_team_roster(
        self,
        team_id: str,
        season: Optional[int] = None
    ) -> List[NPBPlayer]:
        """Get team roster.
        
        Args:
            team_id: Team ID
            season: Season year
            
        Returns:
            List of players on the team
        """
        # TODO: Implement roster fetching
        # This would involve navigating to team-specific pages
        return []
    
    async def health_check(self) -> bool:
        """Check if NPB official site is accessible.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            test_url = f"{self.base_url}/{self.current_year}/stats/"
            page = await self._fetch_page(test_url)
            return page is not None
        except Exception:
            return False