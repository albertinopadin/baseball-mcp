# NPB Stats Integration Research Scratchpad

## Research Started: 2025-06-23

### Initial Observations

From analyzing the baseball-mcp codebase:
- Current architecture uses MLB Stats API (statsapi.mlb.com) for MLB/minor league data
- Statcast integration via pybaseball for advanced metrics
- Modular design with separate API clients, data formatters, and MCP server layer
- File-based caching with 24-hour TTL
- Sport ID system for different leagues (MLB=1, AAA=11, AA=12, etc.)

### Research Goals

1. Find reliable NPB statistics APIs or data sources
2. Determine availability of:
   - Traditional stats (AVG, HR, RBI, hits, ERA, strikeouts)
   - Advanced metrics (WAR, xWOBA, hard hit rate, pitch spin rate, FIP)
3. Evaluate implementation approaches that fit current architecture
4. Consider caching strategies for NPB data

### NPB Background

- Nippon Professional Baseball (NPB) is Japan's highest level of baseball
- 12 teams split into Central League and Pacific League
- Season runs March/April through October
- Known for high-quality play and unique style

---

## NPB Data Sources Investigation

### 1. Official NPB Website Research

- Official site: npb.jp (has English version at npb.jp/eng/)
- **NO PUBLIC API** - Confirmed through extensive research
- Website provides HTML pages with statistics only
- Would require web scraping for data extraction

### 2. pybaseball Library NPB Support

**CONFIRMED: pybaseball does NOT support NPB data**
- pybaseball is MLB-focused only (Baseball Reference, Baseball Savant, FanGraphs)
- No current plans or open issues for NPB integration
- Created by James LeDoux for MLB Advanced Media

### 3. Available NPB Data Sources

#### Free/Open Source Options:

1. **armstjc/Nippon-Baseball-Data-Repository** (GitHub)
   - Provides JSON files for game play-by-play data
   - Python scripts for schedules, standings, player stats
   - Actively maintained repository
   - Data format: JSON

2. **atsukoba/NPB-baseballstats** (GitHub)
   - Contains getNPB.py script that scrapes npb.jp
   - Uses BeautifulSoup4 and requests
   - Covers data from 1950-2017
   - Includes Jupyter notebooks for analysis

3. **Baseball-Reference.com/register/npb-stats.shtml**
   - Comprehensive NPB stats from 1936-present
   - Central & Pacific League coverage
   - HTML-based (requires scraping)
   - Likely includes some advanced metrics

4. **BaseballGuru.com**
   - Downloadable CSV files and spreadsheets
   - Includes sabermetric stats
   - Historical NPB data

#### Commercial APIs:

1. **Sportradar Global Baseball API**
   - Professional-grade API
   - Includes NPB, KBO, World Baseball Classic
   - Real-time data feeds
   - Paid service

2. **OddsMatrix Baseball API**
   - Covers NPB League
   - 45+ betting markets
   - XML feeds and push/pull options
   - Paid service

3. **LSports Baseball Data API**
   - "Fastest and most reliable" API
   - NPB coverage
   - 100+ bookmakers
   - Paid service

### 4. Advanced Metrics Availability

**Traditional Stats**: Widely available (AVG, HR, RBI, ERA, etc.)
- Available from most sources above

**Advanced Calculated Metrics**: Limited availability
- WAR - Possibly available from Baseball-Reference or calculated sources
- FIP - Likely available from specialized sites like NPBstats.com
- wOBA - May be available from sabermetric sources

**Tracking Data Metrics**: VERY LIMITED OR UNAVAILABLE
- xWOBA - Unlikely (requires Statcast-like tracking)
- Hard hit rate - Unlikely
- Pitch spin rate - Unlikely
- Exit velocity - Unlikely
- Launch angle - Unlikely

**Key Challenge**: NPB doesn't have publicly available tracking technology data like MLB's Statcast

### 5. NPBstats.com

- Japanese professional baseball statistics website
- Claims to provide "basic records and sabermetric records such as wOBA, FIP and WAR"
- Site appears to be down currently (connection refused)
- No API documentation found

---

## Technical Considerations

### Web Scraping Challenges:
1. Japanese language content (need proper encoding)
2. Dynamic content (may require Selenium)
3. Rate limiting concerns
4. Data structure inconsistencies
5. Maintenance burden (site changes)

### Data Integration Challenges:
1. Player name romanization variations
2. Different stat categories than MLB
3. League structure differences (Central vs Pacific)
4. Historical data gaps
5. No unified player IDs across sources

---

## Discovered NPB-Specific Python Tools

1. **getNPB.py** (from atsukoba's repo)
   - Scrapes npb.jp/bis/yearly/
   - Uses BeautifulSoup4 + requests
   - Can fetch by year or bulk 1950-2017

2. **farm-stats-sw** 
   - NPB Farm league statistics
   - Uses ScraperWiki framework

3. **No comprehensive NPB Python package exists**
   - Unlike MLB which has pybaseball, MLB-StatsAPI, etc.
   - Gap in the ecosystem for NPB data

---

## Key Findings Summary

1. **No official NPB API exists** - all data must be scraped or obtained from third parties
2. **pybaseball does not support NPB** - confirmed to be MLB-only
3. **Advanced tracking metrics largely unavailable** - NPB lacks public Statcast-equivalent
4. **Multiple scraping targets exist** - npb.jp, Baseball-Reference, various Japanese sites
5. **Commercial APIs available** - Sportradar, OddsMatrix, LSports (all paid)
6. **Some open-source scrapers exist** - but nothing comprehensive or well-maintained

---

## Proposed Implementation Approaches

### Approach 1: Web Scraping Solution (Recommended for Free Implementation)

**Overview**: Build a comprehensive NPB scraper similar to how pybaseball scrapes Baseball Reference

**Architecture**:
```
src/
├── npb_api.py          # NPB-specific API client (scraping functions)
├── npb_constants.py    # NPB team IDs, league mappings, etc.
└── data_utils.py       # Extend with NPB formatters
```

**Data Sources**:
1. Primary: Baseball-Reference.com/register/npb-stats.shtml
   - Most comprehensive historical data
   - Likely includes some advanced metrics
   - English language (easier parsing)
   
2. Secondary: npb.jp/eng/
   - Official source for current season
   - Real-time updates
   - May have data not on Baseball-Reference

**Implementation Details**:
- Use BeautifulSoup4 + httpx for scraping (consistent with current architecture)
- Implement caching with same 24-hour TTL system
- Create NPB-specific formatters in data_utils.py
- Add new MCP tools mirroring MLB tools:
  - `search_npb_player`
  - `get_npb_player_stats`
  - `get_npb_team_roster`
  - `get_npb_standings`

**Pros**:
- Free implementation
- Full control over data parsing
- Can integrate multiple sources
- Follows existing architectural patterns

**Cons**:
- Maintenance burden when sites change
- Slower than API calls
- Rate limiting concerns
- No real-time game data

### Approach 2: Commercial API Integration (Best for Production)

**Overview**: Integrate Sportradar's Global Baseball API for professional-grade NPB data

**Implementation**:
- Create new `sportradar_api.py` module
- Add API key configuration to environment
- Map Sportradar data format to existing formatters

**Pros**:
- Professional reliability
- Real-time data
- Comprehensive coverage
- Official data source
- Less maintenance

**Cons**:
- Subscription cost
- API rate limits
- Vendor lock-in
- May not have historical data

### Approach 3: Hybrid Solution (Balanced Approach)

**Overview**: Combine free scraping for historical/basic data with optional commercial API for real-time

**Architecture**:
```
src/
├── npb_api.py          # Orchestrates data sources
├── npb_scraper.py      # Web scraping functions
├── npb_commercial.py   # Optional commercial API (Sportradar)
└── npb_constants.py    # NPB configurations
```

**Data Strategy**:
1. Historical data: Scrape Baseball-Reference (free)
2. Current season basic stats: Scrape npb.jp (free)
3. Real-time/advanced: Commercial API (optional paid upgrade)

**Pros**:
- Free basic functionality
- Upgrade path for premium features
- Best of both worlds
- Follows microservices pattern

**Cons**:
- More complex implementation
- Multiple data source management
- Potential data inconsistencies

### Approach 4: Community Data Repository Integration

**Overview**: Use armstjc/Nippon-Baseball-Data-Repository as primary source

**Implementation**:
- Clone/download repository data
- Build Python wrapper around JSON files
- Periodic updates from repository
- Contribute improvements back

**Pros**:
- Community maintained
- Open source collaboration
- JSON format already
- No scraping needed

**Cons**:
- Depends on maintainer activity
- May lag behind current games
- Limited to what repository provides
- No real-time capability

---

## Recommended Implementation Path

### Phase 1: MVP with Web Scraping
1. Implement Baseball-Reference scraper for NPB
2. Focus on traditional stats first (AVG, HR, RBI, ERA)
3. Add basic player search and stats retrieval
4. Extend existing cache system for NPB data
5. Create 4-5 core MCP tools for NPB

### Phase 2: Enhanced Metrics
1. Add calculated advanced metrics (OPS+, ERA+)
2. Implement WAR if available from sources
3. Add team standings and schedules
4. Improve player name matching (romanization)

### Phase 3: Premium Features (Optional)
1. Integrate commercial API for those who want it
2. Add real-time game data
3. Attempt to find tracking data sources
4. Build historical database

---

## Technical Decisions & Trade-offs

### Scraping vs API
- **Scraping**: Free but fragile, good for MVP
- **API**: Reliable but expensive, good for production

### Data Freshness
- **Cached scraping**: Good enough for most use cases (24hr TTL)
- **Real-time API**: Necessary for live game features

### Advanced Metrics
- **Reality**: Most tracking metrics (xWOBA, spin rate) unavailable
- **Solution**: Focus on calculated metrics (WAR, FIP, wOBA)

### Maintenance
- **Scraping**: Requires regular monitoring and updates
- **API**: Set and forget, vendor handles changes

---

## NPB-Specific Challenges to Address

1. **Player Names**
   - Multiple romanization systems
   - Need fuzzy matching
   - Consider Japanese character support

2. **League Structure**
   - Central League vs Pacific League
   - Different DH rules
   - Climax Series playoffs

3. **Statistical Differences**
   - Tied games possible
   - Different ball specifications
   - Smaller stadiums affect stats

4. **Data Gaps**
   - Less historical data than MLB
   - No public tracking data
   - Limited English documentation

---

## Questions for User

1. **Budget**: Is this a free/open-source project or is there budget for commercial APIs?

2. **Priorities**: What's more important - comprehensive historical data or real-time current season?

3. **Metrics**: Which specific advanced metrics are must-haves vs nice-to-haves?

4. **Maintenance**: Who will maintain the scrapers when websites change?

5. **User Base**: Will this be used by English speakers only or need Japanese language support?

---

## Next Steps After Approach Selection

1. Create NPB-specific modules following existing patterns
2. Implement data source connections (scraper or API)
3. Add NPB tools to MCP server
4. Extend formatters for NPB data
5. Add comprehensive tests
6. Document NPB limitations vs MLB
7. Consider creating example scripts

---

## Research Completed: 2025-06-23

This research provides a comprehensive overview of NPB data availability and multiple implementation paths. The recommended approach depends on project constraints and requirements.

---

## Selected Implementation Approach (Based on User Feedback)

**User Requirements:**
- Open-source project (free implementation initially)
- Support for commercial APIs later
- Need extensible architecture

### Chosen Approach: Hybrid Architecture with Provider Pattern

This approach allows starting with web scraping while maintaining clean interfaces for future commercial API integration.

---

## Detailed Implementation Plan

### 1. Architecture Design

```
src/
├── npb/                           # NPB module directory
│   ├── __init__.py
│   ├── providers/                 # Data provider implementations
│   │   ├── __init__.py
│   │   ├── base.py               # Abstract base provider
│   │   ├── scraper_provider.py   # Web scraping implementation
│   │   └── sportradar_provider.py # Future commercial API
│   ├── scrapers/                  # Scraping implementations
│   │   ├── __init__.py
│   │   ├── base_scraper.py       # Base scraper class
│   │   ├── baseball_reference.py # Baseball-Reference scraper
│   │   └── npb_official.py       # npb.jp scraper
│   ├── models.py                  # NPB data models
│   ├── constants.py               # NPB teams, leagues, etc.
│   └── api.py                     # High-level NPB API
├── data_utils.py                  # Extend with NPB formatters
└── baseball_mcp_server.py         # Add NPB tools
```

### 2. Provider Pattern Implementation

```python
# npb/providers/base.py
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

class NPBDataProvider(ABC):
    """Abstract base class for NPB data providers"""
    
    @abstractmethod
    async def search_player(self, name: str) -> List[Dict[str, Any]]:
        """Search for players by name"""
        pass
    
    @abstractmethod
    async def get_player_stats(self, player_id: str, season: Optional[int] = None) -> Dict[str, Any]:
        """Get player statistics"""
        pass
    
    @abstractmethod
    async def get_team_roster(self, team_id: str, season: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get team roster"""
        pass
    
    @abstractmethod
    async def get_standings(self, season: Optional[int] = None) -> Dict[str, Any]:
        """Get league standings"""
        pass
```

### 3. Web Scraping Implementation Plan

#### Phase 1: Core Scraping Infrastructure
1. **Base Scraper Class**
   - HTTP client with retry logic
   - Rate limiting (2-3 requests/second)
   - User-agent rotation
   - Error handling and logging

2. **Baseball-Reference NPB Scraper**
   - Player search and stats
   - Team rosters and standings
   - Historical data (1936-present)
   - Parse HTML tables to structured data

3. **NPB Official Site Scraper**
   - Current season data
   - Real-time standings
   - Japanese name handling
   - Fallback for missing BR data

#### Phase 2: Data Models and Normalization

```python
# npb/models.py
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

class NPBLeague(Enum):
    CENTRAL = "central"
    PACIFIC = "pacific"

@dataclass
class NPBPlayer:
    id: str  # Internal ID (could be name-based initially)
    name_english: str
    name_japanese: Optional[str]
    team_id: Optional[str]
    position: Optional[str]
    jersey_number: Optional[int]
    
@dataclass
class NPBBattingStats:
    player_id: str
    season: int
    games: int
    at_bats: int
    runs: int
    hits: int
    doubles: int
    triples: int
    home_runs: int
    rbis: int
    stolen_bases: int
    batting_average: float
    on_base_percentage: float
    slugging_percentage: float
    ops: float
    # Advanced metrics when available
    war: Optional[float] = None
    woba: Optional[float] = None
    ops_plus: Optional[int] = None
```

#### Phase 3: High-Level API

```python
# npb/api.py
from typing import Optional
from .providers.base import NPBDataProvider
from .providers.scraper_provider import ScraperProvider

class NPBAPI:
    def __init__(self, provider: Optional[NPBDataProvider] = None):
        self.provider = provider or ScraperProvider()
    
    async def search_player(self, name: str) -> str:
        """Search for NPB players"""
        results = await self.provider.search_player(name)
        return format_player_search_results(results)
    
    async def get_player_stats(self, player_id: str, season: Optional[int] = None) -> str:
        """Get NPB player statistics"""
        stats = await self.provider.get_player_stats(player_id, season)
        return format_player_stats(stats)
```

### 4. MCP Tool Integration

New tools to add to `baseball_mcp_server.py`:

```python
@server.tool(
    description="Search for NPB (Japanese baseball) players by name"
)
async def search_npb_player(search_str: str) -> str:
    """Search for NPB players"""
    return await npb_api.search_player(search_str)

@server.tool(
    description="Get NPB player statistics including traditional and advanced metrics"
)
async def get_npb_player_stats(
    player_id: str,
    season: Optional[str] = None,
    stats_type: str = "season"
) -> str:
    """Get NPB player statistics"""
    return await npb_api.get_player_stats(player_id, season, stats_type)

@server.tool(
    description="Get NPB team roster"
)
async def get_npb_team_roster(
    team_id: str,
    season: Optional[str] = None
) -> str:
    """Get NPB team roster"""
    return await npb_api.get_team_roster(team_id, season)

@server.tool(
    description="Get NPB standings by league"
)
async def get_npb_standings(
    league: Optional[str] = None,  # "central", "pacific", or None for both
    season: Optional[str] = None
) -> str:
    """Get NPB standings"""
    return await npb_api.get_standings(league, season)
```

### 5. Caching Strategy

- Extend existing cache_utils.py to support NPB
- Cache keys: `npb_{function}_{params_hash}`
- TTL: 24 hours for historical, 1 hour for current season
- Special handling for live/today's data

### 6. Implementation Phases

#### Phase 1: MVP (Week 1-2)
- [ ] Basic scraper infrastructure
- [ ] Baseball-Reference player search
- [ ] Player batting stats (traditional only)
- [ ] Simple MCP tools (search_player, get_stats)
- [ ] Basic caching

#### Phase 2: Enhanced Features (Week 3-4)
- [ ] NPB official site scraper
- [ ] Pitching statistics
- [ ] Team rosters and standings
- [ ] Advanced metrics (WAR, OPS+, FIP where available)
- [ ] Improved name matching

#### Phase 3: Polish & Commercial Prep (Week 5-6)
- [ ] Error handling improvements
- [ ] Comprehensive testing
- [ ] Documentation
- [ ] Provider interface refinement
- [ ] Config system for future API keys

### 7. Future Commercial API Integration

When ready to add Sportradar or other commercial APIs:

```python
# npb/providers/sportradar_provider.py
class SportradarProvider(NPBDataProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sportradar.com/baseball/global/v2"
    
    async def search_player(self, name: str) -> List[Dict[str, Any]]:
        # Implement Sportradar API calls
        pass
```

Then users can switch providers:
```python
# Use free scraping
npb_api = NPBAPI()  # Default ScraperProvider

# Use commercial API
npb_api = NPBAPI(SportradarProvider(api_key="..."))
```

### 8. Testing Strategy

1. **Unit Tests**
   - Mock HTML responses for scrapers
   - Test data parsing logic
   - Test provider interface compliance

2. **Integration Tests**
   - Test against real websites (sparingly)
   - Verify data consistency
   - Test error handling

3. **Example Scripts**
   - NPB player comparison
   - Season statistics leaders
   - Team performance analysis

---

## Decisions Made

1. **Provider Pattern**: Clean separation between data sources
2. **Start with Scraping**: Free implementation first
3. **Baseball-Reference Primary**: Most reliable English source
4. **Simple Player IDs**: Name-based initially, can migrate later
5. **Focus on Available Metrics**: No false promises about tracking data
6. **Gradual Enhancement**: MVP first, then add features

---

## Next Immediate Steps

1. Create `src/npb/` directory structure
2. Implement base provider interface
3. Build Baseball-Reference scraper for players
4. Add first MCP tool (search_npb_player)
5. Test end-to-end with Claude Desktop

---

## Implementation Update (2025-06-23)

### Completed:
- ✅ Created NPB module structure with provider pattern
- ✅ Implemented base provider interface
- ✅ Built Baseball-Reference scraper
- ✅ Added NPB tools to MCP server
- ✅ Basic player search functionality works

### Issue Discovered: Cloudflare Protection

Baseball-Reference uses Cloudflare protection which blocks automated scraping:
- Returns 403 Forbidden status
- Shows "Enable JavaScript and cookies to continue" page
- Makes direct scraping impossible without browser automation

### Alternative Approaches:

1. **Use Different Data Source**
   - NPB official site (npb.jp) might not have Cloudflare
   - Other Japanese baseball sites
   - Focus on sites without anti-bot protection

2. **Browser Automation**
   - Use Selenium or Playwright
   - Much slower and resource-intensive
   - Not ideal for MCP server use case

3. **Cached/Static Data**
   - Use pre-scraped datasets
   - armstjc/Nippon-Baseball-Data-Repository
   - Limited to historical data

4. **Hybrid with Manual Updates**
   - Manual periodic data collection
   - Store in local database
   - Not real-time but practical

### Recommended Next Steps:

1. Test npb.jp/eng/ for Cloudflare protection
2. If blocked, pivot to using community data repositories
3. Consider implementing a local database approach
4. Document limitations clearly for users

---

## Extended Research on Historical NPB Data (2025-06-23)

### Current Implementation Analysis

After analyzing the codebase:
- NPB module uses provider pattern with web scraping
- NPB official site (npb.jp) only has recent data (2005+)
- Baseball-Reference blocked by Cloudflare
- Tests show 404 errors for years like 1992-2000 on npb.jp
- Current implementation cannot retrieve historical data for players like Ichiro (1992-2000)

### Historical Data Sources Investigation

#### Japanese Statistical Sites
1. **1point02.jp**
   - Comprehensive Japanese baseball statistics
   - Has historical data back to 1936
   - Includes some calculated advanced metrics
   - Japanese language only

2. **yakyubaka.com (Yakyu Baka)**
   - "Baseball Fool" - extensive NPB database
   - Historical statistics and records
   - Player career pages with yearly stats

3. **Baseball Lab (baseballdata.jp)**
   - Japanese baseball analytics site
   - Historical data and advanced metrics
   - Subscription may be required for full access

4. **Delta Graphs (deltagraphs.com)**
   - Japanese sabermetrics pioneer
   - Calculates NPB-specific WAR
   - Advanced analytics articles

5. **Yahoo! Japan Sports NPB Section**
   - Comprehensive modern stats
   - May have some historical data
   - Less likely to block scrapers

#### GitHub/Open Source Repositories
1. **npb-db**
   - SQLite database with historical NPB stats
   - Appears to be community maintained
   - Could be imported directly

2. **armstjc/Nippon-Baseball-Data-Repository**
   - JSON files with play-by-play data
   - Python scripts for processing
   - Actively maintained

3. **Various CSV compilations**
   - Found several repos with historical NPB data in CSV format
   - Quality and completeness vary
   - Often focus on specific eras or teams

### Advanced Metrics Availability Analysis

#### Available (Traditional Stats)
- **Batting**: G, AB, R, H, 2B, 3B, HR, RBI, SB, CS, BB, SO, AVG, OBP, SLG, OPS
- **Pitching**: W, L, ERA, G, GS, CG, SHO, SV, IP, H, R, ER, HR, BB, SO, WHIP
- **Source**: Most Japanese statistical sites from 1936 onward

#### Limited Availability (Advanced Calculated Metrics)
- **WAR (Wins Above Replacement)**
  - Delta Graphs calculates NPB-specific WAR
  - Methodology differs from MLB WAR
  - Not universally available
  
- **FIP (Fielding Independent Pitching)**
  - Can be calculated from available stats
  - Need NPB-specific constants
  - Formula: ((13*HR + 3*BB - 2*K)/IP) + constant
  
- **wOBA (Weighted On-Base Average)**
  - Requires NPB-specific linear weights
  - Some sites attempt calculations
  - Different run environment than MLB

- **OPS+ and ERA+**
  - Park and league adjusted stats
  - Requires NPB park factors
  - Can be calculated with effort

#### NOT Available (Tracking-Based Metrics)
- **Statcast Metrics**: Exit velocity, launch angle, sprint speed
- **Pitch Tracking**: Spin rate, movement, velocity by pitch type
- **Expected Stats**: xBA, xSLG, xWOBA
- **Batted Ball**: Hard hit rate, barrel rate
- **Reason**: NPB doesn't have publicly available ball tracking technology

### Key Findings

1. **Historical Data Exists** but is fragmented across multiple Japanese sites
2. **Language Barrier** is significant - most comprehensive sources are Japanese-only
3. **No Unified API** - all data must be scraped or imported from static sources
4. **Advanced Metrics** are limited to what can be calculated from traditional stats
5. **Tracking Data** is completely unavailable publicly
6. **Player Name Romanization** varies significantly between sources

### Technical Challenges

1. **Website Protection**
   - Some sites use Cloudflare or other anti-bot measures
   - Need to respect rate limits and robots.txt
   
2. **Data Consistency**
   - Different sites use different player ID systems
   - Name romanization inconsistencies (Otani vs Ohtani)
   - Statistical categorization differences

3. **Historical Completeness**
   - Some years have gaps in data
   - Older seasons may only have basic stats
   - Need to indicate data quality/completeness

4. **Maintenance Burden**
   - Websites change structure
   - New anti-scraping measures
   - Keeping multiple scrapers updated

---

## Proposed Implementation Approaches for Historical NPB Data

### Approach 1: Static Dataset Import + Modern Scraping (RECOMMENDED)

**Overview**: Import historical data from existing datasets and scrape only recent seasons

**Architecture**:
```
src/npb/
├── providers/
│   ├── historical_provider.py    # Query local historical database
│   ├── scraper_provider.py       # Existing (for 2005+ data)
│   └── composite_provider.py     # Combines historical + modern
├── data/
│   ├── import/
│   │   ├── npb_db_importer.py  # Import from npb-db SQLite
│   │   ├── csv_importer.py     # Import from CSV files
│   │   └── json_importer.py    # Import from JSON datasets
│   ├── historical.db            # SQLite with all historical data
│   └── metrics/
│       ├── calculator.py        # Calculate FIP, basic WAR
│       └── constants.py         # NPB-specific constants
└── scrapers/
    └── (existing scrapers for modern data)
```

**Implementation Steps**:
1. Download historical datasets (npb-db, CSV compilations)
2. Create unified schema for historical data
3. Import all data into local SQLite database
4. Build historical provider to query this database
5. Create composite provider that uses:
   - Historical provider for data before 2005
   - Existing scrapers for 2005+
6. Implement metrics calculator for advanced stats

**Pros**:
- Most reliable approach for historical data
- No web scraping needed for historical stats
- Fast query performance
- Can calculate our own advanced metrics

**Cons**:
- Initial data import effort
- Need to find/validate historical datasets
- Static data (no real-time historical updates)

### Approach 2: Multi-Site Japanese Scraper Network

**Overview**: Build scrapers for multiple Japanese statistical sites

**Target Sites**:
1. **1point02.jp** - Comprehensive stats including some advanced metrics
2. **yakyubaka.com** - Extensive historical database
3. **Yahoo! Japan Sports** - Less likely to block scrapers
4. **Stats Crew** - English-language Japanese baseball stats

**Architecture**:
```
src/npb/
├── scrapers/
│   ├── one_point_zero_two.py   # 1point02.jp scraper
│   ├── yakyu_baka.py           # yakyubaka.com scraper
│   ├── yahoo_sports_jp.py      # Yahoo Japan scraper
│   └── stats_crew.py           # Stats Crew scraper
├── providers/
│   └── multi_source_provider.py # Aggregates multiple scrapers
├── utils/
│   ├── japanese_parser.py      # Handle Japanese text/encoding
│   ├── name_normalizer.py      # Handle romanization variants
│   └── data_reconciler.py      # Merge conflicting data
└── cache/
    └── historical_cache.py      # Aggressive caching for historical
```

**Key Features**:
- Fallback chain when one site is unavailable
- Japanese text parsing and translation
- Fuzzy name matching for romanization issues
- Data reconciliation when sources conflict

**Pros**:
- Access to most comprehensive data
- Can get some calculated Japanese advanced metrics
- Redundancy across multiple sources

**Cons**:
- Complex to maintain multiple scrapers
- Japanese language challenges
- Sites may block or change structure

### Approach 3: Community Repository Integration

**Overview**: Use and contribute to open-source NPB data repositories

**Primary Sources**:
- armstjc/Nippon-Baseball-Data-Repository (JSON data)
- npb-db project (SQLite database)
- Various CSV compilations on GitHub

**Architecture**:
```
src/npb/
├── providers/
│   └── repository_provider.py   # Interface to community data
├── sync/
│   ├── github_sync.py          # Sync with GitHub repos
│   └── data_updater.py         # Periodic updates
├── contributions/
│   ├── data_validator.py       # Validate our additions
│   └── export_formatter.py     # Format data for contribution
└── local_store/
    └── repository_cache.db      # Local copy of all data
```

**Workflow**:
1. Clone/download community repositories
2. Import into structured local database
3. Periodically sync updates
4. Calculate missing advanced metrics
5. Contribute improvements back to community

**Pros**:
- Leverages existing community work
- Can contribute improvements
- Already structured data (JSON/CSV)

**Cons**:
- Depends on community maintenance
- May have data gaps
- Limited to what repositories provide

### Approach 4: Hybrid Progressive Enhancement

**Overview**: Start simple and progressively add data sources

**Phase 1 - Basic Historical (Week 1)**:
- Import one good historical dataset (npb-db)
- Support basic queries for historical players
- Traditional stats only

**Phase 2 - Enhanced Metrics (Week 2-3)**:
- Add metrics calculator (FIP, basic WAR)
- Import additional datasets for validation
- Add data quality indicators

**Phase 3 - Japanese Sources (Week 4-5)**:
- Add 1-2 Japanese site scrapers
- Focus on sites with advanced metrics
- Handle Japanese language content

**Phase 4 - Full Integration (Week 6+)**:
- Combine all sources
- Add commercial API support option
- Complete documentation

---

## Recommended Advanced Metrics Implementation

### Metrics We CAN Calculate:
1. **FIP (Fielding Independent Pitching)**
   ```python
   # NPB-specific FIP
   def calculate_npb_fip(hr, bb, hbp, k, ip):
       # NPB constant is different from MLB (around 3.10-3.20)
       NPB_FIP_CONSTANT = 3.15  
       return ((13*hr + 3*(bb+hbp) - 2*k) / ip) + NPB_FIP_CONSTANT
   ```

2. **wOBA (Weighted On-Base Average)**
   ```python
   # NPB linear weights (approximate, need refinement)
   NPB_WEIGHTS = {
       'bb': 0.69,
       'hbp': 0.72,
       '1b': 0.88,
       '2b': 1.24,
       '3b': 1.56,
       'hr': 1.95
   }
   ```

3. **Basic WAR**
   - Position player: Batting Runs + Baserunning + Fielding + Positional + Replacement
   - Pitcher: Based on FIP and innings pitched
   - Use simplified version without defensive metrics

4. **Park-Adjusted Stats (OPS+, ERA+)**
   - Calculate park factors from historical data
   - Adjust for NPB's unique ballparks

### Metrics We CANNOT Provide:
- Exit Velocity
- Launch Angle  
- Spin Rate
- Hard Hit Rate
- xWOBA, xBA, xSLG
- Pitch movement data
- Sprint speed

### Data Quality Indicators:
```python
class DataQuality(Enum):
    COMPLETE = "complete"      # All stats available
    BASIC = "basic"           # Traditional stats only
    PARTIAL = "partial"       # Some stats missing
    ESTIMATED = "estimated"   # Calculated/inferred
```

---

## Final Recommendation

**Implement Approach 1 (Static Dataset Import + Modern Scraping) because:**

1. **Most Reliable** - Historical data won't change, so static import is perfect
2. **Best Performance** - Local database queries are fast
3. **Maintainable** - Only need to maintain scrapers for recent seasons
4. **Extensible** - Can add more data sources later
5. **Quality Control** - Can validate and clean data during import

**Implementation Priority:**
1. Find and download best historical datasets (npb-db, CSV files)
2. Create import scripts and unified database schema
3. Build historical provider with caching
4. Add metrics calculator for FIP and basic WAR
5. Create composite provider combining historical + modern
6. Document limitations clearly (no tracking data)
7. Add examples showing what's available vs. MLB

**Success Metrics:**
- Can retrieve full career stats for historical players (like Ichiro 1992-2000)
- Calculate basic advanced metrics (FIP, simple WAR)
- Clear documentation about what metrics are/aren't available
- Fast query performance (<100ms for career stats)
- Easy to add new data sources later