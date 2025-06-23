"""NPB data models."""

from dataclasses import dataclass
from typing import Optional, List
from datetime import date


@dataclass
class NPBPlayer:
    """NPB player information."""
    id: str  # Unique identifier (initially name-based)
    name_english: str
    name_japanese: Optional[str] = None
    team_id: Optional[str] = None
    team_name: Optional[str] = None
    position: Optional[str] = None
    jersey_number: Optional[int] = None
    birth_date: Optional[date] = None
    height: Optional[str] = None  # e.g., "180cm"
    weight: Optional[str] = None  # e.g., "80kg"
    bats: Optional[str] = None  # L/R/S
    throws: Optional[str] = None  # L/R


@dataclass
class NPBBattingStats:
    """NPB batting statistics."""
    player_id: str
    season: int
    team: Optional[str] = None
    games: int = 0
    plate_appearances: int = 0
    at_bats: int = 0
    runs: int = 0
    hits: int = 0
    doubles: int = 0
    triples: int = 0
    home_runs: int = 0
    rbis: int = 0
    stolen_bases: int = 0
    caught_stealing: int = 0
    walks: int = 0
    strikeouts: int = 0
    batting_average: float = 0.0
    on_base_percentage: float = 0.0
    slugging_percentage: float = 0.0
    ops: float = 0.0
    # Advanced metrics when available
    war: Optional[float] = None
    woba: Optional[float] = None
    wrc_plus: Optional[int] = None
    ops_plus: Optional[int] = None


@dataclass
class NPBPitchingStats:
    """NPB pitching statistics."""
    player_id: str
    season: int
    team: Optional[str] = None
    games: int = 0
    games_started: int = 0
    complete_games: int = 0
    shutouts: int = 0
    wins: int = 0
    losses: int = 0
    saves: int = 0
    holds: int = 0
    innings_pitched: float = 0.0
    hits_allowed: int = 0
    runs_allowed: int = 0
    earned_runs: int = 0
    home_runs_allowed: int = 0
    walks: int = 0
    strikeouts: int = 0
    era: float = 0.0
    whip: float = 0.0
    strikeouts_per_nine: float = 0.0
    walks_per_nine: float = 0.0
    # Advanced metrics when available
    fip: Optional[float] = None
    war: Optional[float] = None
    era_plus: Optional[int] = None


@dataclass
class NPBTeamStanding:
    """NPB team standing information."""
    team_id: str
    team_name: str
    league: str  # "central" or "pacific"
    season: int
    wins: int
    losses: int
    ties: int
    winning_percentage: float
    games_behind: float
    runs_scored: int
    runs_allowed: int
    
    @property
    def games_played(self) -> int:
        """Total games played."""
        return self.wins + self.losses + self.ties