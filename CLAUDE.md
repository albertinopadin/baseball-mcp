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

### Technical Details
- **Language**: Python 3.12
- **Package Manager**: uv
- **API**: MLB Stats API (statsapi.mlb.com)
- **Protocol**: MCP (Model Context Protocol)

### Project Structure
```
baseball-mcp/
├── baseball_mcp_server.py  # Main MCP server implementation
├── data_utils.py          # MLB Stats API utilities
├── pyproject.toml         # Project configuration
├── uv.lock               # Dependency lock file
├── README.md             # User documentation
└── CLAUDE.md            # This file
```

## Development Guidelines

### Code Standards
- Follow PEP 8 for Python code style
- Use type hints for function parameters and return values
- Keep functions focused and single-purpose
- Handle API errors gracefully

### Testing Approach
- Test with various player names (active, retired, partial matches)
- Verify proper handling of API rate limits
- Ensure graceful error handling for network issues

## Future Enhancements

### Potential Features
1. **Advanced Metrics**: Include sabermetric statistics (WAR, OPS+, FIP, etc.)
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
- Implement intelligent caching with TTL
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
- No caching mechanism (each request hits the API)
- Limited to data available through MLB Stats API
- No authentication required (public API)
- Rate limiting not implemented (relies on API's built-in limits)
- No webhook support for real-time updates

## Debugging Tips
- Check API responses in `data_utils.py` for troubleshooting
- Verify MCP protocol compliance in `baseball_mcp_server.py`
- Use logging to track API calls and responses
- Test with Claude Desktop's MCP debugging tools