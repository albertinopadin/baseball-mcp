def get_with_default(key: str, data: dict, default="Unknown"):
    return data.get(key, default)


def format_player_data(data: dict) -> str:
    """Format a player data object into a readable string."""
    primary_position = data.get('primaryPosition', {})
    position_name = primary_position.get('name', 'Unknown') if isinstance(primary_position, dict) else primary_position
    
    bat_side = data.get('batSide', {})
    bat_side_desc = bat_side.get('description', 'Unknown') if isinstance(bat_side, dict) else bat_side
    
    pitch_hand = data.get('pitchHand', {})
    pitch_hand_desc = pitch_hand.get('description', 'Unknown') if isinstance(pitch_hand, dict) else pitch_hand
    
    return f"""Player Information:
    ID: {get_with_default('id', data)}
    Full Name: {get_with_default('fullName', data)}
    Jersey Number: {get_with_default('primaryNumber', data)}
    Position: {position_name}
    
    Personal Details:
    Birth Date: {get_with_default('birthDate', data)}
    Age: {get_with_default('currentAge', data)}
    Birth Place: {get_with_default('birthCity', data)}, {get_with_default('birthCountry', data)}
    Height: {get_with_default('height', data)}
    Weight: {get_with_default('weight', data)} lbs
    
    Playing Style:
    Bats: {bat_side_desc}
    Throws: {pitch_hand_desc}
    
    Career:
    Active: {get_with_default('active', data)}
    MLB Debut: {get_with_default('mlbDebutDate', data)}
    """


def format_team_data(data: dict) -> str:
    """Format a team data object into a readable string."""
    venue = data.get('venue', {})
    venue_name = venue.get('name', 'Unknown') if isinstance(venue, dict) else 'Unknown'
    
    league = data.get('league', {})
    league_name = league.get('name', 'Unknown') if isinstance(league, dict) else 'Unknown'
    
    division = data.get('division', {})
    division_name = division.get('name', 'Unknown') if isinstance(division, dict) else 'Unknown'
    
    return f"""Team Information:
    ID: {get_with_default('id', data)}
    Name: {get_with_default('name', data)}
    Abbreviation: {get_with_default('abbreviation', data)}
    
    Location:
    City: {get_with_default('locationName', data)}
    Venue: {venue_name}
    
    Organization:
    League: {league_name}
    Division: {division_name}
    
    Details:
    First Year: {get_with_default('firstYearOfPlay', data)}
    Active: {get_with_default('active', data)}
    """


def format_roster_data(roster: list) -> str:
    """Format roster data into a readable string."""
    if not roster:
        return "No roster data available."
    
    formatted_players = []
    for player in roster:
        person = player.get('person', {})
        position = player.get('position', {})
        jersey = player.get('jerseyNumber', 'N/A')
        status = player.get('status', {})
        
        player_info = f"""  #{jersey} {person.get('fullName', 'Unknown')} - {position.get('name', 'Unknown')}
    Status: {status.get('description', 'Active')}"""
        formatted_players.append(player_info)
    
    return "Team Roster:\n" + "\n\n".join(formatted_players)


def format_player_stats(stats: list) -> str:
    """Format player statistics into a readable string."""
    if not stats:
        return "No statistics available."
    
    formatted_stats = []
    for stat_group in stats:
        group_name = stat_group.get('group', {}).get('displayName', 'Statistics')
        type_name = stat_group.get('type', {}).get('displayName', '')
        
        splits = stat_group.get('splits', [])
        if not splits:
            continue
            
        stat_lines = [f"\n{group_name} - {type_name}:"]
        
        for split in splits:
            season = split.get('season', 'N/A')
            team = split.get('team', {})
            team_name = team.get('name', 'N/A') if isinstance(team, dict) else 'N/A'
            
            stat_data = split.get('stat', {})
            
            # Format based on stat type
            if 'avg' in stat_data:  # Hitting stats
                stat_lines.append(f"""  Season: {season} - Team: {team_name}
    G: {stat_data.get('gamesPlayed', 0)} | AB: {stat_data.get('atBats', 0)} | R: {stat_data.get('runs', 0)} | H: {stat_data.get('hits', 0)}
    2B: {stat_data.get('doubles', 0)} | 3B: {stat_data.get('triples', 0)} | HR: {stat_data.get('homeRuns', 0)} | RBI: {stat_data.get('rbi', 0)}
    BB: {stat_data.get('baseOnBalls', 0)} | SO: {stat_data.get('strikeOuts', 0)} | SB: {stat_data.get('stolenBases', 0)} | CS: {stat_data.get('caughtStealing', 0)}
    AVG: {stat_data.get('avg', 'N/A')} | OBP: {stat_data.get('obp', 'N/A')} | SLG: {stat_data.get('slg', 'N/A')} | OPS: {stat_data.get('ops', 'N/A')}""")
            elif 'era' in stat_data:  # Pitching stats
                stat_lines.append(f"""  Season: {season} - Team: {team_name}
    W-L: {stat_data.get('wins', 0)}-{stat_data.get('losses', 0)} | ERA: {stat_data.get('era', 'N/A')} | WHIP: {stat_data.get('whip', 'N/A')}
    IP: {stat_data.get('inningsPitched', 'N/A')} | SO: {stat_data.get('strikeOuts', 0)} | BB: {stat_data.get('baseOnBalls', 0)}""")
            
        formatted_stats.append("\n".join(stat_lines))
    
    return "\n\n".join(formatted_stats)


def format_schedule_data(dates: list) -> str:
    """Format schedule data into a readable string."""
    if not dates:
        return "No games scheduled."
    
    formatted_games = []
    for date_entry in dates:
        date = date_entry.get('date', 'Unknown')
        games = date_entry.get('games', [])
        
        if games:
            formatted_games.append(f"\nDate: {date}")
            
        for game in games:
            game_pk = game.get('gamePk', 'N/A')
            status = game.get('status', {}).get('detailedState', 'Unknown')
            
            teams = game.get('teams', {})
            away = teams.get('away', {})
            home = teams.get('home', {})
            
            away_team = away.get('team', {}).get('name', 'Unknown')
            home_team = home.get('team', {}).get('name', 'Unknown')
            
            away_score = away.get('score', 'N/A')
            home_score = home.get('score', 'N/A')
            
            game_info = f"""  Game {game_pk}: {away_team} @ {home_team}
    Status: {status}
    Score: {away_team} {away_score} - {home_team} {home_score}"""
            
            formatted_games.append(game_info)
    
    return "Schedule:\n" + "\n\n".join(formatted_games)


def format_game_data(data: dict) -> str:
    """Format game boxscore data into a readable string."""
    teams = data.get('teams', {})
    away = teams.get('away', {})
    home = teams.get('home', {})
    
    away_team = away.get('team', {}).get('name', 'Unknown')
    home_team = home.get('team', {}).get('name', 'Unknown')
    
    away_stats = away.get('teamStats', {}).get('batting', {})
    home_stats = home.get('teamStats', {}).get('batting', {})
    
    return f"""Game Summary:
    {away_team} vs {home_team}
    
    Score:
    {away_team}: {away_stats.get('runs', 0)}
    {home_team}: {home_stats.get('runs', 0)}
    
    Hits:
    {away_team}: {away_stats.get('hits', 0)}
    {home_team}: {home_stats.get('hits', 0)}
    
    Errors:
    {away_team}: {away_stats.get('errors', 0)}
    {home_team}: {home_stats.get('errors', 0)}
    """


def format_standings_data(records: list) -> str:
    """Format standings data into a readable string."""
    if not records:
        return "No standings data available."
    
    formatted_standings = []
    for division in records:
        division_name = division.get('division', {}).get('name', 'Unknown Division')
        standings = division.get('teamRecords', [])
        
        formatted_standings.append(f"\n{division_name}:")
        
        for i, team in enumerate(standings, 1):
            team_data = team.get('team', {})
            team_name = team_data.get('name', 'Unknown')
            wins = team.get('wins', 0)
            losses = team.get('losses', 0)
            pct = team.get('winningPercentage', '0.000')
            gb = team.get('gamesBack', '-')
            
            formatted_standings.append(
                f"  {i}. {team_name}: {wins}-{losses} ({pct}) GB: {gb}"
            )
    
    return "Standings:" + "\n".join(formatted_standings)


def format_live_game_data(data: dict) -> str:
    """Format live game feed data into a readable string."""
    game_data = data.get('gameData', {})
    live_data = data.get('liveData', {})
    
    teams = game_data.get('teams', {})
    away = teams.get('away', {}).get('name', 'Unknown')
    home = teams.get('home', {}).get('name', 'Unknown')
    
    status = game_data.get('status', {})
    detailed_state = status.get('detailedState', 'Unknown')
    
    linescore = live_data.get('linescore', {})
    current_inning = linescore.get('currentInning', 'N/A')
    inning_state = linescore.get('inningState', 'N/A')
    
    teams_data = linescore.get('teams', {})
    away_runs = teams_data.get('away', {}).get('runs', 0)
    home_runs = teams_data.get('home', {}).get('runs', 0)
    
    return f"""Live Game Feed:
    {away} @ {home}
    
    Status: {detailed_state}
    Inning: {inning_state} {current_inning}
    
    Score:
    {away}: {away_runs}
    {home}: {home_runs}
    
    Outs: {linescore.get('outs', 0)}
    Balls: {linescore.get('balls', 0)}
    Strikes: {linescore.get('strikes', 0)}
    """