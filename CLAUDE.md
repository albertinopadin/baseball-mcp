# CLAUDE.md - Project Context for Baseball MCP Server

## Project Overview

This is an MCP (Model Context Protocol) server that provides access to Major League Baseball player data through the official MLB Stats API. The server is designed to work with Claude Desktop and other MCP-compatible clients.

## Current Implementation Status

### Completed Features
- Complete MCP server implementation with Python
- Comprehensive MLB Stats API integration with all major endpoints
- **NEW: Full Minor League Support** (v0.0.6):
  - Access data for Triple-A, Double-A, High-A, Single-A, and Rookie leagues
  - Player stats, team rosters, and game schedules for all minor league levels
  - New tool to list all available sports/leagues with their IDs
- **NEW: NPB (Nippon Professional Baseball) Support** (v0.0.8):
  - Player search across Central and Pacific leagues
  - Team information for all 12 NPB teams
  - Player statistics parsing from official NPB website
  - Japanese name search with romanization support
  - Multi-source data aggregation (NPB Official + FanGraphs)
  - Extensible plugin architecture for future sources
- Player functionality:
  - Search players by name (across all levels including NPB)
  - Get detailed player information by ID
  - Retrieve player statistics (career, season, game logs) for MLB, minor leagues, and NPB
  - **NEW: Statcast batting metrics** (exit velocity, launch angle, barrel rate)
  - **NEW: Statcast pitching metrics** (spin rate, velocity, pitch movement)
- Team functionality:
  - Search and list teams from any league (MLB or minor leagues)
  - Get detailed team information
  - View team rosters (active, 40-man, full season)
- Game functionality:
  - View game schedules for any league level
  - Get detailed game boxscores (MLB and minor leagues)
  - Access live game feeds for real-time data (MLB only)
- League functionality:
  - View current standings by league/division (MLB only)
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
  - Baseball Reference (baseball-reference.com) - Historical NPB data (1936-present, web scraping)
  - NPB Official Website (npb.jp) - Japanese baseball data (2008-present, web scraping)
  - FanGraphs International (fangraphs.com) - NPB advanced metrics (placeholder implementation)
- **Protocol**: MCP (Model Context Protocol)
- **Key Dependencies**: httpx, pybaseball, pandas, beautifulsoup4

### Project Structure
```
baseball-mcp/
├── src/
│   ├── baseball_mcp_server.py  # Main MCP server (tool definitions only)
│   ├── mlb_stats_api.py       # MLB Stats API client functions
│   ├── statcast_api.py        # Statcast/pybaseball client functions
│   ├── npb_api.py             # NPB API interface for MCP integration
│   ├── data_utils.py          # Data formatting utilities
│   ├── cache_utils.py         # Caching mechanism
│   ├── sports_api.py          # Sports/leagues information
│   ├── sports_constants.py    # Sport ID constants
│   └── npb/                   # NPB package
│       ├── __init__.py
│       ├── base.py            # Abstract base class for data sources
│       ├── models.py          # NPB data models
│       ├── aggregator.py      # Multi-source data aggregator
│       ├── name_utils.py      # Japanese name handling
│       └── sources/           # Data source implementations
│           ├── __init__.py
│           ├── npb_official.py # NPB official website scraper
│           └── fangraphs.py    # FanGraphs NPB scraper
├── test/
│   ├── test_dodgers_stats.py  # Example test script for Dodgers stats
│   ├── test_statcast.py       # Statcast functionality tests
│   ├── test_mlb_stats_api.py  # Unit tests for MLB Stats API
│   ├── test_statcast_api.py   # Unit tests for Statcast API
│   ├── test_npb_basic.py      # NPB basic functionality tests
│   ├── test_npb_integration.py # NPB MCP integration tests
│   └── test_npb_phase2.py     # NPB Phase 2 comprehensive tests
├── scratchpads/
│   └── npb-stats-scratchpad.md # NPB implementation notes
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

## Future Enhancements

### Potential Features
1. **Advanced Metrics**: Include additional sabermetric statistics (WAR, OPS+, FIP, etc.)
2. **Historical Data**: Enhanced historical season comparisons
3. **Playoff Data**: Specialized playoff/postseason statistics
4. **Draft Data**: MLB draft information and history
5. **Injury Reports**: Player injury status and history
6. **Transactions**: Trade and roster move tracking
7. **Umpire Data**: Umpire statistics and tendencies
8. **Weather Data**: Game-time weather conditions
9. **Venue Details**: Detailed ballpark information
10. **Media Content**: Game highlights and video clips

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

6. **NPB Integration**:
   - Uses `sport_id=31` to access NPB data
   - Supports same tool interfaces as MLB
   - Handles Japanese name formats and romanization
   - Aggregates data from multiple sources

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
  - Web scraping dependent (may break if site structure changes)
  - Limited to data available on public websites
  - Advanced metrics require FanGraphs (not fully implemented)
  - NPB Official source only has data from 2008-present
  - NPB Official only shows players meeting minimum plate appearances (3.1 × team games)
  - Baseball Reference provides full historical data (1936-present) via web scraping
  - Player IDs are generated, not official

## Debugging Tips
- Check API responses in `src/data_utils.py` for troubleshooting
- Verify MCP protocol compliance in `src/baseball_mcp_server.py`
- Use logging to track API calls and responses
- Test with Claude Desktop's MCP debugging tools
- Run example test scripts in `test/` directory

## Version History
- v0.0.11: Added NPB year-by-year statistics support
  - Implemented season-by-season NPB stats retrieval
  - Added yearByYear option for NPB player stats
  - Parse individual seasons from Baseball Reference tables
  - Includes team information for each season
- v0.0.10: Improved NPB player search with smart selection
  - Automatically selects players with NPB stats when multiple matches exist
  - Handles MLB players who also played in NPB (e.g., Alex Cabrera)
  - Concurrent stat checking for better performance
- v0.0.9: Added Baseball Reference integration for historical NPB data (1936-present)
  - Successfully tested with Ichiro Suzuki, Sadaharu Oh, Shohei Ohtani, Tetsuto Yamada
  - Implemented smart search handling for MLB/NPB crossover players
  - Fixed league detection for proper NPB season identification
- v0.0.8: Added NPB (Nippon Professional Baseball) support with web scraping, Japanese name handling
- v0.0.7: Added minor league example screenshot, documentation improvements
- v0.0.6: Added full minor league support with sport IDs, new get_available_sports tool
- v0.0.5: Refactored code into separate modules (mlb_stats_api.py, statcast_api.py), improved testing
- v0.0.4: Added Statcast data integration with pybaseball, implemented caching system
- v0.0.3: Reorganized project structure with src/ and test/ directories
- v0.0.2: Added comprehensive MLB Stats API integration
- v0.0.1: Initial MCP server implementation