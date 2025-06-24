"""FanGraphs NPB data source implementation for advanced metrics."""

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
from ..name_utils import normalize_name, match_name
from . import register_source
from cache_utils import cache_result


@register_source("fangraphs")
class FanGraphsNPBSource(AbstractNPBDataSource):
    """Data source for FanGraphs NPB statistics (advanced metrics)."""
    
    def __init__(self):
        """Initialize FanGraphs NPB source."""
        super().__init__(
            base_url="https://www.fangraphs.com",
            cache_ttl=43200  # 12 hours
        )
        self.current_year = datetime.now().year
    
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
                        "Accept": "text/html,application/xhtml+xml"
                    },
                    timeout=30.0,
                    follow_redirects=True
                )
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    async def search_player(self, name: str) -> List[NPBPlayer]:
        """Search for NPB players by name on FanGraphs.
        
        Args:
            name: Player name to search for
            
        Returns:
            List of matching players
        """
        # FanGraphs NPB leaderboard URL
        url = f"{self.base_url}/leaders/international/npb"
        
        players = await self._parse_leaderboard(url, name)
        return players
    
    @cache_result(ttl_hours=12)
    async def _parse_leaderboard(self, url: str, search_name: str) -> List[NPBPlayer]:
        """Parse FanGraphs NPB leaderboard for players.
        
        Args:
            url: Leaderboard URL
            search_name: Player name to search for
            
        Returns:
            List of matching players
        """
        page = await self._fetch_page(url)
        if not page:
            return []
        
        players = []
        
        # Find the leaderboard table
        table = page.find('table', {'class': 'rgMasterTable'})
        if not table:
            # Try alternative table classes
            table = page.find('table', {'id': 'LeaderBoard1_dg1'})
        
        if not table:
            return []
        
        rows = table.find_all('tr', {'class': ['rgRow', 'rgAltRow']})
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 3:
                continue
            
            # Player name is usually in the second column with a link
            player_link = None
            player_name = None
            
            for i in range(1, min(4, len(cells))):
                link = cells[i].find('a')
                if link and '/players/' in link.get('href', ''):
                    player_link = link
                    player_name = link.text.strip()
                    break
            
            if not player_name:
                continue
            
            # Check if this player matches our search
            if not match_name(search_name, player_name):
                continue
            
            # Extract player ID from URL
            player_id = None
            if player_link:
                href = player_link.get('href', '')
                # Extract ID from URL like /players/munetaka-murakami/sa3063258/stats
                id_match = re.search(r'/players/[^/]+/([^/]+)', href)
                if id_match:
                    player_id = id_match.group(1)
            
            # Create player object
            player = NPBPlayer(
                id=f"fg_{player_id}" if player_id else f"fg_{normalize_name(player_name)}",
                name_english=player_name,
                source="fangraphs",
                source_id=player_id or player_name
            )
            
            players.append(player)
        
        return players
    
    async def get_player_stats(
        self,
        player_id: str,
        season: Optional[int] = None,
        stats_type: str = "batting"
    ) -> Optional[NPBPlayerStats]:
        """Get player statistics with advanced metrics from FanGraphs.
        
        Args:
            player_id: Player ID (FanGraphs format)
            season: Season year
            stats_type: "batting" or "pitching"
            
        Returns:
            Player statistics with advanced metrics
        """
        # Clean up player ID
        if player_id.startswith('fg_'):
            player_id = player_id[3:]
        elif player_id.startswith('npb_'):
            # Can't use NPB IDs directly with FanGraphs
            return None
        
        # For FanGraphs, we need to fetch the player page
        # This is a simplified version - real implementation would need
        # to handle player page parsing
        return await self._fetch_player_stats(player_id, season, stats_type)
    
    @cache_result(ttl_hours=12)
    async def _fetch_player_stats(
        self,
        player_id: str,
        season: Optional[int],
        stats_type: str
    ) -> Optional[NPBPlayerStats]:
        """Fetch player stats from their FanGraphs page.
        
        Args:
            player_id: FanGraphs player ID
            season: Season year
            stats_type: Stats type
            
        Returns:
            Player stats with advanced metrics
        """
        # This is a placeholder - actual implementation would:
        # 1. Construct player page URL
        # 2. Parse the stats table
        # 3. Extract advanced metrics like WAR, wRC+, FIP, etc.
        
        # For now, return None as this requires more complex parsing
        return None
    
    async def get_teams(self, season: Optional[int] = None) -> List[NPBTeam]:
        """Get NPB teams from FanGraphs.
        
        Note: FanGraphs doesn't provide comprehensive team data,
        so this returns an empty list. Use NPB Official source for teams.
        """
        return []
    
    async def get_team_roster(
        self,
        team_id: str,
        season: Optional[int] = None
    ) -> List[NPBPlayer]:
        """Get team roster from FanGraphs.
        
        Note: FanGraphs doesn't provide roster data in an easily parseable format.
        """
        return []
    
    async def health_check(self) -> bool:
        """Check if FanGraphs is accessible.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            test_url = f"{self.base_url}/leaders/international/npb"
            page = await self._fetch_page(test_url)
            return page is not None
        except Exception:
            return False
    
    def _parse_advanced_batting_stats(self, row_cells: list) -> dict:
        """Parse advanced batting statistics from table row.
        
        Args:
            row_cells: List of table cells
            
        Returns:
            Dictionary of advanced stats
        """
        # Column mapping for FanGraphs NPB leaderboard
        # This would need to be adjusted based on actual table structure
        stats = {}
        
        # Helper to extract stat from cell
        def get_cell_value(index, is_float=True):
            if index < len(row_cells):
                try:
                    text = row_cells[index].text.strip()
                    if text and text != '-':
                        return float(text) if is_float else int(text)
                except (ValueError, IndexError):
                    pass
            return None
        
        # Map columns to stats (indices would need adjustment)
        col_index = 5  # Start after name, team, etc.
        
        # Traditional stats first
        stats['games'] = get_cell_value(col_index, is_float=False)
        stats['plate_appearances'] = get_cell_value(col_index + 1, is_float=False)
        
        # Advanced metrics (approximate positions)
        stats['war'] = get_cell_value(col_index + 15)
        stats['wrc_plus'] = get_cell_value(col_index + 16, is_float=False)
        stats['woba'] = get_cell_value(col_index + 17)
        stats['xwoba'] = get_cell_value(col_index + 18)
        
        return {k: v for k, v in stats.items() if v is not None}