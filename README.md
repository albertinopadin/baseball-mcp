# baseball-mcp

MCP (Model Context Protocol) Server for Major League Baseball Data.

## Overview

This MCP server provides access to MLB player data through the official MLB Stats API. It allows you to search for players by name and retrieve detailed information about them.

## Features

- Search for MLB players by name (active and retired)
- Retrieve comprehensive player information including:
  - Personal details (name, age, birthplace, height, weight)
  - Position and jersey number
  - Batting/pitching statistics
  - Career milestones
  - Team affiliations

## Installation

This project uses `uv` for Python package management. To install:

```bash
# Clone the repository
git clone https://github.com/yourusername/baseball-mcp.git
cd baseball-mcp

# Install dependencies with uv
uv sync
```

## Usage

### Running the MCP Server

```bash
uv run baseball_mcp_server.py
```

### Available Tools

#### `search_player`
Search for MLB players by name.

**Parameters:**
- `search_str` (string, required): Name of player to search for

**Example:**
```json
{
  "tool": "search_player",
  "arguments": {
    "search_str": "Jose Altuve"
  }
}
```

## Requirements

- Python 3.12+
- `uv` package manager
- Dependencies listed in `pyproject.toml`

## Development

The project structure:
- `baseball_mcp_server.py` - Main MCP server implementation
- `data_utils.py` - Utilities for interacting with MLB Stats API
- `pyproject.toml` - Project configuration and dependencies

## API Reference

This server uses the official MLB Stats API (statsapi.mlb.com) to retrieve player data.
