#!/usr/bin/env python3
"""Comprehensive test suite for NPB Phase 2 functionality."""

import asyncio
import sys
sys.path.insert(0, '/Users/albertinopadin/Desktop/Dev/Python Projects/baseball-mcp/src')

from npb.sources.npb_official import NPBOfficialSource
from npb.sources.fangraphs import FanGraphsNPBSource
from npb.aggregator import NPBDataAggregator
from npb.name_utils import normalize_name, match_name, generate_name_variants
from baseball_mcp_server import search_player, get_player_stats, search_teams
from sports_constants import NIPPON_PROFESSIONAL as NPB


async def test_name_utilities():
    """Test Japanese name handling utilities."""
    print("\n=== Testing Name Utilities ===")
    
    # Test normalization
    test_names = [
        ("Munetaka Murakami", "munetaka murakami"),
        ("Shohei Ohtani", "shohei ohtani"),
        ("Yoshinobu Yamamoto", "yoshinobu yamamoto"),
        ("Seiya Suzuki", "seiya suzuki"),
        ("Yu Darvish", "yu darvish")
    ]
    
    print("\nName Normalization:")
    for original, expected in test_names:
        normalized = normalize_name(original)
        print(f"  {original} -> {normalized} {'✓' if normalized == expected else '✗'}")
    
    # Test romanization variants
    print("\nRomanization Variants:")
    variant_tests = [
        "Shohei Ohtani",  # oh -> o
        "Yuuki Takahashi",  # uu -> u
        "Kenta Maeda"
    ]
    
    for name in variant_tests:
        variants = generate_name_variants(name)
        print(f"  {name}: {variants}")
    
    # Test name matching
    print("\nName Matching:")
    match_tests = [
        ("Ohtani", "Shohei Ohtani", True),
        ("shohei ohtani", "Shohei Ohtani", True),
        ("Otani", "Ohtani", True),  # Romanization variant
        ("Yamamoto", "Yoshinobu Yamamoto", True),
        ("Tanaka", "Yamamoto", False)
    ]
    
    for search, candidate, expected in match_tests:
        result = match_name(search, candidate)
        status = '✓' if result == expected else '✗'
        print(f"  '{search}' vs '{candidate}': {result} {status}")


async def test_npb_official_parsing():
    """Test NPB Official source HTML parsing."""
    print("\n\n=== Testing NPB Official Source ===")
    
    source = NPBOfficialSource()
    
    # Test health check
    print("\nHealth Check:")
    is_healthy = await source.health_check()
    print(f"  NPB Official: {'✓ Healthy' if is_healthy else '✗ Unhealthy'}")
    
    # Test player search with different name formats
    print("\nPlayer Search Tests:")
    test_searches = [
        "Murakami",  # Last name only
        "Munetaka Murakami",  # Full name
        "Yamamoto",  # Common last name
        "Ohtani"  # Player who moved to MLB
    ]
    
    for name in test_searches:
        print(f"\n  Searching for '{name}'...")
        players = await source.search_player(name)
        print(f"  Found {len(players)} player(s)")
        for player in players[:3]:  # Show first 3
            print(f"    - {player.name_english} ({player.team.abbreviation if player.team else 'No team'})")
    
    # Test statistics retrieval
    print("\n\nStatistics Retrieval:")
    if len(players) > 0:
        test_player = players[0]
        print(f"  Getting stats for {test_player.name_english}...")
        stats = await source.get_player_stats(test_player.id, stats_type="batting")
        if stats:
            print(f"    Games: {stats.games}")
            print(f"    AVG: {stats.batting_average}")
            print(f"    HR: {stats.home_runs}")
            print(f"    RBI: {stats.rbi}")
        else:
            print("    No stats found")


async def test_fangraphs_source():
    """Test FanGraphs NPB source."""
    print("\n\n=== Testing FanGraphs Source ===")
    
    source = FanGraphsNPBSource()
    
    # Test health check
    print("\nHealth Check:")
    is_healthy = await source.health_check()
    print(f"  FanGraphs: {'✓ Healthy' if is_healthy else '✗ Unhealthy'}")
    
    # Test player search
    print("\nPlayer Search:")
    players = await source.search_player("Murakami")
    print(f"  Found {len(players)} player(s) on FanGraphs")
    for player in players:
        print(f"    - {player.name_english} (ID: {player.id})")


async def test_aggregator():
    """Test NPB data aggregator."""
    print("\n\n=== Testing Data Aggregator ===")
    
    # Initialize aggregator with both sources
    aggregator = NPBDataAggregator()
    
    # Test health checks
    print("\nSource Health Checks:")
    health_status = await aggregator.health_check()
    for source, status in health_status.items():
        print(f"  {source}: {'✓ Healthy' if status else '✗ Unhealthy'}")
    
    # Test aggregated search
    print("\n\nAggregated Player Search:")
    players = await aggregator.search_player("Yamamoto")
    print(f"  Found {len(players)} total player(s) across all sources")
    
    sources_found = set()
    for player in players:
        sources_found.add(player.source)
        print(f"    - {player.name_english} (Source: {player.source})")
    
    print(f"  Data from sources: {', '.join(sources_found)}")
    
    # Test priority handling
    print("\n\nTesting Source Priorities:")
    print("  Default priorities:")
    for op, sources in aggregator.source_priorities.items():
        print(f"    {op}: {' > '.join(sources)}")


async def test_mcp_integration():
    """Test MCP integration with NPB."""
    print("\n\n=== Testing MCP Integration ===")
    
    # Test team search
    print("\nNPB Teams (via MCP):")
    teams_result = await search_teams(sport_id=NPB)
    print(teams_result[:300] + "..." if len(teams_result) > 300 else teams_result)
    
    # Test player search
    print("\n\nNPB Player Search (via MCP):")
    search_names = ["Murakami", "Yamamoto"]
    
    for name in search_names:
        print(f"\n  Searching for '{name}'...")
        result = await search_player(name, sport_id=NPB)
        if "No NPB players found" in result:
            print(f"    {result}")
        else:
            # Show preview
            lines = result.split('\n')
            preview = '\n'.join(lines[:5])
            print(f"    {preview}")
            if len(lines) > 5:
                print("    ...")


async def test_caching():
    """Test caching functionality."""
    print("\n\n=== Testing Cache System ===")
    
    import time
    from cache_utils import get_cached_data, get_cache_key
    
    source = NPBOfficialSource()
    
    # First call - should hit the network
    print("\nFirst call (no cache):")
    start = time.time()
    players1 = await source._parse_batting_stats_page(
        "https://npb.jp/bis/eng/2024/stats/bat_c.html",
        "yamamoto",
        2024,
        "Central"
    )
    time1 = time.time() - start
    print(f"  Time: {time1:.2f}s")
    print(f"  Players found: {len(players1)}")
    
    # Second call - should use cache
    print("\nSecond call (cached):")
    start = time.time()
    players2 = await source._parse_batting_stats_page(
        "https://npb.jp/bis/eng/2024/stats/bat_c.html",
        "yamamoto",
        2024,
        "Central"
    )
    time2 = time.time() - start
    print(f"  Time: {time2:.2f}s")
    print(f"  Cache speedup: {time1/time2:.1f}x faster")
    
    # Verify cache exists
    cache_key = get_cache_key(
        "_parse_batting_stats_page",
        "https://npb.jp/bis/eng/2024/stats/bat_c.html",
        "yamamoto",
        2024,
        "Central"
    )
    cached_data = get_cached_data(cache_key)
    print(f"  Cache exists: {'✓' if cached_data is not None else '✗'}")


async def run_all_tests():
    """Run all Phase 2 tests."""
    print("NPB Phase 2 Comprehensive Test Suite")
    print("=" * 50)
    
    await test_name_utilities()
    await test_npb_official_parsing()
    await test_fangraphs_source()
    await test_aggregator()
    await test_mcp_integration()
    await test_caching()
    
    print("\n\n" + "=" * 50)
    print("All Phase 2 tests completed!")


if __name__ == "__main__":
    asyncio.run(run_all_tests())