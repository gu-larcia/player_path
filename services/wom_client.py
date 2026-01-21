"""WiseOldMan API client for player data."""

import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests


def parse_wom_datetime(dt_string: Optional[str]) -> Optional[datetime]:
    """Parse WOM API datetime string to Python datetime."""
    if not dt_string:
        return None
    try:
        # Handle ISO format with Z suffix
        if dt_string.endswith("Z"):
            dt_string = dt_string[:-1] + "+00:00"
        return datetime.fromisoformat(dt_string.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


class WOMClient:
    """Client for WiseOldMan API v2."""
    
    def __init__(
        self,
        base_url: str = "https://api.wiseoldman.net/v2",
        api_key: Optional[str] = None,
        user_agent: str = "OSRS-Player-Analytics/1.0"
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.user_agent = user_agent
        self.session = requests.Session()
        
        # Set up headers
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Accept": "application/json",
        })
        
        if self.api_key:
            self.session.headers["x-api-key"] = self.api_key
        
        # Rate limiting
        self._last_request_time = 0
        self._min_request_interval = 0.1 if api_key else 0.5  # seconds
    
    def _rate_limit(self):
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_request_interval:
            time.sleep(self._min_request_interval - elapsed)
        self._last_request_time = time.time()
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make an API request with rate limiting."""
        self._rate_limit()
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, timeout=30, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            elif e.response.status_code == 429:
                raise Exception("Rate limit exceeded. Please wait and try again.")
            raise Exception(f"API error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Return current rate limit configuration."""
        return {
            "has_api_key": bool(self.api_key),
            "rate_limit": "100/min" if self.api_key else "20/min",
            "request_interval": self._min_request_interval,
        }
    
    # Player endpoints
    def search_players(self, username: str) -> List[Dict]:
        """Search for players by username."""
        result = self._request("GET", "/players/search", params={"username": username})
        return result if result else []
    
    def get_player(self, username: str) -> Optional[Dict]:
        """Get player details by username."""
        return self._request("GET", f"/players/{username}")
    
    def get_player_by_id(self, player_id: int) -> Optional[Dict]:
        """Get player details by ID."""
        return self._request("GET", f"/players/id/{player_id}")
    
    def get_player_details(self, username: str) -> Optional[Dict]:
        """Get detailed player data including latest snapshot."""
        return self._request("GET", f"/players/{username}")
    
    def get_player_snapshots(
        self,
        username: str,
        period: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Get player snapshots (historical data).
        
        Args:
            username: Player username
            period: One of 'day', 'week', 'month', 'year', '5min'
            start_date: ISO format date string
            end_date: ISO format date string
        """
        params = {}
        if period:
            params["period"] = period
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        
        result = self._request("GET", f"/players/{username}/snapshots", params=params or None)
        return result if result else []
    
    def get_player_gains(
        self,
        username: str,
        period: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get XP/KC gains for a player over a time period.
        
        Args:
            username: Player username
            period: One of 'day', 'week', 'month', 'year'
            start_date: ISO format date string
            end_date: ISO format date string
        """
        params = {}
        if period:
            params["period"] = period
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        
        return self._request("GET", f"/players/{username}/gained", params=params or None)
    
    def get_player_achievements(self, username: str) -> List[Dict]:
        """Get player achievements/milestones."""
        result = self._request("GET", f"/players/{username}/achievements")
        return result if result else []
    
    def get_player_achievement_progress(self, username: str) -> List[Dict]:
        """Get player achievement progress."""
        result = self._request("GET", f"/players/{username}/achievements/progress")
        return result if result else []
    
    def get_player_competitions(self, username: str) -> List[Dict]:
        """Get competitions the player has participated in."""
        result = self._request("GET", f"/players/{username}/competitions")
        return result if result else []
    
    def get_player_groups(self, username: str) -> List[Dict]:
        """Get groups the player belongs to."""
        result = self._request("GET", f"/players/{username}/groups")
        return result if result else []
    
    def get_player_records(self, username: str, period: Optional[str] = None, metric: Optional[str] = None) -> List[Dict]:
        """Get player records (best gains in a period)."""
        params = {}
        if period:
            params["period"] = period
        if metric:
            params["metric"] = metric
        
        result = self._request("GET", f"/players/{username}/records", params=params or None)
        return result if result else []
    
    # Efficiency data
    def get_efficiency_rates(self) -> Optional[Dict]:
        """Get current EHP/EHB rates."""
        return self._request("GET", "/efficiency/rates")
