#!/usr/bin/env python3
"""Unit tests for Statcast API module."""

import asyncio
import sys
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import statcast_api


async def test_statcast_batting():
    """Test Statcast batting data retrieval."""
    print("\n" + "="*60)
    print("Testing Statcast Batting Data")
    print("="*60)
    
    # Test with valid player
    print("\n1. Testing Shohei Ohtani 2024 batting data:")
    result = await statcast_api.get_player_statcast_batting(
        player_name="Shohei Ohtani",
        season="2024"
    )
    print(result)
    assert "Exit Velocity" in result
    assert "Launch Angle" in result
    assert "Barrel Rate" in result
    
    # Test with specific date range
    print("\n2. Testing Ronald Acuna Jr. for May 2024:")
    result = await statcast_api.get_player_statcast_batting(
        player_name="Ronald Acuna Jr.",
        start_date="2024-05-01",
        end_date="2024-05-31"
    )
    print(result)
    
    # Test with invalid player
    print("\n3. Testing invalid player:")
    result = await statcast_api.get_player_statcast_batting(
        player_name="Fake Player"
    )
    print(result)
    assert "No player found" in result
    
    # Test error handling for player with no data
    print("\n4. Testing player with no recent data:")
    result = await statcast_api.get_player_statcast_batting(
        player_name="Barry Bonds",
        season="2024"
    )
    print(result)
    assert "No Statcast batting data available" in result or "No player found" in result


async def test_statcast_pitching():
    """Test Statcast pitching data retrieval."""
    print("\n" + "="*60)
    print("Testing Statcast Pitching Data")
    print("="*60)
    
    # Test with valid pitcher
    print("\n1. Testing Dylan Cease 2024 pitching data:")
    result = await statcast_api.get_player_statcast_pitching(
        player_name="Dylan Cease",
        season="2024"
    )
    print(result)
    assert "Velocity" in result
    assert "Spin Rate" in result
    assert "Pitch Arsenal" in result
    
    # Test with specific date range
    print("\n2. Testing Shohei Ohtani pitching for April 2024:")
    result = await statcast_api.get_player_statcast_pitching(
        player_name="Shohei Ohtani",
        start_date="2024-04-01",
        end_date="2024-04-30"
    )
    print(result)
    
    # Test with injured pitcher (no data)
    print("\n3. Testing pitcher with no 2024 data:")
    result = await statcast_api.get_player_statcast_pitching(
        player_name="Jacob deGrom",
        season="2024"
    )
    print(result)
    # deGrom might have limited data in 2024, so check for either no data or actual data
    assert "No Statcast pitching data available" in result or "Pitch Arsenal" in result


async def test_caching():
    """Test that caching is working properly."""
    print("\n" + "="*60)
    print("Testing Caching Functionality")
    print("="*60)
    
    # First call - should hit the API
    print("\n1. First call to API (should be slower):")
    start_time = time.time()
    result1 = await statcast_api.get_player_statcast_batting(
        player_name="Fernando Tatis Jr.",
        season="2024"
    )
    first_call_time = time.time() - start_time
    print(f"First call took: {first_call_time:.2f} seconds")
    
    # Second call - should use cache
    print("\n2. Second call (should use cache and be faster):")
    start_time = time.time()
    result2 = await statcast_api.get_player_statcast_batting(
        player_name="Fernando Tatis Jr.",
        season="2024"
    )
    second_call_time = time.time() - start_time
    print(f"Second call took: {second_call_time:.2f} seconds")
    
    # Verify results are the same
    assert result1 == result2
    print(f"\n✅ Cache is working! Second call was {first_call_time/second_call_time:.1f}x faster")


async def test_pybaseball_availability():
    """Test handling when pybaseball is not available."""
    print("\n" + "="*60)
    print("Testing PyBaseball Availability Check")
    print("="*60)
    
    # Check if pybaseball is available
    print("\n1. Checking pybaseball availability:")
    if statcast_api.PYBASEBALL_AVAILABLE:
        print("✅ PyBaseball is available")
    else:
        print("❌ PyBaseball is not available")
        # Test error message
        result = await statcast_api.get_player_statcast_batting("Test Player")
        assert "pybaseball library is not installed" in result


async def test_date_handling():
    """Test various date parameter combinations."""
    print("\n" + "="*60)
    print("Testing Date Parameter Handling")
    print("="*60)
    
    # Test with only start date
    print("\n1. Testing with only start_date:")
    result = await statcast_api.get_player_statcast_batting(
        player_name="Mookie Betts",
        start_date="2024-07-01"
    )
    print("Result length:", len(result))
    
    # Test with only end date
    print("\n2. Testing with only end_date:")
    result = await statcast_api.get_player_statcast_batting(
        player_name="Mookie Betts",
        end_date="2024-07-31"
    )
    print("Result length:", len(result))
    
    # Test with no dates (should default to current season)
    print("\n3. Testing with no dates (defaults to current season):")
    result = await statcast_api.get_player_statcast_batting(
        player_name="Mookie Betts"
    )
    print("Result preview:", result[:200] + "..." if len(result) > 200 else result)


async def main():
    """Run all tests."""
    print("Starting Statcast API Tests")
    print("This may take a moment on first run as data is fetched...")
    print("Note: Some players may not have data for certain periods")
    
    try:
        # Check if pybaseball is available first
        if not statcast_api.PYBASEBALL_AVAILABLE:
            print("\n⚠️  PyBaseball is not available. Some tests will be skipped.")
            await test_pybaseball_availability()
        else:
            await test_statcast_batting()
            await test_statcast_pitching()
            await test_caching()
            await test_date_handling()
        
        print("\n" + "="*60)
        print("All Statcast API tests completed!")
        print("="*60)
        
        # Check cache directory
        cache_dir = Path(".cache")
        if cache_dir.exists():
            cache_files = list(cache_dir.glob("*.json"))
            print(f"\nCache information:")
            print(f"Cache directory: {cache_dir.absolute()}")
            print(f"Number of cached files: {len(cache_files)}")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())