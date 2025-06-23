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
        
        # Also handle name variations (e.g., "Shohei Ohtani" vs "Shohei Otani")
        name_variations = [name_lower]
        if "ohtani" in name_lower:
            name_variations.append(name_lower.replace("ohtani", "otani"))
        elif "otani" in name_lower:
            name_variations.append(name_lower.replace("otani", "ohtani"))
        
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
                for name_var in name_variations:
                    players.extend(self._extract_players_from_stats_page(soup, name_var, "batter"))
        
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
                for name_var in name_variations:
                    players.extend(self._extract_players_from_stats_page(soup, name_var, "pitcher"))
        
        # Also check team-specific pages for better coverage
        # Team codes: g (Giants), t (Tigers), db (BayStars), d (Dragons), c (Carp), s (Swallows)
        #             h (Hawks), f (Fighters), m (Marines), l (Lions), e (Eagles), b (Buffaloes)
        team_codes = ['g', 't', 'db', 'd', 'c', 's', 'h', 'f', 'm', 'l', 'e', 'b']
        
        for team_code in team_codes:
            # Check batting stats by team
            batting_url = f"{self.stats_base_url}/{season}/stats/idb1_{team_code}.html"
            html = await self.fetch_page(batting_url)
            if html:
                soup = self.parse_html(html)
                for name_var in name_variations:
                    players.extend(self._extract_players_from_stats_page(soup, name_var, "batter"))
            
            # Check pitching stats by team
            pitching_url = f"{self.stats_base_url}/{season}/stats/idp1_{team_code}.html"
            html = await self.fetch_page(pitching_url)
            if html:
                soup = self.parse_html(html)
                for name_var in name_variations:
                    players.extend(self._extract_players_from_stats_page(soup, name_var, "pitcher"))
        
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
                        
                        # Use consistent ID format: lastname,_firstname (lowercase)
                        if not player_id:
                            # Convert "Otani, Shohei" to "otani,_shohei"
                            player_id = player_name.lower().replace(" ", "_")
                        
                        players.append({
                            "id": player_id,
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
        
        # First try league leader pages
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
                logger.debug(f"Failed to fetch {stat_type} stats from {url}")
                continue
            
            soup = self.parse_html(html)
            
            if stat_type == "batting":
                stats_list.extend(self._extract_batting_stats(soup, season))
            else:
                stats_list.extend(self._extract_pitching_stats(soup, season))
        
        # Also check team-specific pages for more complete data
        team_codes = ['g', 't', 'db', 'd', 'c', 's', 'h', 'f', 'm', 'l', 'e', 'b']
        
        for team_code in team_codes:
            if stat_type == "batting":
                url = f"{self.stats_base_url}/{season}/stats/idb1_{team_code}.html"
            else:
                url = f"{self.stats_base_url}/{season}/stats/idp1_{team_code}.html"
            
            html = await self.fetch_page(url)
            if not html:
                continue
            
            soup = self.parse_html(html)
            
            if stat_type == "batting":
                team_stats = self._extract_batting_stats(soup, season, team_code=team_code)
                # Add stats that aren't already in the list
                for stat in team_stats:
                    if not any(s.get("player_name") == stat.get("player_name") for s in stats_list):
                        stats_list.append(stat)
            else:
                team_stats = self._extract_pitching_stats(soup, season, team_code=team_code)
                for stat in team_stats:
                    if not any(s.get("player_name") == stat.get("player_name") for s in stats_list):
                        stats_list.append(stat)
        
        return stats_list
    
    def _extract_batting_stats(self, soup, season: int, team_code: Optional[str] = None) -> List[Dict[str, Any]]:
        """Extract batting statistics from stats page."""
        stats_list = []
        
        # Find the stats table - NPB site doesn't use classes
        tables = soup.find_all("table")
        if not tables:
            return stats_list
        
        # The first table usually contains the stats
        table = tables[0] if tables else None
        if not table:
            return stats_list
        
        # Extract headers to map column indices
        headers = []
        header_row = table.find("tr")
        if header_row:
            headers = [th.text.strip() for th in header_row.find_all(["th", "td"])]
        
        # Process data rows
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 20:  # NPB team pages have ~24 columns
                continue
            
            # Skip if first cell contains header text
            first_cell_text = cells[0].text.strip()
            if "batter" in first_cell_text.lower() or "switch" in first_cell_text.lower():
                continue
            
            try:
                # First cell might be * for lefty, + for switch, or empty
                # Second cell is player name
                name_cell = cells[1]
                player_name = name_cell.text.strip()
                
                # Skip empty rows
                if not player_name:
                    continue
                
                # Extract player link if available
                player_link = name_cell.find("a")
                player_url = player_link.get("href", "") if player_link else ""
                player_id = self._extract_player_id_from_url(player_url) if player_url else player_name.replace(" ", "_").lower()
                
                # For team pages, we know the team from the URL
                team = team_code.upper() if team_code else ""
                
                # Stats - NPB team page layout (based on actual data)
                # Cells: [0]=*, [1]=name, [2]=G, [3]=PA, [4]=AB, [5]=R, [6]=H, [7]=2B, [8]=3B, [9]=HR, 
                #        [10]=TB, [11]=RBI, [12]=SH, [13]=SF, [14]=SB, [15]=CS, [16]=BB, [17]=HP, [18]=SO, [19]=DP, [20]=GIDP, [21]=BA, [22]=SLG, [23]=OBP
                stats = {
                    "player_id": player_id,
                    "player_name": player_name,
                    "season": season,
                    "team": team,
                    "games": self.safe_int(cells[2].text) if len(cells) > 2 else 0,
                    "plate_appearances": self.safe_int(cells[3].text) if len(cells) > 3 else 0,
                    "at_bats": self.safe_int(cells[4].text) if len(cells) > 4 else 0,
                    "runs": self.safe_int(cells[5].text) if len(cells) > 5 else 0,
                    "hits": self.safe_int(cells[6].text) if len(cells) > 6 else 0,
                    "doubles": self.safe_int(cells[7].text) if len(cells) > 7 else 0,
                    "triples": self.safe_int(cells[8].text) if len(cells) > 8 else 0,
                    "home_runs": self.safe_int(cells[9].text) if len(cells) > 9 else 0,
                    "rbis": self.safe_int(cells[11].text) if len(cells) > 11 else 0,
                    "stolen_bases": self.safe_int(cells[14].text) if len(cells) > 14 else 0,
                    "walks": self.safe_int(cells[16].text) if len(cells) > 16 else 0,
                    "strikeouts": self.safe_int(cells[18].text) if len(cells) > 18 else 0,
                    "batting_average": self.safe_float(cells[21].text) if len(cells) > 21 else 0.0,
                    "slugging_percentage": self.safe_float(cells[22].text) if len(cells) > 22 else 0.0,
                    "on_base_percentage": self.safe_float(cells[23].text) if len(cells) > 23 else 0.0
                }
                
                # Calculate OPS if we have the components
                if stats["batting_average"] > 0 or stats["on_base_percentage"] > 0:
                    stats["ops"] = stats["on_base_percentage"] + stats["slugging_percentage"]
                
                stats_list.append(stats)
                
            except Exception as e:
                logger.debug(f"Error parsing batting stats row: {e}")
                continue
        
        return stats_list
    
    def _extract_pitching_stats(self, soup, season: int, team_code: Optional[str] = None) -> List[Dict[str, Any]]:
        """Extract pitching statistics from stats page."""
        stats_list = []
        
        # Find the stats table - NPB site doesn't use classes
        tables = soup.find_all("table")
        if not tables:
            return stats_list
        
        # The first table usually contains the stats
        table = tables[0] if tables else None
        if not table:
            return stats_list
        
        # Process data rows
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 20:  # NPB team pages have ~24 columns for pitching too
                continue
            
            # Skip if first cell contains header text
            first_cell_text = cells[0].text.strip()
            if "pitcher" in first_cell_text.lower():
                continue
            
            try:
                # First cell might be * for lefty or empty
                # Second cell is player name
                name_cell = cells[1]
                player_name = name_cell.text.strip()
                
                # Skip empty rows
                if not player_name:
                    continue
                
                # Extract player link if available
                player_link = name_cell.find("a")
                player_url = player_link.get("href", "") if player_link else ""
                player_id = self._extract_player_id_from_url(player_url) if player_url else player_name.replace(" ", "_").lower()
                
                # For team pages, we know the team from the URL
                team = team_code.upper() if team_code else ""
                
                # Stats - NPB team pitching page layout
                # Based on actual data: [0]=*, [1]=name, [2]=G, [3]=W, [4]=L, [5]=S, [6]=H, [7]=CG, [8]=SO, [9]=WP%,
                #        [10]=BF, [11]=GF, [12]=IP, [13]=H, [14]=HR, [15]=BB, [16]=HP, [17]=SO, [18]=R, [19]=ER, [20]=WHIP, [21]=K/9, [22]=BB/9, [23]=ERA
                stats = {
                    "player_id": player_id,
                    "player_name": player_name,
                    "season": season,
                    "team": team,
                    "games": self.safe_int(cells[2].text) if len(cells) > 2 else 0,
                    "wins": self.safe_int(cells[3].text) if len(cells) > 3 else 0,
                    "losses": self.safe_int(cells[4].text) if len(cells) > 4 else 0,
                    "saves": self.safe_int(cells[5].text) if len(cells) > 5 else 0,
                    "holds": self.safe_int(cells[6].text) if len(cells) > 6 else 0,
                    "complete_games": self.safe_int(cells[7].text) if len(cells) > 7 else 0,
                    "shutouts": self.safe_int(cells[8].text) if len(cells) > 8 else 0,
                    "innings_pitched": self._convert_innings(cells[11].text.strip() + cells[12].text.strip()) if len(cells) > 12 else 0.0,
                    "hits_allowed": self.safe_int(cells[13].text) if len(cells) > 13 else 0,
                    "home_runs_allowed": self.safe_int(cells[14].text) if len(cells) > 14 else 0,
                    "walks": self.safe_int(cells[15].text) if len(cells) > 15 else 0,
                    "strikeouts": self.safe_int(cells[18].text) if len(cells) > 18 else 0,
                    "runs_allowed": self.safe_int(cells[19].text) if len(cells) > 19 else 0,
                    "earned_runs": self.safe_int(cells[19].text) if len(cells) > 19 else 0,
                    "era": self.safe_float(cells[23].text) if len(cells) > 23 else 0.0,
                }
                
                # Calculate WHIP if not provided
                if stats["innings_pitched"] > 0:
                    stats["whip"] = (stats["hits_allowed"] + stats["walks"]) / stats["innings_pitched"]
                else:
                    stats["whip"] = 0.0
                
                stats_list.append(stats)
                
            except Exception as e:
                logger.debug(f"Error parsing pitching stats row: {e}")
                continue
        
        return stats_list
    
    def _convert_innings(self, innings_str: str) -> float:
        """Convert NPB innings format to decimal.
        
        NPB uses ".1" for 1/3 of an inning and ".2" for 2/3 of an inning.
        """
        if not innings_str:
            return 0.0
        
        innings_str = innings_str.strip()
        if '.' in innings_str:
            whole, fraction = innings_str.split('.')
            whole_innings = self.safe_int(whole)
            
            if fraction == '1':
                return whole_innings + 0.33
            elif fraction == '2':
                return whole_innings + 0.67
            else:
                # Regular decimal
                return self.safe_float(innings_str)
        else:
            return self.safe_float(innings_str)
    
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