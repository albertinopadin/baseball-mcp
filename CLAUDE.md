# CLAUDE.md - Project Context for Baseball MCP Server

## Project Overview

This is an MCP (Model Context Protocol) server that provides access to baseball data from multiple leagues:
- **MLB and Minor League Baseball** through the official MLB Stats API
- **Nippon Professional Baseball (NPB)** through web scraping of official statistics

The server is designed to work with Claude Desktop and other MCP-compatible clients, providing comprehensive baseball statistics across different leagues and countries.

## Current Implementation Status

### Completed Features
- Complete MCP server implementation with Python
- Comprehensive MLB Stats API integration with all major endpoints
- **NEW: Full Minor League Support** (v0.0.6):
  - Access data for Triple-A, Double-A, High-A, Single-A, and Rookie leagues
  - Player stats, team rosters, and game schedules for all minor league levels
  - New tool to list all available sports/leagues with their IDs
- **NEW: NPB (Japanese Baseball) Support** (v0.0.8-0.0.9):
  - Search for NPB players by name
  - Retrieve batting and pitching statistics
  - Support for historical NPB data
  - Web scraping from official NPB statistics site
  - Name variation handling (e.g., Ohtani/Otani)
  - **NEW: Historical database for pre-2005 players** (v0.0.9):
    - Local SQLite database with historical player data
    - Sample data includes Ichiro (1992-2000), Sadaharu Oh, Tetsuharu Kawakami
    - Composite provider seamlessly combines historical + modern data
  - **NEW: Advanced metrics calculator** (v0.0.9):
    - FIP (Fielding Independent Pitching) with NPB-specific constant
    - wOBA (Weighted On-Base Average) with NPB linear weights
    - OPS+ and ERA+ (league-adjusted stats)
    - Basic WAR estimates (simplified without defensive metrics)
- Player functionality:
  - Search players by name (across all levels including NPB)
  - Get detailed player information by ID
  - Retrieve player statistics (career, season, game logs) for MLB, minor leagues, and NPB
  - **NEW: Statcast batting metrics** (exit velocity, launch angle, barrel rate)
  - **NEW: Statcast pitching metrics** (spin rate, velocity, pitch movement)
- Team functionality:
  - Search and list teams from any league (MLB, minor leagues, or NPB)
  - Get detailed team information
  - View team rosters (active, 40-man, full season)
- Game functionality:
  - View game schedules for any league level
  - Get detailed game boxscores (MLB and minor leagues)
  - Access live game feeds for real-time data (MLB only)
- League functionality:
  - View current standings by league/division (MLB and NPB)
  - Support for different standings types
- **NEW: Caching system**:
  - File-based JSON cache with 24-hour TTL
  - Improves performance for repeated requests
  - Automatic cache invalidation

### Technical Details
- **Language**: Python 3.12
- **Package Manager**: uv
- **APIs**: 
  - MLB Stats API (statsapi.mlb.com) - Player, team, and game data
  - Baseball Savant (via pybaseball) - Statcast metrics
  - NPB Official Site (npb.jp) - Japanese baseball statistics via web scraping
- **Protocol**: MCP (Model Context Protocol)
- **Key Dependencies**: httpx, pybaseball, pandas, beautifulsoup4

### Project Structure
```
baseball-mcp/
├── src/
│   ├── baseball_mcp_server.py  # Main MCP server (tool definitions only)
│   ├── mlb_stats_api.py       # MLB Stats API client functions
│   ├── statcast_api.py        # Statcast/pybaseball client functions
│   ├── data_utils.py          # Data formatting utilities
│   ├── cache_utils.py         # Caching mechanism
│   └── npb/                   # NPB (Japanese baseball) module
│       ├── __init__.py        # Module initialization
│       ├── api.py             # NPB API interface
│       ├── constants.py       # NPB teams and league constants
│       ├── data_formatters.py # NPB data formatting utilities
│       ├── data/              # Historical data management
│       │   ├── __init__.py
│       │   ├── database.py    # SQLite database manager
│       │   ├── historical_data.py # Sample historical player data
│       │   ├── schema.sql     # Database schema
│       │   └── metrics/       # Advanced metrics calculators
│       │       ├── __init__.py
│       │       ├── calculator.py # NPB metrics calculations
│       │       └── constants.py  # NPB-specific constants
│       ├── providers/         # Data provider implementations
│       │   ├── base.py        # Abstract base provider
│       │   ├── scraper_provider.py # Web scraping provider
│       │   ├── historical_provider.py # Local database provider
│       │   └── composite_provider.py  # Combines historical + modern
│       └── scrapers/          # Web scraping implementations
│           ├── base_scraper.py # Base scraper class
│           ├── npb_official.py # NPB official site scraper
│           └── baseball_reference.py # Baseball-Reference scraper (backup)
├── test/
│   ├── test_dodgers_stats.py  # Example test script for Dodgers stats
│   ├── test_statcast.py       # Statcast functionality tests
│   ├── test_mlb_stats_api.py  # Unit tests for MLB Stats API
│   ├── test_statcast_api.py   # Unit tests for Statcast API
│   ├── test_npb_api.py        # Unit tests for NPB API
│   └── test_search_ohtani.py  # Example NPB search test
├── scratchpads/               # Development notes and research
│   └── npb-stats-scratchpad.md # NPB implementation research
├── .cache/                    # Cache directory (gitignored)
├── pyproject.toml             # Project configuration
├── uv.lock                    # Dependency lock file
├── README.md                  # User documentation
└── CLAUDE.md                  # This file
```

## Development Guidelines

### Code Standards
- Follow PEP 8 for Python code style
- Use type hints for function parameters and return values
- Keep functions focused and single-purpose
- Handle API errors gracefully
- Maintain separation of concerns (MCP tools, API clients, utilities)

### Testing Approach
- Test with various player names (active, retired, partial matches)
- Verify proper handling of API rate limits
- Ensure graceful error handling for network issues
- Test Statcast data retrieval and caching functionality
- Verify cache TTL and invalidation
- Test NPB name variations (e.g., Ohtani/Otani)
- Verify NPB scraping handles different table structures

## Future Enhancements

### Potential Features
1. ~~**Advanced Metrics**: Include additional sabermetric statistics (WAR, OPS+, FIP, etc.)~~ ✅ Partially completed for NPB
2. ~~**Historical Data**: Enhanced historical season comparisons~~ ✅ Completed for NPB with local database
3. **Playoff Data**: Specialized playoff/postseason statistics
4. **Draft Data**: MLB draft information and history
5. **Injury Reports**: Player injury status and history
6. **Transactions**: Trade and roster move tracking
7. **Umpire Data**: Umpire statistics and tendencies
8. **Weather Data**: Game-time weather conditions
9. **Venue Details**: Detailed ballpark information
10. **Media Content**: Game highlights and video clips
11. **Expand NPB Historical Data**: Import more complete datasets from community sources
12. **Commercial API Integration**: Add support for Sportradar or other paid APIs

### Technical Improvements
- ~~Implement intelligent caching with TTL~~ ✅ Completed in v0.0.4
- Add rate limiting protection
- Create comprehensive unit and integration tests
- Add structured logging with log levels
- Implement request retry logic with exponential backoff
- Add request timeout handling
- Create data validation schemas
- Add performance monitoring

## MCP Integration Notes

### Current Tools
1. **Sports/League Tools**:
   - `get_available_sports`: List all available sports/leagues with their IDs

2. **Player Tools**:
   - `search_player`: Search for players by name (all levels)
   - `get_player`: Get detailed player information by ID
   - `get_player_stats`: Retrieve player statistics (MLB and minor leagues)
   - `get_player_statcast_batting`: Get Statcast batting metrics (exit velocity, launch angle, etc.)
   - `get_player_statcast_pitching`: Get Statcast pitching metrics (spin rate, velocity, etc.)

3. **Team Tools**:
   - `search_teams`: Search and filter teams (MLB and minor leagues)
   - `get_team`: Get detailed team information
   - `get_team_roster`: View team rosters

4. **Game Tools**:
   - `get_schedule`: View game schedules (MLB and minor leagues)
   - `get_game_info`: Get game boxscore data (MLB and minor leagues)
   - `get_live_game_feed`: Access live game data (MLB only)

5. **League Tools**:
   - `get_standings`: View league/division standings (MLB only)

6. **NPB Tools**:
   - `search_npb_player`: Search for NPB players by name
   - `get_npb_player_stats`: Get NPB player statistics (batting and pitching)
   - `get_npb_teams`: Get list of all NPB teams

### Tool Response Format
All tools return formatted, human-readable responses with relevant data organized by category. Error handling is implemented for all API calls.

### Minor League Usage
To access minor league data, use the appropriate sport_id parameter:
- **Triple-A (AAA)**: sport_id=11
- **Double-A (AA)**: sport_id=12
- **High-A (A+)**: sport_id=13
- **Single-A (A)**: sport_id=14
- **Rookie (R)**: sport_id=16

Example queries:
- Get Triple-A teams: `search_teams(sport_id=11)`
- Get Double-A player stats: `get_player_stats(person_id=123456, sport_id=12, stats="season")`
- Get Single-A schedule: `get_schedule(sport_id=14, start_date="2024-06-01", end_date="2024-06-07")`

Use `get_available_sports()` to see all available leagues and their IDs.

### NPB Usage
To access NPB (Japanese baseball) data:
- Use `search_npb_player()` to find players
- Player IDs from search results can be used with `get_npb_player_stats()`
- Season parameter is optional (defaults to current season)
- Handles name variations automatically (e.g., Ohtani/Otani)
- Supports ID format variations (e.g., "otani-000sho", "otani,_shohei")

Example NPB queries:
- Search for player: `search_npb_player("Shohei Ohtani")`
- Get 2017 stats: `get_npb_player_stats("otani-000sho", "2017")`
- Get all NPB teams: `get_npb_teams()`

Note: The NPB integration uses web scraping from the official NPB statistics site (npb.jp) and handles various player ID formats for compatibility.

## Known Limitations
- ~~No caching mechanism (each request hits the API)~~ ✅ Fixed in v0.0.4
- Limited to data available through MLB Stats API and Baseball Savant
- No authentication required (public API)
- Rate limiting not implemented (relies on API's built-in limits)
- No webhook support for real-time updates
- DataFrames from pybaseball are not cached (JSON serialization limitation)
- Minor league limitations:
  - Standings not available for minor leagues
  - Live game feeds only available for MLB games
  - YearByYear stats only show MLB history
  - Statcast data only available for MLB players
- NPB limitations:
  - Data obtained via web scraping (no official API)
  - Limited to statistics available on NPB official site
  - No advanced metrics (xWOBA, spin rates) for NPB
  - Historical data may be incomplete for older seasons
  - Player IDs must be obtained through search first

## Debugging Tips
- Check API responses in `src/data_utils.py` for troubleshooting
- Verify MCP protocol compliance in `src/baseball_mcp_server.py`
- Use logging to track API calls and responses
- Test with Claude Desktop's MCP debugging tools
- Run example test scripts in `test/` directory

## Version History
- v0.0.8: Added NPB (Japanese baseball) support with web scraping from official NPB site
  - Fixed player ID format handling for NPB stats retrieval
  - Added support for name variations (Ohtani/Otani)
  - Implemented season-by-season stats retrieval
  - Enhanced web scraping reliability
- v0.0.7: Added minor league example screenshot, documentation improvements
- v0.0.6: Added full minor league support with sport IDs, new get_available_sports tool
- v0.0.5: Refactored code into separate modules (mlb_stats_api.py, statcast_api.py), improved testing
- v0.0.4: Added Statcast data integration with pybaseball, implemented caching system
- v0.0.3: Reorganized project structure with src/ and test/ directories
- v0.0.2: Added comprehensive MLB Stats API integration
- v0.0.1: Initial MCP server implementation