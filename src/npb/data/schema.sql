-- NPB Historical Database Schema

-- Players table
CREATE TABLE IF NOT EXISTS players (
    player_id TEXT PRIMARY KEY,
    name_english TEXT NOT NULL,
    name_japanese TEXT,
    name_romanized_variants TEXT, -- JSON array of alternative romanizations
    birth_date TEXT,
    birth_place TEXT,
    height TEXT,
    weight TEXT,
    bats TEXT,
    throws TEXT,
    debut_date TEXT,
    final_game TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Teams table
CREATE TABLE IF NOT EXISTS teams (
    team_id TEXT PRIMARY KEY,
    name_english TEXT NOT NULL,
    name_japanese TEXT,
    abbreviation TEXT,
    league TEXT CHECK (league IN ('Central', 'Pacific')),
    city TEXT,
    founded_year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Batting statistics table
CREATE TABLE IF NOT EXISTS batting_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id TEXT NOT NULL,
    season INTEGER NOT NULL,
    team_id TEXT,
    league TEXT,
    games INTEGER DEFAULT 0,
    plate_appearances INTEGER DEFAULT 0,
    at_bats INTEGER DEFAULT 0,
    runs INTEGER DEFAULT 0,
    hits INTEGER DEFAULT 0,
    doubles INTEGER DEFAULT 0,
    triples INTEGER DEFAULT 0,
    home_runs INTEGER DEFAULT 0,
    rbis INTEGER DEFAULT 0,
    stolen_bases INTEGER DEFAULT 0,
    caught_stealing INTEGER DEFAULT 0,
    walks INTEGER DEFAULT 0,
    strikeouts INTEGER DEFAULT 0,
    hit_by_pitch INTEGER DEFAULT 0,
    sacrifice_hits INTEGER DEFAULT 0,
    sacrifice_flies INTEGER DEFAULT 0,
    batting_average REAL DEFAULT 0.0,
    on_base_percentage REAL DEFAULT 0.0,
    slugging_percentage REAL DEFAULT 0.0,
    ops REAL DEFAULT 0.0,
    -- Advanced metrics (when available)
    ops_plus INTEGER,
    war REAL,
    woba REAL,
    -- Data quality metadata
    data_source TEXT NOT NULL,
    data_quality TEXT DEFAULT 'complete', -- complete, traditional, partial, estimated
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    UNIQUE(player_id, season, team_id)
);

-- Pitching statistics table
CREATE TABLE IF NOT EXISTS pitching_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id TEXT NOT NULL,
    season INTEGER NOT NULL,
    team_id TEXT,
    league TEXT,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    era REAL DEFAULT 0.0,
    games INTEGER DEFAULT 0,
    games_started INTEGER DEFAULT 0,
    complete_games INTEGER DEFAULT 0,
    shutouts INTEGER DEFAULT 0,
    saves INTEGER DEFAULT 0,
    holds INTEGER DEFAULT 0,
    innings_pitched REAL DEFAULT 0.0,
    hits_allowed INTEGER DEFAULT 0,
    runs_allowed INTEGER DEFAULT 0,
    earned_runs INTEGER DEFAULT 0,
    home_runs_allowed INTEGER DEFAULT 0,
    walks INTEGER DEFAULT 0,
    strikeouts INTEGER DEFAULT 0,
    wild_pitches INTEGER DEFAULT 0,
    hit_batters INTEGER DEFAULT 0,
    whip REAL DEFAULT 0.0,
    -- Advanced metrics (when available)
    era_plus INTEGER,
    fip REAL,
    war REAL,
    strikeouts_per_nine REAL,
    walks_per_nine REAL,
    -- Data quality metadata
    data_source TEXT NOT NULL,
    data_quality TEXT DEFAULT 'complete',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    UNIQUE(player_id, season, team_id)
);

-- Career totals view for batting
CREATE VIEW IF NOT EXISTS batting_career_totals AS
SELECT 
    player_id,
    COUNT(DISTINCT season) as seasons,
    SUM(games) as games,
    SUM(plate_appearances) as plate_appearances,
    SUM(at_bats) as at_bats,
    SUM(runs) as runs,
    SUM(hits) as hits,
    SUM(doubles) as doubles,
    SUM(triples) as triples,
    SUM(home_runs) as home_runs,
    SUM(rbis) as rbis,
    SUM(stolen_bases) as stolen_bases,
    SUM(caught_stealing) as caught_stealing,
    SUM(walks) as walks,
    SUM(strikeouts) as strikeouts,
    CASE WHEN SUM(at_bats) > 0 THEN ROUND(CAST(SUM(hits) AS REAL) / SUM(at_bats), 3) ELSE 0.0 END as batting_average,
    CASE WHEN (SUM(at_bats) + SUM(walks) + SUM(hit_by_pitch) + SUM(sacrifice_flies)) > 0 
        THEN ROUND(CAST(SUM(hits) + SUM(walks) + SUM(hit_by_pitch) AS REAL) / 
            (SUM(at_bats) + SUM(walks) + SUM(hit_by_pitch) + SUM(sacrifice_flies)), 3) 
        ELSE 0.0 END as on_base_percentage,
    CASE WHEN SUM(at_bats) > 0 
        THEN ROUND(CAST(SUM(hits) + SUM(doubles) + 2*SUM(triples) + 3*SUM(home_runs) AS REAL) / SUM(at_bats), 3) 
        ELSE 0.0 END as slugging_percentage,
    CASE WHEN SUM(at_bats) > 0 
        THEN ROUND(
            CAST(SUM(hits) + SUM(walks) + SUM(hit_by_pitch) AS REAL) / 
            (SUM(at_bats) + SUM(walks) + SUM(hit_by_pitch) + SUM(sacrifice_flies)) +
            CAST(SUM(hits) + SUM(doubles) + 2*SUM(triples) + 3*SUM(home_runs) AS REAL) / SUM(at_bats), 3
        )
        ELSE 0.0 END as ops
FROM batting_stats
GROUP BY player_id;

-- Career totals view for pitching
CREATE VIEW IF NOT EXISTS pitching_career_totals AS
SELECT 
    player_id,
    COUNT(DISTINCT season) as seasons,
    SUM(wins) as wins,
    SUM(losses) as losses,
    SUM(games) as games,
    SUM(games_started) as games_started,
    SUM(complete_games) as complete_games,
    SUM(shutouts) as shutouts,
    SUM(saves) as saves,
    SUM(innings_pitched) as innings_pitched,
    SUM(hits_allowed) as hits_allowed,
    SUM(runs_allowed) as runs_allowed,
    SUM(earned_runs) as earned_runs,
    SUM(home_runs_allowed) as home_runs_allowed,
    SUM(walks) as walks,
    SUM(strikeouts) as strikeouts,
    CASE WHEN SUM(innings_pitched) > 0 
        THEN ROUND(CAST(SUM(earned_runs) * 9 AS REAL) / SUM(innings_pitched), 2) 
        ELSE 0.0 END as era,
    CASE WHEN SUM(innings_pitched) > 0 
        THEN ROUND(CAST(SUM(hits_allowed) + SUM(walks) AS REAL) / SUM(innings_pitched), 3) 
        ELSE 0.0 END as whip
FROM pitching_stats
GROUP BY player_id;

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_batting_player_season ON batting_stats(player_id, season);
CREATE INDEX IF NOT EXISTS idx_batting_season ON batting_stats(season);
CREATE INDEX IF NOT EXISTS idx_batting_team ON batting_stats(team_id);
CREATE INDEX IF NOT EXISTS idx_pitching_player_season ON pitching_stats(player_id, season);
CREATE INDEX IF NOT EXISTS idx_pitching_season ON pitching_stats(season);
CREATE INDEX IF NOT EXISTS idx_pitching_team ON pitching_stats(team_id);
CREATE INDEX IF NOT EXISTS idx_players_name ON players(name_english);
CREATE INDEX IF NOT EXISTS idx_players_romanized ON players(name_romanized_variants);

-- Trigger to update timestamps
CREATE TRIGGER IF NOT EXISTS update_players_timestamp 
AFTER UPDATE ON players
BEGIN
    UPDATE players SET updated_at = CURRENT_TIMESTAMP WHERE player_id = NEW.player_id;
END;

CREATE TRIGGER IF NOT EXISTS update_batting_timestamp 
AFTER UPDATE ON batting_stats
BEGIN
    UPDATE batting_stats SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_pitching_timestamp 
AFTER UPDATE ON pitching_stats
BEGIN
    UPDATE pitching_stats SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;