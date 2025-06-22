"""Statcast API client for accessing advanced baseball metrics via pybaseball."""
from typing import Optional
from datetime import datetime
import asyncio
from data_utils import format_statcast_batting_data, format_statcast_pitching_data

# Import pybaseball for Statcast data
try:
    from pybaseball import statcast_batter, statcast_pitcher, playerid_lookup
    import pandas as pd
    PYBASEBALL_AVAILABLE = True
except ImportError:
    PYBASEBALL_AVAILABLE = False


async def get_player_statcast_batting(
    player_name: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    season: Optional[str] = None
) -> str:
    """Get Statcast batting metrics for a player including exit velocity, launch angle, and barrel rate.
    
    Args:
        player_name: Full name of the player (e.g., "Aaron Judge")
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
        season: Season year (e.g., "2024"). If not provided with dates, defaults to current season
    """
    if not PYBASEBALL_AVAILABLE:
        return "Statcast data is not available. The pybaseball library is not installed."
    
    # Set default dates if not provided
    if not start_date and not end_date:
        if season:
            start_date = f"{season}-03-20"
            end_date = f"{season}-10-05"
        else:
            # Default to current season
            current_year = datetime.now().year
            start_date = f"{current_year}-03-20"
            end_date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # Parse the player name
        names = player_name.strip().split()
        if len(names) < 2:
            return f"Please provide a full name (first and last name) for {player_name}"
        
        first_name = names[0]
        last_name = " ".join(names[1:])  # Handle names with multiple parts
        
        # Look up player ID using pybaseball
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        
        # Wrap playerid_lookup to handle potential issues
        def lookup_player(last: str, first: str):
            try:
                result = playerid_lookup(last, first)
                # playerid_lookup sometimes returns a string on error
                if isinstance(result, str):
                    return None
                return result
            except Exception:
                return None
        
        player_lookup = await loop.run_in_executor(
            None, 
            lookup_player, 
            last_name, 
            first_name
        )
        
        # Check if player_lookup failed or is empty
        if player_lookup is None:
            return f"No player found matching '{player_name}'"
        
        # Now we know it's a DataFrame, check if empty
        if player_lookup.empty:
            return f"No player found matching '{player_name}'"
        
        # Get the first match (most relevant)
        player_id = int(player_lookup.iloc[0]['key_mlbam'])
        
        # Get Statcast data without caching (DataFrames need special handling for caching)
        statcast_data = await loop.run_in_executor(
            None,
            statcast_batter,
            start_date,
            end_date,
            player_id
        )
        
        if statcast_data is None or statcast_data.empty:
            return f"No Statcast batting data available for {player_name} from {start_date} to {end_date}"
        
        # Format the data
        return format_statcast_batting_data(statcast_data)
        
    except Exception as e:
        return f"Error retrieving Statcast data for {player_name}: {str(e)}"


async def get_player_statcast_pitching(
    player_name: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    season: Optional[str] = None
) -> str:
    """Get Statcast pitching metrics for a player including spin rate, velocity, and pitch movement.
    
    Args:
        player_name: Full name of the player (e.g., "Gerrit Cole")
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
        season: Season year (e.g., "2024"). If not provided with dates, defaults to current season
    """
    if not PYBASEBALL_AVAILABLE:
        return "Statcast data is not available. The pybaseball library is not installed."
    
    # Set default dates if not provided
    if not start_date and not end_date:
        if season:
            start_date = f"{season}-03-20"
            end_date = f"{season}-10-05"
        else:
            # Default to current season
            current_year = datetime.now().year
            start_date = f"{current_year}-03-20"
            end_date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # Parse the player name
        names = player_name.strip().split()
        if len(names) < 2:
            return f"Please provide a full name (first and last name) for {player_name}"
        
        first_name = names[0]
        last_name = " ".join(names[1:])  # Handle names with multiple parts
        
        # Look up player ID using pybaseball
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        
        # Wrap playerid_lookup to handle potential issues
        def lookup_player(last: str, first: str):
            try:
                result = playerid_lookup(last, first)
                # playerid_lookup sometimes returns a string on error
                if isinstance(result, str):
                    return None
                return result
            except Exception:
                return None
        
        player_lookup = await loop.run_in_executor(
            None, 
            lookup_player, 
            last_name, 
            first_name
        )
        
        # Check if player_lookup failed or is empty
        if player_lookup is None:
            return f"No player found matching '{player_name}'"
        
        # Now we know it's a DataFrame, check if empty
        if player_lookup.empty:
            return f"No player found matching '{player_name}'"
        
        # Get the first match (most relevant)
        player_id = int(player_lookup.iloc[0]['key_mlbam'])
        
        # Get Statcast data without caching (DataFrames need special handling for caching)
        statcast_data = await loop.run_in_executor(
            None,
            statcast_pitcher,
            start_date,
            end_date,
            player_id
        )
        
        if statcast_data is None or statcast_data.empty:
            return f"No Statcast pitching data available for {player_name} from {start_date} to {end_date}"
        
        # Format the data
        return format_statcast_pitching_data(statcast_data)
        
    except Exception as e:
        return f"Error retrieving Statcast data for {player_name}: {str(e)}"