# CLAUDE.md - Project Context for Baseball MCP Server

## Project Overview

This is an MCP (Model Context Protocol) server that provides access to Major League Baseball player data through the official MLB Stats API. The server is designed to work with Claude Desktop and other MCP-compatible clients.

## Current Implementation Status

### Completed Features
- Basic MCP server setup with Python
- Player search functionality using MLB Stats API
- Comprehensive player data retrieval including:
  - Personal information (name, age, birthplace, etc.)
  - Physical attributes (height, weight)
  - Position and jersey number
  - Career statistics
  - Team affiliations
  - Active/retired status

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
1. **Team Data**: Add tools for retrieving team information and rosters
2. **Game Statistics**: Implement game scores and schedules
3. **Season Stats**: Add season-by-season player statistics
4. **Advanced Metrics**: Include sabermetric statistics (WAR, OPS+, etc.)
5. **Historical Data**: Access to historical seasons and records
6. **Live Game Data**: Real-time game updates and play-by-play

### Technical Improvements
- Add caching to reduce API calls
- Implement rate limiting protection
- Add comprehensive error handling
- Create unit tests for all components
- Add logging for debugging

## MCP Integration Notes

### Current Tools
- `search_player`: Searches for players by name and returns detailed information

### Tool Response Format
Each player result includes:
- ID and API link
- Full name and nicknames
- Birth information
- Physical attributes
- Position details
- Batting/pitching preferences
- MLB debut date
- Active status

## Known Limitations
- Currently only supports player search (no team or game data)
- No caching mechanism (each search hits the API)
- Limited to data available through MLB Stats API
- No authentication required (public API)

## Debugging Tips
- Check API responses in `data_utils.py` for troubleshooting
- Verify MCP protocol compliance in `baseball_mcp_server.py`
- Use logging to track API calls and responses
- Test with Claude Desktop's MCP debugging tools