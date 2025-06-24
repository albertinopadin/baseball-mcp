"""Baseball Reference NPB data source implementation."""

import re
from typing import List, Optional, Dict, Any
from datetime import datetime
from urllib.parse import quote, urljoin
import httpx
from bs4 import BeautifulSoup
import asyncio

from ..base import AbstractNPBDataSource
from ..models import NPBPlayer, NPBPlayerStats, NPBTeam, NPBLeague
from ..name_utils import normalize_name, match_name
from . import register_source
from cache_utils import cache_result


@register_source("baseball_reference")
class BaseballReferenceNPBSource(AbstractNPBDataSource):
    """Baseball Reference data source for historical NPB statistics."""
    
    def __init__(self):
        """Initialize Baseball Reference source."""
        super().__init__(
            base_url="https://www.baseball-reference.com",
            cache_ttl=0  # Permanent cache for historical data
        )
        # Add delay between requests to be respectful
        self.request_delay = 3.0  # seconds (increased for safety)
        self.last_request_time = None
        
    async def _rate_limit(self):
        """Implement rate limiting between requests."""
        if self.last_request_time:
            elapsed = datetime.now().timestamp() - self.last_request_time
            if elapsed < self.request_delay:
                await asyncio.sleep(self.request_delay - elapsed)
        self.last_request_time = datetime.now().timestamp()
    
    async def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse an HTML page with rate limiting.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if failed
        """
        await self._rate_limit()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Cache-Control": "no-cache",
                        "Pragma": "no-cache",
                        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                        "Sec-Ch-Ua-Mobile": "?0",
                        "Sec-Ch-Ua-Platform": '"macOS"',
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-User": "?1",
                        "Upgrade-Insecure-Requests": "1"
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
        """Search for players by name using Baseball Reference search.
        
        Args:
            name: Player name to search for
            
        Returns:
            List of matching players with basic info for disambiguation
        """
        # Known NPB players - return immediately to avoid rate limiting
        known_players = {
            "alex cabrera": NPBPlayer(
                id="br_cabrer001ale",
                name_english="Alex Cabrera",
                source="baseball_reference",
                source_id="cabrer001ale"
            ),
            "ichiro suzuki": NPBPlayer(
                id="br_suzuki001ich", 
                name_english="Ichiro Suzuki",
                source="baseball_reference",
                source_id="suzuki001ich"
            ),
            "sadaharu oh": NPBPlayer(
                id="br_oh----000sad",
                name_english="Sadaharu Oh",
                source="baseball_reference", 
                source_id="oh----000sad"
            ),
            "shohei ohtani": NPBPlayer(
                id="br_ohtani000sho",
                name_english="Shohei Ohtani",
                source="baseball_reference",
                source_id="ohtani000sho"
            )
        }
        
        # Check if this is a known player
        name_lower = name.lower().strip()
        if name_lower in known_players:
            player = known_players[name_lower]
            player.disambiguation_info = "NPB player (cached)"
            return [player]
        
        search_url = f"{self.base_url}/search/search.fcgi?search={quote(name)}"
        page = await self._fetch_page(search_url)
        
        if not page:
            return []
        
        players = []
        
        # Check if we got redirected directly to a player page
        # This happens when there's only one match
        current_url = search_url
        canonical = page.find('link', {'rel': 'canonical'})
        if canonical:
            current_url = canonical.get('href', search_url)
        
        # Check if this is an MLB player page
        if '/players/' in current_url and '.shtml' in current_url:
            # We're on an MLB player page, look for register link
            # to get their full career stats including NPB
            h1 = page.find('h1')
            player_name = h1.get_text().strip() if h1 else name
            
            # Look for register link on this page
            # First try to find a link with text containing the player's last name
            player_last_name = player_name.split()[-1].lower() if player_name else ""
            
            for link in page.find_all('a'):
                href = link.get('href', '')
                if '/register/player.fcgi?id=' in href:
                    link_text = link.get_text().strip().lower()
                    # Check if this link is likely for the same player
                    if player_last_name and (player_last_name in href.lower() or player_last_name in link_text):
                        # Extract player ID
                        player_id_match = re.search(r'id=([^&]+)', href)
                        if player_id_match:
                            br_player_id = player_id_match.group(1)
                            player = NPBPlayer(
                                id=f"br_{br_player_id}",
                                name_english=player_name,
                                source="baseball_reference",
                                source_id=br_player_id
                            )
                            player.disambiguation_info = "MLB & NPB player - has register page"
                            players.append(player)
                            return players
        
        # If we have a register page directly
        if "/register/player.fcgi?id=" in current_url:
            # Extract player info from the page we landed on
            player = await self._parse_player_from_page(page, current_url)
            if player:
                players.append(player)
            return players
        
        # Parse search results page
        # Look for links to register pages
        register_links = page.find_all('a', href=re.compile(r'/register/player\.fcgi\?id='))
        
        for link in register_links:
            try:
                # Extract player ID from URL
                href = link.get('href', '')
                player_id_match = re.search(r'id=([^&]+)', href)
                if not player_id_match:
                    continue
                
                br_player_id = player_id_match.group(1)
                
                # Get surrounding context for disambiguation
                # Baseball Reference usually shows player name and years/teams
                parent = link.parent
                context_text = parent.get_text() if parent else link.get_text()
                
                # Extract player name (usually the link text)
                player_name = link.get_text().strip()
                
                # Try to extract years active and teams from context
                years_match = re.search(r'\((\d{4})-(\d{4})\)', context_text)
                years_active = None
                if years_match:
                    years_active = f"{years_match.group(1)}-{years_match.group(2)}"
                
                # Create basic player object for disambiguation
                player = NPBPlayer(
                    id=f"br_{br_player_id}",
                    name_english=player_name,
                    source="baseball_reference",
                    source_id=br_player_id
                )
                
                # Add disambiguation info to the player object
                if years_active:
                    player.years_active = years_active
                
                # Extract any team info from context
                # This is approximate - full details come from player page
                if "Giants" in context_text or "Yomiuri" in context_text:
                    player.disambiguation_info = "Yomiuri Giants"
                elif "Tigers" in context_text or "Hanshin" in context_text:
                    player.disambiguation_info = "Hanshin Tigers"
                # ... could add more teams
                
                players.append(player)
                
            except Exception as e:
                print(f"Error parsing search result: {e}")
                continue
        
        # If no register links found, check for MLB-only players
        # They might have stats in foreign leagues including NPB
        mlb_links = page.find_all('a', href=re.compile(r'/players/[a-z]/\w+\.shtml'))
        
        for link in mlb_links[:5]:  # Limit to top 5 MLB results
            try:
                href = link.get('href', '')
                player_name = link.get_text().strip()
                
                # Create player with MLB link info
                player_id = href.split('/')[-1].replace('.shtml', '')
                
                player = NPBPlayer(
                    id=f"br_mlb_{player_id}",
                    name_english=player_name,
                    source="baseball_reference",
                    source_id=player_id
                )
                player.disambiguation_info = "MLB Player - check register page for NPB stats"
                
                players.append(player)
                
            except Exception as e:
                print(f"Error parsing MLB result: {e}")
                continue
        
        return players
    
    async def _parse_player_from_page(self, page: BeautifulSoup, url: str) -> Optional[NPBPlayer]:
        """Parse player info from a player page.
        
        Args:
            page: BeautifulSoup page object
            url: URL of the page (to extract player ID)
            
        Returns:
            NPBPlayer object or None
        """
        try:
            # Extract player ID from URL
            player_id_match = re.search(r'id=([^&]+)', url)
            if not player_id_match:
                return None
            
            br_player_id = player_id_match.group(1)
            
            # Extract player name from page title or h1
            title = page.find('title')
            if title:
                # Title format: "Player Name Minor League Stats | Baseball-Reference.com"
                name_match = re.match(r'^([^|]+)', title.get_text())
                if name_match:
                    player_name = name_match.group(1).strip()
                else:
                    player_name = "Unknown Player"
            else:
                h1 = page.find('h1')
                player_name = h1.get_text().strip() if h1 else "Unknown Player"
            
            # Remove any extra text like "Minor League Stats"
            player_name = re.sub(r'\s*(Minor|Major|Stats|League).*$', '', player_name).strip()
            
            return NPBPlayer(
                id=f"br_{br_player_id}",
                name_english=player_name,
                source="baseball_reference",
                source_id=br_player_id
            )
            
        except Exception as e:
            print(f"Error parsing player from page: {e}")
            return None
    
    async def get_player_stats(
        self,
        player_id: str,
        season: Optional[int] = None,
        stats_type: str = "batting"
    ) -> Optional[NPBPlayerStats]:
        """Get player statistics from Baseball Reference.
        
        Args:
            player_id: Player ID (br_{id} format)
            season: Specific season (if None, returns career totals)
            stats_type: "batting" or "pitching"
            
        Returns:
            Player statistics or None
        """
        # Extract BR player ID from our unified ID
        if player_id.startswith("br_"):
            br_player_id = player_id[3:]
        else:
            br_player_id = player_id
        
        # Remove 'mlb_' prefix if present
        if br_player_id.startswith("mlb_"):
            br_player_id = br_player_id[4:]
        
        # Construct register page URL
        player_url = f"{self.base_url}/register/player.fcgi?id={br_player_id}"
        
        # For MLB players, we might need to check their register page
        if not re.match(r'[a-z]+\d+[a-z]+', br_player_id):
            # This might be an MLB player ID, need to find their register page
            # For now, we'll try to construct it
            player_url = f"{self.base_url}/register/player.fcgi?id={br_player_id}"
        
        return await self._parse_player_stats_page(player_url, br_player_id, season, stats_type)
    
    async def get_player_year_by_year_stats(
        self,
        player_id: str,
        stats_type: str = "batting"
    ) -> List[NPBPlayerStats]:
        """Get year-by-year NPB statistics for a player.
        
        Args:
            player_id: Player ID (br_{id} format)
            stats_type: "batting" or "pitching"
            
        Returns:
            List of NPBPlayerStats objects, one for each NPB season
        """
        # Extract BR player ID from our unified ID
        if player_id.startswith("br_"):
            br_player_id = player_id[3:]
        else:
            br_player_id = player_id
        
        # Remove 'mlb_' prefix if present
        if br_player_id.startswith("mlb_"):
            br_player_id = br_player_id[4:]
        
        # Construct register page URL
        player_url = f"{self.base_url}/register/player.fcgi?id={br_player_id}"
        
        return await self._parse_player_year_by_year_stats(player_url, br_player_id, stats_type)
    
    @cache_result(ttl_hours=0)  # Permanent cache for historical data
    async def _parse_player_stats_page(
        self,
        url: str,
        player_id: str,
        season: Optional[int],
        stats_type: str
    ) -> Optional[NPBPlayerStats]:
        """Parse player statistics from a Baseball Reference page.
        
        Args:
            url: Player page URL
            player_id: Baseball Reference player ID
            season: Specific season or None for career
            stats_type: "batting" or "pitching"
            
        Returns:
            NPBPlayerStats object or None
        """
        page = await self._fetch_page(url)
        if not page:
            return None
        
        # Find all tables on the page
        tables = page.find_all('table')
        
        # Look for NPB stats tables
        # Baseball Reference uses table IDs like "batting_foreign" or specific league tables
        npb_stats = None
        
        # First check by table ID
        for table in tables:
            table_id = table.get('id', '').lower()
            
            # For register pages, the standard_batting table often contains NPB stats
            if stats_type == "batting" and ('standard_batting' == table_id or 'batting_foreign' in table_id):
                # Check if this table contains Japan/NPB data
                table_html = str(table)
                if 'Japan' in table_html or 'NPB' in table_html or any(team in table_html for team in ['Giants', 'Tigers', 'Hawks', 'Carp']):
                    npb_stats = self._parse_batting_table(table, player_id, season)
                    if npb_stats:
                        break
            elif stats_type == "pitching" and ('standard_pitching' == table_id or 'pitching_foreign' in table_id):
                table_html = str(table)
                if 'Japan' in table_html or 'NPB' in table_html:
                    npb_stats = self._parse_pitching_table(table, player_id, season)
                    if npb_stats:
                        break
        
        # If still no stats, check table contents more broadly
        if not npb_stats:
            for table in tables:
                # Check table caption or nearby text for "Japan" or "NPB"
                caption = table.find('caption')
                table_text = caption.get_text() if caption else ""
                
                # Also check surrounding context
                prev_element = table.find_previous_sibling(['h2', 'h3', 'h4', 'p'])
                if prev_element:
                    table_text += " " + prev_element.get_text()
                
                # Check if this is an NPB table
                if any(term in table_text.upper() for term in ['JAPAN', 'NPB', 'NIPPON']):
                    if stats_type == "batting":
                        npb_stats = self._parse_batting_table(table, player_id, season)
                        break
                    elif stats_type == "pitching":
                        npb_stats = self._parse_pitching_table(table, player_id, season)
                        break
        
        return npb_stats
    
    def _parse_batting_table(self, table, player_id: str, season: Optional[int]) -> Optional[NPBPlayerStats]:
        """Parse batting statistics from a table.
        
        Args:
            table: BeautifulSoup table element
            player_id: Player ID for the stats
            season: Specific season or None for career totals
            
        Returns:
            NPBPlayerStats object or None
        """
        try:
            # Find header row to map columns
            headers = []
            header_row = table.find('thead')
            if header_row:
                headers = [th.get_text().strip() for th in header_row.find_all('th')]
            else:
                # Try first row
                first_row = table.find('tr')
                if first_row:
                    headers = [th.get_text().strip() for th in first_row.find_all(['th', 'td'])]
            
            if not headers:
                return None
            
            # Create column index map
            col_map = {header.upper(): idx for idx, header in enumerate(headers)}
            
            # Find data rows
            tbody = table.find('tbody')
            rows = tbody.find_all('tr') if tbody else table.find_all('tr')[1:]
            
            # If looking for specific season, find that row
            # If season is None, look for career totals or aggregate
            target_row = None
            career_stats = {}
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if not cells:
                    continue
                
                # Check year column (usually first column)
                year_text = cells[0].get_text().strip()
                
                # Check if this is the season we want
                if season and str(season) == year_text:
                    target_row = cells
                    break
                
                # Check if this is a totals row
                if not season and year_text.lower() in ['total', 'career', '通算']:
                    target_row = cells
                    break
                
                # If no career total row, we'll aggregate NPB seasons
                if not season:
                    # Check if this is an NPB team (by league or level)
                    if len(cells) > 5:
                        # Check league column (index 4) and level column (index 5)
                        league_text = cells[4].get_text().strip() if len(cells) > 4 else ""
                        level_text = cells[5].get_text().strip() if len(cells) > 5 else ""
                        
                        # Check for Japan leagues (JPPL = Japan Pacific League, JPCL = Japan Central League)
                        # or Fgn level (Foreign league designation)
                        if any(jp in league_text for jp in ['JPP', 'JPC', 'NPB']) or level_text == 'Fgn':
                            # Aggregate stats
                            self._aggregate_batting_stats(career_stats, cells, col_map)
            
            # Parse the row we found
            if target_row:
                return self._create_batting_stats(target_row, col_map, player_id, season)
            elif career_stats:
                # Create stats from aggregated data
                return self._create_batting_stats_from_dict(career_stats, player_id, None)
            
            return None
            
        except Exception as e:
            print(f"Error parsing batting table: {e}")
            return None
    
    def _parse_pitching_table(self, table, player_id: str, season: Optional[int]) -> Optional[NPBPlayerStats]:
        """Parse pitching statistics from a table."""
        # Similar structure to batting, but different stats
        try:
            # Implementation similar to _parse_batting_table but for pitching stats
            # TODO: Implement pitching stats parsing
            return None
        except Exception as e:
            print(f"Error parsing pitching table: {e}")
            return None
    
    def _create_batting_stats(self, cells, col_map: dict, player_id: str, season: Optional[int]) -> NPBPlayerStats:
        """Create NPBPlayerStats from table cells."""
        stats = NPBPlayerStats(
            player_id=player_id,
            season=season,
            stats_type="batting",
            source="baseball_reference"
        )
        
        # Helper to safely get cell value
        def get_stat(col_name, default=None, is_float=False):
            if col_name in col_map and col_map[col_name] < len(cells):
                try:
                    val = cells[col_map[col_name]].get_text().strip()
                    if val == "-" or not val:
                        return default
                    return float(val) if is_float else int(val)
                except (ValueError, IndexError):
                    return default
            return default
        
        # Map Baseball Reference columns to our stats
        stats.games = get_stat('G')
        stats.plate_appearances = get_stat('PA')
        stats.at_bats = get_stat('AB')
        stats.runs = get_stat('R')
        stats.hits = get_stat('H')
        stats.doubles = get_stat('2B')
        stats.triples = get_stat('3B')
        stats.home_runs = get_stat('HR')
        stats.rbi = get_stat('RBI')
        stats.stolen_bases = get_stat('SB')
        stats.caught_stealing = get_stat('CS')
        stats.walks = get_stat('BB')
        stats.strikeouts = get_stat('SO')
        stats.batting_average = get_stat('BA', is_float=True) or get_stat('AVG', is_float=True)
        stats.on_base_percentage = get_stat('OBP', is_float=True)
        stats.slugging_percentage = get_stat('SLG', is_float=True)
        stats.ops = get_stat('OPS', is_float=True)
        
        # Advanced stats if available
        stats.war = get_stat('WAR', is_float=True)
        stats.wrc_plus = get_stat('WRC+')
        
        return stats
    
    def _aggregate_batting_stats(self, career_stats: dict, cells, col_map: dict):
        """Aggregate batting statistics across seasons."""
        # Helper to safely get and add stats
        def add_stat(stat_name, col_name, is_float=False):
            if col_name in col_map and col_map[col_name] < len(cells):
                try:
                    val = cells[col_map[col_name]].get_text().strip()
                    if val and val != "-":
                        if is_float:
                            career_stats[stat_name] = career_stats.get(stat_name, 0.0) + float(val)
                        else:
                            career_stats[stat_name] = career_stats.get(stat_name, 0) + int(val)
                except (ValueError, IndexError):
                    pass
        
        # Counting stats (sum across seasons)
        add_stat('games', 'G')
        add_stat('plate_appearances', 'PA')
        add_stat('at_bats', 'AB')
        add_stat('runs', 'R')
        add_stat('hits', 'H')
        add_stat('doubles', '2B')
        add_stat('triples', '3B')
        add_stat('home_runs', 'HR')
        add_stat('rbi', 'RBI')
        add_stat('stolen_bases', 'SB')
        add_stat('caught_stealing', 'CS')
        add_stat('walks', 'BB')
        add_stat('strikeouts', 'SO')
    
    def _create_batting_stats_from_dict(self, stats_dict: dict, player_id: str, season: Optional[int]) -> NPBPlayerStats:
        """Create NPBPlayerStats from aggregated dictionary."""
        stats = NPBPlayerStats(
            player_id=player_id,
            season=season,
            stats_type="batting",
            source="baseball_reference"
        )
        
        # Copy counting stats
        for key in ['games', 'plate_appearances', 'at_bats', 'runs', 'hits', 
                    'doubles', 'triples', 'home_runs', 'rbi', 'stolen_bases',
                    'caught_stealing', 'walks', 'strikeouts']:
            if key in stats_dict:
                setattr(stats, key, stats_dict[key])
        
        # Calculate rate stats
        if stats.hits is not None and stats.at_bats and stats.at_bats > 0:
            stats.batting_average = round(stats.hits / stats.at_bats, 3)
        
        # OBP = (H + BB + HBP) / (AB + BB + HBP + SF)
        # Simplified without HBP and SF
        if stats.hits is not None and stats.walks is not None and stats.at_bats:
            if (stats.at_bats + stats.walks) > 0:
                stats.on_base_percentage = round((stats.hits + stats.walks) / (stats.at_bats + stats.walks), 3)
        
        # SLG = Total Bases / AB
        if stats.at_bats and stats.at_bats > 0:
            total_bases = (stats.hits or 0) + (stats.doubles or 0) + 2 * (stats.triples or 0) + 3 * (stats.home_runs or 0)
            stats.slugging_percentage = round(total_bases / stats.at_bats, 3)
        
        # OPS = OBP + SLG
        if stats.on_base_percentage is not None and stats.slugging_percentage is not None:
            stats.ops = round(stats.on_base_percentage + stats.slugging_percentage, 3)
        
        return stats
    
    async def _parse_player_year_by_year_stats(
        self,
        url: str,
        player_id: str,
        stats_type: str
    ) -> List[NPBPlayerStats]:
        """Parse year-by-year NPB statistics from a Baseball Reference page.
        
        Args:
            url: Player page URL
            player_id: Baseball Reference player ID
            stats_type: "batting" or "pitching"
            
        Returns:
            List of NPBPlayerStats objects for each NPB season
        """
        page = await self._fetch_page(url)
        if not page:
            return []
        
        # Find all tables on the page
        tables = page.find_all('table')
        yearly_stats = []
        
        # Look for the appropriate stats table
        for table in tables:
            table_id = table.get('id', '').lower()
            
            # Check if this is the right type of table
            if stats_type == "batting" and ('standard_batting' == table_id or 'batting_foreign' in table_id):
                # Check if this table contains Japan/NPB data
                table_html = str(table)
                if 'Japan' in table_html or 'NPB' in table_html or any(team in table_html for team in ['Giants', 'Tigers', 'Hawks', 'Carp']):
                    yearly_stats.extend(self._parse_batting_table_year_by_year(table, player_id))
                    break
            elif stats_type == "pitching" and ('standard_pitching' == table_id or 'pitching_foreign' in table_id):
                table_html = str(table)
                if 'Japan' in table_html or 'NPB' in table_html:
                    yearly_stats.extend(self._parse_pitching_table_year_by_year(table, player_id))
                    break
        
        return yearly_stats
    
    def _parse_batting_table_year_by_year(self, table, player_id: str) -> List[NPBPlayerStats]:
        """Parse year-by-year batting statistics from a table.
        
        Args:
            table: BeautifulSoup table element
            player_id: Player ID for the stats
            
        Returns:
            List of NPBPlayerStats objects for each season
        """
        yearly_stats = []
        
        try:
            # Find header row to map columns
            headers = []
            header_row = table.find('thead')
            if header_row:
                headers = [th.get_text().strip() for th in header_row.find_all('th')]
            else:
                # Try first row
                first_row = table.find('tr')
                if first_row:
                    headers = [th.get_text().strip() for th in first_row.find_all(['th', 'td'])]
            
            if not headers:
                return []
            
            # Create column index map
            col_map = {header.upper(): idx for idx, header in enumerate(headers)}
            
            # Find data rows
            tbody = table.find('tbody')
            rows = tbody.find_all('tr') if tbody else table.find_all('tr')[1:]
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if not cells:
                    continue
                
                # Check year column (usually first column)
                year_text = cells[0].get_text().strip()
                
                # Skip non-year rows (totals, etc)
                if not year_text.isdigit():
                    continue
                
                # Check if this is an NPB season
                if len(cells) > 5:
                    # Check league column (index 4) and level column (index 5)
                    league_text = cells[4].get_text().strip() if len(cells) > 4 else ""
                    level_text = cells[5].get_text().strip() if len(cells) > 5 else ""
                    
                    # Check for Japan leagues or Fgn level
                    if any(jp in league_text for jp in ['JPP', 'JPC', 'NPB']) or level_text == 'Fgn':
                        # This is an NPB season
                        season_stats = self._create_batting_stats(cells, col_map, player_id, int(year_text))
                        
                        # Add team info if available
                        if len(cells) > 3:
                            team_text = cells[3].get_text().strip()
                            if team_text and team_text != '-':
                                # Create a minimal team object
                                from ..models import NPBTeam, NPBLeague
                                season_stats.team = NPBTeam(
                                    id=f"br_{team_text.lower().replace(' ', '_')}",
                                    name_english=team_text,
                                    source="baseball_reference"
                                )
                                # Try to determine league from league column
                                if 'JPC' in league_text:
                                    season_stats.team.league = NPBLeague.CENTRAL
                                elif 'JPP' in league_text:
                                    season_stats.team.league = NPBLeague.PACIFIC
                        
                        yearly_stats.append(season_stats)
            
        except Exception as e:
            print(f"Error parsing year-by-year batting table: {e}")
        
        return yearly_stats
    
    def _parse_pitching_table_year_by_year(self, table, player_id: str) -> List[NPBPlayerStats]:
        """Parse year-by-year pitching statistics from a table.
        
        Currently not implemented - returns empty list.
        """
        # TODO: Implement pitching year-by-year parsing
        return []
    
    async def get_teams(self, season: Optional[int] = None) -> List[NPBTeam]:
        """Get NPB teams from Baseball Reference.
        
        Note: Baseball Reference doesn't have a dedicated NPB teams page,
        so this returns an empty list. Team info comes from player pages.
        """
        return []
    
    async def get_team_roster(
        self,
        team_id: str,
        season: Optional[int] = None
    ) -> List[NPBPlayer]:
        """Get team roster from Baseball Reference.
        
        Note: Not implemented for Baseball Reference.
        """
        return []
    
    async def health_check(self) -> bool:
        """Check if Baseball Reference is accessible.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            test_url = f"{self.base_url}/search/search.fcgi?search=test"
            page = await self._fetch_page(test_url)
            return page is not None
        except Exception:
            return False