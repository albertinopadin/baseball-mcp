"""NPB-specific constants for advanced metrics calculations."""

# FIP (Fielding Independent Pitching) constant
# MLB uses ~3.20, NPB typically runs lower due to different ball/environment
# This is an estimate and should be refined with more research
NPB_FIP_CONSTANT = 3.10

# Linear weights for wOBA calculation
# These are NPB-specific values (approximate)
# MLB values differ due to different run environment
NPB_WOBA_WEIGHTS = {
    'bb': 0.69,      # Walk
    'hbp': 0.72,     # Hit by pitch
    '1b': 0.88,      # Single
    '2b': 1.24,      # Double
    '3b': 1.56,      # Triple
    'hr': 1.95,      # Home run
}

# League run environment factors (for park adjustments)
# These would need to be calculated per season ideally
NPB_LEAGUE_FACTORS = {
    'central': 1.00,  # Central League (no DH)
    'pacific': 1.05,  # Pacific League (has DH, typically more runs)
}

# Replacement level constants
# Wins per 600 PA for position players
NPB_REPLACEMENT_LEVEL_BATTING = 2.0
# Wins per 200 IP for pitchers
NPB_REPLACEMENT_LEVEL_PITCHING = 2.0

# Runs per win converter
# Slightly different from MLB due to run environment
NPB_RUNS_PER_WIN = 9.5