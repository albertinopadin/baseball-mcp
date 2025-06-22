import json
import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional, Callable
import functools

CACHE_DIR = Path(".cache")
DEFAULT_TTL_HOURS = 24

def ensure_cache_dir():
    """Ensure the cache directory exists."""
    CACHE_DIR.mkdir(exist_ok=True)

def get_cache_key(func_name: str, *args, **kwargs) -> str:
    """Generate a unique cache key based on function name and arguments."""
    key_parts = [func_name]
    key_parts.extend(str(arg) for arg in args)
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    key_string = "|".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()

def is_cache_valid(timestamp: str, ttl_hours: int = DEFAULT_TTL_HOURS) -> bool:
    """Check if cached data is still valid based on TTL."""
    cached_time = datetime.fromisoformat(timestamp)
    return datetime.now() - cached_time < timedelta(hours=ttl_hours)

def get_cached_data(cache_key: str, ttl_hours: int = DEFAULT_TTL_HOURS) -> Optional[Any]:
    """Retrieve cached data if it exists and is valid."""
    ensure_cache_dir()
    cache_file = CACHE_DIR / f"{cache_key}.json"
    
    if not cache_file.exists():
        return None
    
    try:
        with open(cache_file, 'r') as f:
            cached = json.load(f)
        
        if is_cache_valid(cached['timestamp'], ttl_hours):
            return cached['data']
        else:
            # Cache expired, remove it
            cache_file.unlink()
            return None
    except (json.JSONDecodeError, KeyError):
        # Invalid cache file, remove it
        cache_file.unlink()
        return None

def save_to_cache(cache_key: str, data: Any):
    """Save data to cache with current timestamp."""
    ensure_cache_dir()
    cache_file = CACHE_DIR / f"{cache_key}.json"
    
    cache_data = {
        'timestamp': datetime.now().isoformat(),
        'data': data
    }
    
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f, indent=2, default=str)

def cache_result(ttl_hours: int = DEFAULT_TTL_HOURS):
    """Decorator to cache function results."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = get_cache_key(func.__name__, *args, **kwargs)
            
            # Check cache first
            cached_data = get_cached_data(cache_key, ttl_hours)
            if cached_data is not None:
                return cached_data
            
            # Call the original function
            result = await func(*args, **kwargs)
            
            # Save to cache if result is not None
            if result is not None:
                save_to_cache(cache_key, result)
            
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = get_cache_key(func.__name__, *args, **kwargs)
            
            # Check cache first
            cached_data = get_cached_data(cache_key, ttl_hours)
            if cached_data is not None:
                return cached_data
            
            # Call the original function
            result = func(*args, **kwargs)
            
            # Save to cache if result is not None
            if result is not None:
                save_to_cache(cache_key, result)
            
            return result
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

def clear_cache():
    """Clear all cached data."""
    if CACHE_DIR.exists():
        for cache_file in CACHE_DIR.glob("*.json"):
            cache_file.unlink()

def clear_expired_cache(ttl_hours: int = DEFAULT_TTL_HOURS):
    """Clear only expired cache entries."""
    if not CACHE_DIR.exists():
        return
    
    for cache_file in CACHE_DIR.glob("*.json"):
        try:
            with open(cache_file, 'r') as f:
                cached = json.load(f)
            
            if not is_cache_valid(cached['timestamp'], ttl_hours):
                cache_file.unlink()
        except (json.JSONDecodeError, KeyError):
            # Invalid cache file, remove it
            cache_file.unlink()

# Import asyncio only if needed
import asyncio