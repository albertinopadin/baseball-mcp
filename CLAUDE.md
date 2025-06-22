# CLAUDE.md - Project Context for Baseball MCP Server

## Project Overview

This is an MCP (Model Context Protocol) server that provides access to Major League Baseball player data through the official MLB Stats API. The server is designed to work with Claude Desktop and other MCP-compatible clients.

## Current Implementation Status

### Completed Features
- Complete MCP server implementation with Python
- Comprehensive MLB Stats API integration with all major endpoints
- Player functionality:
  - Search players by name
  - Get detailed player information by ID
  - Retrieve player statistics (career, season, game logs)
  - **NEW: Statcast batting metrics** (exit velocity, launch angle, barrel rate)
  - **NEW: Statcast pitching metrics** (spin rate, velocity, pitch movement)
- Team functionality:
  - Search and list all MLB teams
  - Get detailed team information
  - View team rosters (active, 40-man, full season)
- Game functionality:
  - View game schedules with flexible date filtering
  - Get detailed game boxscores
  - Access live game feeds for real-time data
- League functionality:
  - View current standings by league/division
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
- **Protocol**: MCP (Model Context Protocol)
- **Key Dependencies**: httpx, pybaseball, pandas

### Project Structure
```
baseball-mcp/
├── src/
│   ├── baseball_mcp_server.py  # Main MCP server (tool definitions only)
│   ├── mlb_stats_api.py       # MLB Stats API client functions
│   ├── statcast_api.py        # Statcast/pybaseball client functions
│   ├── data_utils.py          # Data formatting utilities
│   └── cache_utils.py         # Caching mechanism
├── test/
│   ├── test_dodgers_stats.py  # Example test script for Dodgers stats
│   ├── test_statcast.py       # Statcast functionality tests
│   ├── test_mlb_stats_api.py  # Unit tests for MLB Stats API
│   └── test_statcast_api.py   # Unit tests for Statcast API
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
1. **Player Tools**:
   - `search_player`: Search for players by name
   - `get_player`: Get detailed player information by ID
   - `get_player_stats`: Retrieve player statistics
   - `get_player_statcast_batting`: Get Statcast batting metrics (exit velocity, launch angle, etc.)
   - `get_player_statcast_pitching`: Get Statcast pitching metrics (spin rate, velocity, etc.)

2. **Team Tools**:
   - `search_teams`: Search and filter MLB teams
   - `get_team`: Get detailed team information
   - `get_team_roster`: View team rosters

3. **Game Tools**:
   - `get_schedule`: View game schedules
   - `get_game_info`: Get game boxscore data
   - `get_live_game_feed`: Access live game data

4. **League Tools**:
   - `get_standings`: View league/division standings

### Tool Response Format
All tools return formatted, human-readable responses with relevant data organized by category. Error handling is implemented for all API calls.

## Known Limitations
- ~~No caching mechanism (each request hits the API)~~ ✅ Fixed in v0.0.4
- Limited to data available through MLB Stats API and Baseball Savant
- No authentication required (public API)
- Rate limiting not implemented (relies on API's built-in limits)
- No webhook support for real-time updates
- DataFrames from pybaseball are not cached (JSON serialization limitation)

## Debugging Tips
- Check API responses in `src/data_utils.py` for troubleshooting
- Verify MCP protocol compliance in `src/baseball_mcp_server.py`
- Use logging to track API calls and responses
- Test with Claude Desktop's MCP debugging tools
- Run example test scripts in `test/` directory

## Version History
- v0.0.5: Refactored code into separate modules (mlb_stats_api.py, statcast_api.py), improved testing
- v0.0.4: Added Statcast data integration with pybaseball, implemented caching system
- v0.0.3: Reorganized project structure with src/ and test/ directories
- v0.0.2: Added comprehensive MLB Stats API integration
- v0.0.1: Initial MCP server implementation