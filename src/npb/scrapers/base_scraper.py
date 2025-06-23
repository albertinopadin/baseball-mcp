"""Base scraper class for NPB web scraping."""

import httpx
import asyncio
from typing import Optional, Dict, Any, List
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import random

logger = logging.getLogger(__name__)


class BaseScraper:
    """Base class for NPB web scrapers with common functionality."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session: Optional[httpx.AsyncClient] = None
        self.rate_limit_delay = 0.5  # seconds between requests
        self.last_request_time = 0.0
        
        # User agents for rotation
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.aclose()
    
    async def _rate_limit(self):
        """Enforce rate limiting between requests."""
        current_time = asyncio.get_event_loop().time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.rate_limit_delay:
            delay = self.rate_limit_delay - time_since_last_request
            await asyncio.sleep(delay)
        
        self.last_request_time = asyncio.get_event_loop().time()
    
    def _get_random_user_agent(self) -> str:
        """Get a random user agent."""
        return random.choice(self.user_agents)
    
    async def fetch_page(self, url: str, **kwargs) -> Optional[str]:
        """Fetch a web page with rate limiting and error handling.
        
        Args:
            url: URL to fetch
            **kwargs: Additional arguments for httpx request
            
        Returns:
            Page HTML content or None on error
        """
        if not self.session:
            raise RuntimeError("Scraper must be used as async context manager")
        
        await self._rate_limit()
        
        # Update headers with random user agent
        headers = kwargs.get("headers", {})
        headers["User-Agent"] = self._get_random_user_agent()
        kwargs["headers"] = headers
        
        try:
            logger.debug(f"Fetching URL: {url}")
            response = await self.session.get(url, **kwargs)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content into BeautifulSoup object.
        
        Args:
            html: HTML content
            
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, "html.parser")
    
    def safe_float(self, value: Any, default: float = 0.0) -> float:
        """Safely convert value to float.
        
        Args:
            value: Value to convert
            default: Default value if conversion fails
            
        Returns:
            Float value
        """
        if value is None or value == "" or value == "-":
            return default
        try:
            # Remove any commas from numbers
            if isinstance(value, str):
                value = value.replace(",", "")
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def safe_int(self, value: Any, default: int = 0) -> int:
        """Safely convert value to int.
        
        Args:
            value: Value to convert
            default: Default value if conversion fails
            
        Returns:
            Integer value
        """
        if value is None or value == "" or value == "-":
            return default
        try:
            # Remove any commas from numbers
            if isinstance(value, str):
                value = value.replace(",", "")
            return int(float(value))  # Handle decimal strings
        except (ValueError, TypeError):
            return default
    
    def extract_table_data(self, soup: BeautifulSoup, table_id: Optional[str] = None) -> List[Dict[str, str]]:
        """Extract data from an HTML table.
        
        Args:
            soup: BeautifulSoup object
            table_id: Optional table ID to find specific table
            
        Returns:
            List of dictionaries with table data
        """
        if table_id:
            table = soup.find("table", {"id": table_id})
        else:
            table = soup.find("table")
        
        if not table:
            return []
        
        # Extract headers
        headers = []
        header_row = table.find("thead", recursive=True)
        if header_row:
            header_row = header_row.find("tr")
            if header_row:
                headers = [th.text.strip() for th in header_row.find_all(["th", "td"])]
        
        # Extract data rows
        data = []
        tbody = table.find("tbody")
        if tbody:
            for row in tbody.find_all("tr"):
                row_data = {}
                cells = row.find_all(["td", "th"])
                for i, cell in enumerate(cells):
                    if i < len(headers):
                        row_data[headers[i]] = cell.text.strip()
                if row_data:  # Only add non-empty rows
                    data.append(row_data)
        
        return data