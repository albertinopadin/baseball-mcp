#!/usr/bin/env python3
"""Test script for Statcast MCP tools."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from baseball_mcp_server import get_player_statcast_batting, get_player_statcast_pitching


async def test_statcast_batting():
    """Test the Statcast batting data tool."""
    print("\n" + "="*60)
    print("Testing Statcast Batting Data")
    print("="*60)
    
    # Test with Aaron Judge for 2024 season
    print("\n1. Testing Aaron Judge 2024 season stats:")
    result = await get_player_statcast_batting(
        player_name="Aaron Judge",
        season="2024"
    )
    print(result)
    
    # Test with specific date range
    print("\n2. Testing Mookie Betts for June 2024:")
    result = await get_player_statcast_batting(
        player_name="Mookie Betts",
        start_date="2024-06-01",
        end_date="2024-06-30"
    )
    print(result)
    
    # Test caching (should be faster)
    print("\n3. Testing cache - repeating Aaron Judge query:")
    import time
    start_time = time.time()
    result = await get_player_statcast_batting(
        player_name="Aaron Judge",
        season="2024"
    )
    elapsed = time.time() - start_time
    print(f"Query completed in {elapsed:.2f} seconds (should be fast due to cache)")
    
    # Test invalid player
    print("\n4. Testing invalid player name:")
    result = await get_player_statcast_batting(
        player_name="Fake Player"
    )
    print(result)


async def test_statcast_pitching():
    """Test the Statcast pitching data tool."""
    print("\n" + "="*60)
    print("Testing Statcast Pitching Data")
    print("="*60)
    
    # Test with Gerrit Cole for 2024 season
    print("\n1. Testing Gerrit Cole 2024 season stats:")
    result = await get_player_statcast_pitching(
        player_name="Gerrit Cole",
        season="2024"
    )
    print(result)
    
    # Test with specific date range
    print("\n2. Testing Jacob deGrom for May 2024:")
    result = await get_player_statcast_pitching(
        player_name="Jacob deGrom",
        start_date="2024-05-01",
        end_date="2024-05-31"
    )
    print(result)
    
    # Test with Spencer Strider
    print("\n3. Testing Spencer Strider 2024:")
    result = await get_player_statcast_pitching(
        player_name="Spencer Strider",
        season="2024"
    )
    print(result)


async def main():
    """Run all tests."""
    print("Starting Statcast MCP Tools Tests")
    print("This may take a moment on first run as data is fetched...")
    
    try:
        await test_statcast_batting()
        await test_statcast_pitching()
        
        print("\n" + "="*60)
        print("All tests completed!")
        print("="*60)
        
        # Check cache directory
        from pathlib import Path
        cache_dir = Path(".cache")
        if cache_dir.exists():
            cache_files = list(cache_dir.glob("*.json"))
            print(f"\nCache information:")
            print(f"Cache directory: {cache_dir.absolute()}")
            print(f"Number of cached files: {len(cache_files)}")
            
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())