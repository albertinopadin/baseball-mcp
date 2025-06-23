"""Baseball-Reference NPB scraper implementation."""

import re
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, quote
import logging

from .base_scraper import BaseScraper
from ..models import NPBPlayer, NPBBattingStats, NPBPitchingStats
from ..constants import BR_NPB_BASE_URL, get_team_by_name

logger = logging.getLogger(__name__)


class BaseballReferenceNPBScraper(BaseScraper):
    """Scraper for Baseball-Reference NPB data."""
    
    def __init__(self):
        super().__init__(BR_NPB_BASE_URL)
        self.search_base_url = f"{BR_NPB_BASE_URL}/search/search.fcgi"
    
    async def search_players(self, name: str) -> List[Dict[str, Any]]:
        """Search for NPB players by name.
        
        Args:
            name: Player name to search for
            
        Returns:
            List of player dictionaries
        """
        # Construct search URL
        search_params = {
            "search": name,
            "pid": "",
            "hint": ""
        }
        
        # Build query string manually to ensure proper encoding
        query_parts = [f"{k}={quote(str(v))}" for k, v in search_params.items()]
        search_url = f"{self.search_base_url}?{'&'.join(query_parts)}"
        
        html = await self.fetch_page(search_url)
        if not html:
            logger.error(f"Failed to fetch search results for {name}")
            return []
        
        soup = self.parse_html(html)
        players = []
        
        # Check if we were redirected to a single player page
        if "/players/" in str(soup):
            # Extract player info from the page
            player_info = self._extract_player_from_page(soup, html)
            if player_info:
                players.append(player_info)
            return players
        
        # Look for search results
        search_results = soup.find("div", {"id": "searches"})
        if not search_results:
            logger.debug(f"No search results found for {name}")
            return []
        
        # Find Japanese baseball results section
        japan_section = None
        for h3 in search_results.find_all("h3"):
            if "Japan" in h3.text or "NPB" in h3.text:
                japan_section = h3.find_next_sibling("div", class_="search-item-list")
                break
        
        if not japan_section:
            logger.debug(f"No Japanese baseball results for {name}")
            return []
        
        # Extract player links
        for item in japan_section.find_all("div", class_="search-item"):
            link = item.find("a")
            if link and "/register/player.fcgi" in link.get("href", ""):
                player_data = self._parse_search_result_item(item, link)
                if player_data:
                    players.append(player_data)
        
        return players
    
    def _extract_player_from_page(self, soup, html: str) -> Optional[Dict[str, Any]]:
        """Extract player info when redirected to player page."""
        # Extract player ID from URL in the HTML
        player_id_match = re.search(r'/register/player\.fcgi\?id=([^"&]+)', html)
        if not player_id_match:
            return None
        
        player_id = player_id_match.group(1)
        
        # Extract player name from page title or h1
        h1 = soup.find("h1", {"itemprop": "name"})
        if not h1:
            h1 = soup.find("h1")
        
        # Special handling for search results page
        if h1 and "Search Results" in h1.text:
            # This is actually a search results page, extract the actual player name
            # Look for the player's actual name in the page
            name_elem = soup.find("div", {"id": "info"})
            if name_elem:
                name_h1 = name_elem.find("h1")
                if name_h1:
                    name = name_h1.text.strip()
                else:
                    name = "Unknown Player"
            else:
                name = "Unknown Player"
        elif h1:
            name = h1.text.strip()
        else:
            return None
        
        # Extract other info from the page
        info_div = soup.find("div", {"itemtype": "https://schema.org/Person"})
        
        player_data = {
            "id": player_id,
            "name_english": name,
            "url": f"{BR_NPB_BASE_URL}/register/player.fcgi?id={player_id}"
        }
        
        # Try to extract position and team from metadata
        if info_div:
            position_elem = info_div.find("span", string=re.compile(r"Position"))
            if position_elem:
                position_text = position_elem.find_next_sibling(string=True)
                if position_text:
                    player_data["position"] = position_text.strip()
        
        return player_data
    
    def _parse_search_result_item(self, item_div, link) -> Optional[Dict[str, Any]]:
        """Parse a search result item."""
        href = link.get("href", "")
        player_id_match = re.search(r'id=([^&]+)', href)
        if not player_id_match:
            return None
        
        player_id = player_id_match.group(1)
        name = link.text.strip()
        
        # Extract additional info from the search result
        info_text = item_div.text.strip()
        
        player_data = {
            "id": player_id,
            "name_english": name,
            "url": urljoin(BR_NPB_BASE_URL, href)
        }
        
        # Try to extract years active
        years_match = re.search(r'\((\d{4})-(\d{4})\)', info_text)
        if years_match:
            player_data["years_active"] = f"{years_match.group(1)}-{years_match.group(2)}"
        
        # Try to extract position
        position_match = re.search(r'(Pitcher|Catcher|Infielder|Outfielder|First Base|Second Base|Third Base|Shortstop)', info_text)
        if position_match:
            player_data["position"] = position_match.group(1)
        
        return player_data
    
    async def get_player_stats(
        self, 
        player_id: str, 
        season: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get player statistics from Baseball-Reference.
        
        Args:
            player_id: Baseball-Reference player ID
            season: Specific season (None for career)
            
        Returns:
            Dictionary with player stats
        """
        url = f"{BR_NPB_BASE_URL}/register/player.fcgi?id={player_id}"
        html = await self.fetch_page(url)
        
        if not html:
            logger.error(f"Failed to fetch player page for ID: {player_id}")
            return {}
        
        soup = self.parse_html(html)
        
        # Extract player basic info
        player_info = self._extract_player_info(soup)
        
        # Determine if player is a pitcher or position player
        is_pitcher = self._is_pitcher(soup)
        
        # Extract stats based on player type
        if is_pitcher:
            stats = self._extract_pitching_stats(soup, season)
        else:
            stats = self._extract_batting_stats(soup, season)
        
        return {
            "player": player_info,
            "stats_type": "pitching" if is_pitcher else "batting",
            "stats": stats
        }
    
    def _extract_player_info(self, soup) -> Dict[str, Any]:
        """Extract basic player information from page."""
        info = {}
        
        # Try multiple selectors for player name
        h1 = soup.find("h1", {"itemprop": "name"})
        if not h1:
            # Try the info box
            info_box = soup.find("div", {"id": "info"})
            if info_box:
                h1 = info_box.find("h1")
        
        if h1:
            info["name_english"] = h1.text.strip()
        
        # Extract from info box
        info_div = soup.find("div", {"id": "info"})
        if not info_div:
            info_div = soup.find("div", {"itemtype": "https://schema.org/Person"})
            
        if info_div:
            # Position
            pos_elem = info_div.find(string=re.compile(r"Position"))
            if pos_elem:
                pos_text = pos_elem.find_next(string=True)
                if pos_text:
                    info["position"] = pos_text.strip().rstrip(":")
            
            # Birth date
            birth_elem = info_div.find("span", {"itemprop": "birthDate"})
            if birth_elem:
                info["birth_date"] = birth_elem.get("data-birth", "")
            
            # Height/Weight
            height_weight = info_div.find(string=re.compile(r"\d+cm"))
            if height_weight:
                hw_match = re.search(r'(\d+)cm.*?(\d+)kg', str(height_weight))
                if hw_match:
                    info["height"] = f"{hw_match.group(1)}cm"
                    info["weight"] = f"{hw_match.group(2)}kg"
            
            # Bats/Throws
            bats_throws = info_div.find(string=re.compile(r"Bats:"))
            if bats_throws:
                bt_match = re.search(r'Bats:\s*(\w+).*?Throws:\s*(\w+)', str(bats_throws))
                if bt_match:
                    info["bats"] = bt_match.group(1)
                    info["throws"] = bt_match.group(2)
        
        return info
    
    def _is_pitcher(self, soup) -> bool:
        """Determine if player is a pitcher based on page content."""
        # Check position info
        pos_elem = soup.find(string=re.compile(r"Position"))
        if pos_elem:
            pos_text = str(pos_elem.find_next(string=True))
            if "Pitcher" in pos_text:
                return True
        
        # Check for pitching stats table
        pitching_table = soup.find("table", {"id": re.compile(r"pitching")})
        batting_table = soup.find("table", {"id": re.compile(r"batting")})
        
        # If only pitching table exists, it's a pitcher
        if pitching_table and not batting_table:
            return True
        
        return False
    
    def _extract_batting_stats(self, soup, season: Optional[int] = None) -> List[Dict[str, Any]]:
        """Extract batting statistics from player page."""
        stats_list = []
        
        # Find batting stats table - try multiple IDs
        batting_table = None
        for table_id in ["batting_standard", "batting", "standard_batting"]:
            batting_table = soup.find("table", {"id": table_id})
            if batting_table:
                logger.debug(f"Found batting table with ID: {table_id}")
                break
        
        if not batting_table:
            # Try to find any table with batting-related class
            batting_table = soup.find("table", class_=re.compile(r"batting|stats"))
            if batting_table:
                logger.debug("Found batting table by class")
        
        if not batting_table:
            logger.debug("No batting table found")
            return stats_list
        
        # Extract table data
        table_data = self.extract_table_data(soup, batting_table.get("id"))
        
        for row in table_data:
            # Skip non-NPB rows
            if "Lg" in row and row["Lg"] not in ["JPPL", "JPCL", "NPB"]:
                continue
            
            # Parse year
            year = self.safe_int(row.get("Year", 0))
            
            # If specific season requested, filter
            if season and year != season:
                continue
            
            # Create stats object
            stats = {
                "season": year,
                "team": row.get("Tm", ""),
                "league": row.get("Lg", ""),
                "games": self.safe_int(row.get("G", 0)),
                "plate_appearances": self.safe_int(row.get("PA", 0)),
                "at_bats": self.safe_int(row.get("AB", 0)),
                "runs": self.safe_int(row.get("R", 0)),
                "hits": self.safe_int(row.get("H", 0)),
                "doubles": self.safe_int(row.get("2B", 0)),
                "triples": self.safe_int(row.get("3B", 0)),
                "home_runs": self.safe_int(row.get("HR", 0)),
                "rbis": self.safe_int(row.get("RBI", 0)),
                "stolen_bases": self.safe_int(row.get("SB", 0)),
                "caught_stealing": self.safe_int(row.get("CS", 0)),
                "walks": self.safe_int(row.get("BB", 0)),
                "strikeouts": self.safe_int(row.get("SO", 0)),
                "batting_average": self.safe_float(row.get("BA", 0)),
                "on_base_percentage": self.safe_float(row.get("OBP", 0)),
                "slugging_percentage": self.safe_float(row.get("SLG", 0)),
                "ops": self.safe_float(row.get("OPS", 0)),
                "ops_plus": self.safe_int(row.get("OPS+", None))
            }
            
            stats_list.append(stats)
        
        # If no specific season, return all
        # If specific season, return just that season's stats
        if season and stats_list:
            return stats_list[0:1]  # Return as list with single item
        
        return stats_list
    
    def _extract_pitching_stats(self, soup, season: Optional[int] = None) -> List[Dict[str, Any]]:
        """Extract pitching statistics from player page."""
        stats_list = []
        
        # Find pitching stats table
        pitching_table = soup.find("table", {"id": re.compile(r"pitching")})
        if not pitching_table:
            return stats_list
        
        # Extract table data
        table_data = self.extract_table_data(soup, pitching_table.get("id"))
        
        for row in table_data:
            # Skip non-NPB rows
            if "Lg" in row and row["Lg"] not in ["JPPL", "JPCL", "NPB"]:
                continue
            
            # Parse year
            year = self.safe_int(row.get("Year", 0))
            
            # If specific season requested, filter
            if season and year != season:
                continue
            
            # Create stats object
            stats = {
                "season": year,
                "team": row.get("Tm", ""),
                "league": row.get("Lg", ""),
                "wins": self.safe_int(row.get("W", 0)),
                "losses": self.safe_int(row.get("L", 0)),
                "era": self.safe_float(row.get("ERA", 0)),
                "games": self.safe_int(row.get("G", 0)),
                "games_started": self.safe_int(row.get("GS", 0)),
                "complete_games": self.safe_int(row.get("CG", 0)),
                "shutouts": self.safe_int(row.get("SHO", 0)),
                "saves": self.safe_int(row.get("SV", 0)),
                "innings_pitched": self.safe_float(row.get("IP", 0)),
                "hits_allowed": self.safe_int(row.get("H", 0)),
                "runs_allowed": self.safe_int(row.get("R", 0)),
                "earned_runs": self.safe_int(row.get("ER", 0)),
                "home_runs_allowed": self.safe_int(row.get("HR", 0)),
                "walks": self.safe_int(row.get("BB", 0)),
                "strikeouts": self.safe_int(row.get("SO", 0)),
                "whip": self.safe_float(row.get("WHIP", 0)),
                "era_plus": self.safe_int(row.get("ERA+", None))
            }
            
            # Calculate additional metrics if not provided
            if stats["innings_pitched"] > 0:
                if "SO9" not in row:
                    stats["strikeouts_per_nine"] = (stats["strikeouts"] / stats["innings_pitched"]) * 9
                else:
                    stats["strikeouts_per_nine"] = self.safe_float(row.get("SO9", 0))
                
                if "BB9" not in row:
                    stats["walks_per_nine"] = (stats["walks"] / stats["innings_pitched"]) * 9
                else:
                    stats["walks_per_nine"] = self.safe_float(row.get("BB9", 0))
            
            stats_list.append(stats)
        
        # If no specific season, return all
        # If specific season, return just that season's stats
        if season and stats_list:
            return stats_list[0:1]  # Return as list with single item
        
        return stats_list