# Minor League Stats Investigation Scratchpad

## Investigation Goal
Verify if MLB Stats API can provide minor league statistics using the sportId parameter.

## Reference
- https://billpetti.github.io/baseballr/reference/mlb_sports.html suggests sportId can query different levels
- Need to check mlb-statsapi-spec.json for API spec details

## Progress Log

### Initial Setup (Started)
- Created this scratchpad file to track investigation
- Planning to examine MLB Stats API spec and existing implementation

### MLB Stats API Spec Investigation
- Found mlb-statsapi-spec.json file exists
- Discovered multiple endpoints use sportId parameter
- Sports endpoint at "/api/v1/sports" exists but seems to require sportId in path
- Need to find endpoint that lists all available sports without requiring sportId

### Current Implementation Analysis
- The MLB Stats API implementation already has sportId parameter support!
- Default sportId is 1 (MLB)
- Functions that accept sportId:
  - get_player_stats() - default: 1
  - search_teams() - default: 1
  - get_schedule() - default: 1
- This means we can potentially query minor league data by changing sportId

### API Testing Results - MAJOR DISCOVERY!

#### Available Sports (from /api/v1/sports endpoint)
The API supports 19 different sports/leagues:
- **Minor League Levels:**
  - ID 11: Triple-A (aaa)
  - ID 12: Double-A (aax)
  - ID 13: High-A (afa)
  - ID 14: Single-A (afx)
  - ID 15: Class A Short Season (asx)
  - ID 16: Rookie (rok)
  - ID 21: Minor League Baseball (min) - appears to be general minor leagues
- **Other Leagues:**
  - ID 1: Major League Baseball (mlb)
  - ID 17: Winter Leagues (win)
  - ID 23: Independent Leagues (ind)
  - ID 61: Negro League Baseball (nlb)
  - ID 32: Korean Baseball Organization (kor)
  - ID 31: Nippon Professional Baseball (jml)
  - ID 51: International Baseball (int)
  - ID 22: College Baseball (bbc)
  - ID 586: High School Baseball (hsb)
  - ID 576: Women's Professional Softball (wps)

#### Teams Endpoint Works!
- Successfully retrieved teams for all minor league levels
- Triple-A (11): 30 teams (e.g., Toledo Mud Hens, Lehigh Valley IronPigs)
- Double-A (12): 31 teams (e.g., Altoona Curve, Tulsa Drillers)
- High-A (13): 30 teams (e.g., Bowling Green Hot Rods, Winston-Salem Dash)
- Single-A (14): 31 teams (e.g., Hickory Crawdads, Fayetteville Woodpeckers)

#### Player Stats Challenge
- Bobby Witt Jr. only showed MLB stats (sportId=1)
- Need to test with a player who has recent minor league experience

### Successful Minor League Stats Retrieval!

#### Key Findings:
1. **Player Stats Work with Minor League sportIds!**
   - Successfully retrieved stats for all minor league levels
   - Examples tested: Jackson Holliday, Paul Skenes, Jasson Dominguez, Jordan Walker, Gunnar Henderson
   - All showed appropriate minor league stats when using correct sportId

2. **Data Available by Level:**
   - Triple-A (sportId=11): Full stats available
   - Double-A (sportId=12): Full stats available
   - High-A (sportId=13): Full stats available
   - Single-A (sportId=14): Full stats available
   - Rookie (sportId=16): Full stats available

3. **Stats Include:**
   - Batting: Games, AVG, HR, RBI, etc.
   - Pitching: Games, ERA, W-L, SO, etc.
   - Team affiliation for each level

4. **YearByYear Stats Issue:**
   - The yearByYear endpoint seems to only return MLB stats
   - Does not show minor league seasons in the yearByYear view
   - To get minor league stats, must query each sportId separately

5. **Important Discovery:**
   - Minor league stats ARE available through the API
   - Must use specific sportId for each level
   - Cannot get all levels in one call (must query each level separately)

### Additional Endpoint Testing Results

#### Schedule Endpoint ✅
- Works perfectly with minor league sportIds
- Returns full game schedules for all minor league levels
- Example: Found 100+ games per week for each level

#### Standings Endpoint ❌
- Does NOT work with minor league sportIds
- Returns empty records array
- Minor leagues likely use different structure for standings

#### Game Info Endpoints
- Boxscore endpoint ✅ - Works for minor league games
- Live feed endpoint ❌ - Returns 404 for minor league games
- Can retrieve game PKs from schedule for detailed game info

#### Player Search
- sportId parameter in search doesn't filter results
- Returns same results with or without sportId parameter

## Summary of Findings

### ✅ CONFIRMED: Minor League Stats ARE Available!

**What Works:**
1. **Player Stats** - Full batting/pitching stats for all minor league levels using sportId parameter
2. **Team Lists** - Complete team rosters for each minor league level
3. **Team Rosters** - Player rosters for minor league teams
4. **Game Schedules** - Full schedules for all minor league games
5. **Game Boxscores** - Detailed game data for completed minor league games

**What Doesn't Work:**
1. **Standings** - Not available for minor leagues through standard endpoint
2. **Live Game Feeds** - Not available for minor league games
3. **YearByYear Stats** - Only shows MLB stats, not minor league history
4. **Player Search Filtering** - Can't filter search by sport/level

**Key Sport IDs for Minor Leagues:**
- 11 = Triple-A (AAA)
- 12 = Double-A (AA)
- 13 = High-A (A+)
- 14 = Single-A (A)
- 15 = Short Season A
- 16 = Rookie
- 17 = Winter Leagues
- 21 = Minor League Baseball (general)
- 22 = College Baseball
- 23 = Independent Leagues

**Implementation Notes:**
- The existing MCP server code already supports sportId parameters
- To get minor league data, simply pass the appropriate sportId
- Must query each level separately (no combined query option)
- Cache should work fine with minor league data as well
