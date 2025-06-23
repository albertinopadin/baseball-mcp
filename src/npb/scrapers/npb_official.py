"""NPB official website scraper implementation."""

import re
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse, parse_qs
import logging
from datetime import datetime

from .base_scraper import BaseScraper
from ..constants import NPB_TEAMS, get_team_by_name

logger = logging.getLogger(__name__)


class NPBOfficialScraper(BaseScraper):
    """Scraper for the official NPB website (npb.jp)."""
    
    def __init__(self):
        super().__init__("https://npb.jp")
        self.stats_base_url = f"{self.base_url}/bis/eng"
    
    async def get_current_season(self) -> int:
        """Get the current NPB season year."""
        current_year = datetime.now().year
        # NPB season typically runs March-October
        # If we're in January-February, show previous year's stats
        if datetime.now().month <= 2:
            return current_year - 1
        return current_year
    
    async def search_players_by_stats(self, name: str, season: Optional[int] = None) -> List[Dict[str, Any]]:
        """Search for players by looking at stats pages.
        
        NPB site doesn't have a search function, so we'll look at stats leaders
        and try to find matching names.
        """
        if not season:
            season = await self.get_current_season()
        
        players = []
        name_lower = name.lower()
        
        # Check batting leaders
        # NPB uses different URLs: bat_c.html for Central, bat_p.html for Pacific
        batting_urls = [
            f"{self.stats_base_url}/{season}/stats/bat_c.html",  # Central League
            f"{self.stats_base_url}/{season}/stats/bat_p.html"   # Pacific League
        ]
        
        for batting_url in batting_urls:
            html = await self.fetch_page(batting_url)
            if html:
                soup = self.parse_html(html)
                players.extend(self._extract_players_from_stats_page(soup, name_lower, "batter"))
        
        # Check pitching leaders
        # NPB uses different URLs: pit_c.html for Central, pit_p.html for Pacific
        pitching_urls = [
            f"{self.stats_base_url}/{season}/stats/pit_c.html",  # Central League
            f"{self.stats_base_url}/{season}/stats/pit_p.html"   # Pacific League
        ]
        
        for pitching_url in pitching_urls:
            html = await self.fetch_page(pitching_url)
            if html:
                soup = self.parse_html(html)
                players.extend(self._extract_players_from_stats_page(soup, name_lower, "pitcher"))
        
        # Remove duplicates based on name
        seen = set()
        unique_players = []
        for player in players:
            if player["name_english"] not in seen:
                seen.add(player["name_english"])
                unique_players.append(player)
        
        return unique_players
    
    def _extract_players_from_stats_page(self, soup, search_name: str, player_type: str) -> List[Dict[str, Any]]:
        """Extract players from a stats page that match the search name."""
        players = []
        
        # Find the stats table
        tables = soup.find_all("table", class_="statsTable")
        if not tables:
            return players
        
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                # Skip header rows
                if row.find("th"):
                    continue
                
                cells = row.find_all("td")
                if len(cells) < 3:  # Need at least rank, name, team
                    continue
                
                # Player name is usually in the second cell
                name_cell = cells[1]
                player_link = name_cell.find("a")
                
                if player_link:
                    player_name = player_link.text.strip()
                    
                    # Check if name matches search
                    if search_name in player_name.lower():
                        player_url = player_link.get("href", "")
                        player_id = self._extract_player_id_from_url(player_url)
                        
                        # Team is usually in the third cell
                        team_name = cells[2].text.strip() if len(cells) > 2 else ""
                        
                        players.append({
                            "id": player_id or player_name.replace(" ", "_").lower(),
                            "name_english": player_name,
                            "url": urljoin(self.base_url, player_url) if player_url else "",
                            "team": team_name,
                            "position": "Pitcher" if player_type == "pitcher" else "Batter"
                        })
        
        return players
    
    def _extract_player_id_from_url(self, url: str) -> Optional[str]:
        """Extract player ID from NPB player URL."""
        if not url:
            return None
        
        # NPB URLs often have format: /bis/eng/players/xxxxx.html
        match = re.search(r'/players/(\d+)\.html', url)
        if match:
            return match.group(1)
        
        # Try query parameter format ?id=xxxxx
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        if "id" in params:
            return params["id"][0]
        
        return None
    
    async def get_player_stats_by_year(self, season: int, stat_type: str = "batting") -> List[Dict[str, Any]]:
        """Get all player stats for a given season.
        
        Args:
            season: Year of the season
            stat_type: "batting" or "pitching"
            
        Returns:
            List of player stats dictionaries
        """
        stats_list = []
        
        if stat_type == "batting":
            # Get batting stats for both leagues
            urls = [
                f"{self.stats_base_url}/{season}/stats/bat_c.html",  # Central
                f"{self.stats_base_url}/{season}/stats/bat_p.html"   # Pacific
            ]
        else:
            # Get pitching stats for both leagues
            urls = [
                f"{self.stats_base_url}/{season}/stats/pit_c.html",  # Central
                f"{self.stats_base_url}/{season}/stats/pit_p.html"   # Pacific
            ]
        
        for url in urls:
            html = await self.fetch_page(url)
            if not html:
                logger.error(f"Failed to fetch {stat_type} stats from {url}")
                continue
            
            soup = self.parse_html(html)
            
            if stat_type == "batting":
                stats_list.extend(self._extract_batting_stats(soup, season))
            else:
                stats_list.extend(self._extract_pitching_stats(soup, season))
        
        return stats_list
    
    def _extract_batting_stats(self, soup, season: int) -> List[Dict[str, Any]]:
        """Extract batting statistics from stats page."""
        stats_list = []
        
        # Find the stats table
        table = soup.find("table", class_="statsTable")
        if not table:
            return stats_list
        
        # Extract headers to map column indices
        headers = []
        header_row = table.find("tr")
        if header_row:
            headers = [th.text.strip() for th in header_row.find_all(["th", "td"])]
        
        # Process data rows
        rows = table.find_all("tr")[1:]  # Skip header
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 10:  # Need minimum columns
                continue
            
            try:
                # Extract player info
                rank = self.safe_int(cells[0].text)
                
                # Player name and link
                name_cell = cells[1]
                player_link = name_cell.find("a")
                if not player_link:
                    continue
                
                player_name = player_link.text.strip()
                player_url = player_link.get("href", "")
                player_id = self._extract_player_id_from_url(player_url)
                
                # Team
                team = cells[2].text.strip()
                
                # Stats - map based on typical NPB stats page layout
                stats = {
                    "player_id": player_id or player_name.replace(" ", "_").lower(),
                    "player_name": player_name,
                    "season": season,
                    "team": team,
                    "games": self.safe_int(cells[3].text),
                    "plate_appearances": self.safe_int(cells[4].text),
                    "at_bats": self.safe_int(cells[5].text),
                    "runs": self.safe_int(cells[6].text),
                    "hits": self.safe_int(cells[7].text),
                    "doubles": self.safe_int(cells[8].text) if len(cells) > 8 else 0,
                    "triples": self.safe_int(cells[9].text) if len(cells) > 9 else 0,
                    "home_runs": self.safe_int(cells[10].text) if len(cells) > 10 else 0,
                    "rbis": self.safe_int(cells[11].text) if len(cells) > 11 else 0,
                    "stolen_bases": self.safe_int(cells[12].text) if len(cells) > 12 else 0,
                    "batting_average": self.safe_float(cells[-1].text)  # Usually last column
                }
                
                # Calculate additional stats
                if stats["at_bats"] > 0:
                    stats["on_base_percentage"] = self._calculate_obp(stats)
                    stats["slugging_percentage"] = self._calculate_slg(stats)
                    stats["ops"] = stats["on_base_percentage"] + stats["slugging_percentage"]
                
                stats_list.append(stats)
                
            except Exception as e:
                logger.debug(f"Error parsing batting stats row: {e}")
                continue
        
        return stats_list
    
    def _extract_pitching_stats(self, soup, season: int) -> List[Dict[str, Any]]:
        """Extract pitching statistics from stats page."""
        stats_list = []
        
        # Find the stats table
        table = soup.find("table", class_="statsTable")
        if not table:
            return stats_list
        
        # Process data rows
        rows = table.find_all("tr")[1:]  # Skip header
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 10:  # Need minimum columns
                continue
            
            try:
                # Extract player info
                rank = self.safe_int(cells[0].text)
                
                # Player name and link
                name_cell = cells[1]
                player_link = name_cell.find("a")
                if not player_link:
                    continue
                
                player_name = player_link.text.strip()
                player_url = player_link.get("href", "")
                player_id = self._extract_player_id_from_url(player_url)
                
                # Team
                team = cells[2].text.strip()
                
                # Stats - typical NPB pitching stats layout
                stats = {
                    "player_id": player_id or player_name.replace(" ", "_").lower(),
                    "player_name": player_name,
                    "season": season,
                    "team": team,
                    "wins": self.safe_int(cells[3].text),
                    "losses": self.safe_int(cells[4].text),
                    "era": self.safe_float(cells[5].text),
                    "games": self.safe_int(cells[6].text),
                    "games_started": self.safe_int(cells[7].text) if len(cells) > 7 else 0,
                    "complete_games": self.safe_int(cells[8].text) if len(cells) > 8 else 0,
                    "shutouts": self.safe_int(cells[9].text) if len(cells) > 9 else 0,
                    "innings_pitched": self.safe_float(cells[10].text) if len(cells) > 10 else 0,
                    "strikeouts": self.safe_int(cells[11].text) if len(cells) > 11 else 0,
                    "walks": self.safe_int(cells[12].text) if len(cells) > 12 else 0,
                }
                
                # Calculate WHIP if we have the data
                if stats["innings_pitched"] > 0 and len(cells) > 13:
                    hits_allowed = self.safe_int(cells[13].text)
                    stats["whip"] = (hits_allowed + stats["walks"]) / stats["innings_pitched"]
                
                stats_list.append(stats)
                
            except Exception as e:
                logger.debug(f"Error parsing pitching stats row: {e}")
                continue
        
        return stats_list
    
    def _calculate_obp(self, stats: Dict[str, Any]) -> float:
        """Calculate on-base percentage."""
        # Simplified OBP without walks/HBP data
        # This is just batting average as approximation
        return stats.get("batting_average", 0.0)
    
    def _calculate_slg(self, stats: Dict[str, Any]) -> float:
        """Calculate slugging percentage."""
        ab = stats.get("at_bats", 0)
        if ab == 0:
            return 0.0
        
        singles = stats.get("hits", 0) - stats.get("doubles", 0) - stats.get("triples", 0) - stats.get("home_runs", 0)
        total_bases = (
            singles + 
            (2 * stats.get("doubles", 0)) + 
            (3 * stats.get("triples", 0)) + 
            (4 * stats.get("home_runs", 0))
        )
        
        return total_bases / ab
    
    async def get_team_standings(self, season: Optional[int] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Get NPB standings for both leagues."""
        if not season:
            season = await self.get_current_season()
        
        standings = {
            "central": [],
            "pacific": []
        }
        
        # NPB standings page - uses relative URLs
        urls = [
            (f"{self.stats_base_url}/{season}/standings/std_c.html", "central"),
            (f"{self.stats_base_url}/{season}/standings/std_p.html", "pacific")
        ]
        
        for url, league in urls:
            html = await self.fetch_page(url)
            if not html:
                logger.error(f"Failed to fetch {league} standings for {season}")
                continue
            
            soup = self.parse_html(html)
            
            # Find standings table
            table = soup.find("table", class_="standingsTable")
            if not table:
                # Try without class
                table = soup.find("table")
            
            if table:
                rows = table.find_all("tr")[1:]  # Skip header
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) < 7:  # Need minimum columns
                        continue
                    
                    try:
                        team_standing = {
                            "rank": self.safe_int(cells[0].text),
                            "team": cells[1].text.strip(),
                            "games": self.safe_int(cells[2].text),
                            "wins": self.safe_int(cells[3].text),
                            "losses": self.safe_int(cells[4].text),
                            "ties": self.safe_int(cells[5].text),
                            "winning_percentage": self.safe_float(cells[6].text),
                            "games_behind": self.safe_float(cells[7].text) if len(cells) > 7 else 0
                        }
                        
                        standings[league].append(team_standing)
                        
                    except Exception as e:
                        logger.debug(f"Error parsing standings row: {e}")
                        continue
        
        return standings