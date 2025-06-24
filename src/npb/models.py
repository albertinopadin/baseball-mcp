"""Data models for NPB entities."""

from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum


class NPBLeague(Enum):
    """NPB league enumeration."""
    CENTRAL = "Central League"
    PACIFIC = "Pacific League"


class NPBTeam:
    """NPB team data model."""
    
    def __init__(
        self,
        id: str,
        name_english: str,
        name_japanese: Optional[str] = None,
        abbreviation: Optional[str] = None,
        league: Optional[NPBLeague] = None,
        city: Optional[str] = None,
        stadium: Optional[str] = None,
        founded: Optional[int] = None,
        source: Optional[str] = None,
        source_id: Optional[str] = None
    ):
        self.id = id  # Unified ID
        self.name_english = name_english
        self.name_japanese = name_japanese
        self.abbreviation = abbreviation
        self.league = league
        self.city = city
        self.stadium = stadium
        self.founded = founded
        self.source = source
        self.source_id = source_id  # Native ID from source
        self.source_ids: Dict[str, str] = {}  # Map of source -> native ID
        
        if source and source_id:
            self.source_ids[source] = source_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "name_english": self.name_english,
            "name_japanese": self.name_japanese,
            "abbreviation": self.abbreviation,
            "league": self.league.value if self.league else None,
            "city": self.city,
            "stadium": self.stadium,
            "founded": self.founded,
            "source": self.source,
            "source_ids": self.source_ids
        }


class NPBPlayer:
    """NPB player data model."""
    
    def __init__(
        self,
        id: str,
        name_english: str,
        name_japanese: Optional[str] = None,
        team: Optional[NPBTeam] = None,
        jersey_number: Optional[str] = None,
        position: Optional[str] = None,
        birth_date: Optional[str] = None,
        height: Optional[str] = None,
        weight: Optional[str] = None,
        bats: Optional[str] = None,
        throws: Optional[str] = None,
        source: Optional[str] = None,
        source_id: Optional[str] = None
    ):
        self.id = id  # Unified ID
        self.name_english = name_english
        self.name_japanese = name_japanese
        self.team = team
        self.jersey_number = jersey_number
        self.position = position
        self.birth_date = birth_date
        self.height = height
        self.weight = weight
        self.bats = bats
        self.throws = throws
        self.source = source
        self.source_id = source_id  # Native ID from source
        self.source_ids: Dict[str, str] = {}  # Map of source -> native ID
        
        if source and source_id:
            self.source_ids[source] = source_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "name_english": self.name_english,
            "name_japanese": self.name_japanese,
            "team": self.team.to_dict() if self.team else None,
            "jersey_number": self.jersey_number,
            "position": self.position,
            "birth_date": self.birth_date,
            "height": self.height,
            "weight": self.weight,
            "bats": self.bats,
            "throws": self.throws,
            "source": self.source,
            "source_ids": self.source_ids
        }


class NPBPlayerStats:
    """NPB player statistics data model."""
    
    def __init__(
        self,
        player_id: str,
        season: int,
        stats_type: str = "batting",  # "batting" or "pitching"
        team: Optional[NPBTeam] = None,
        games: Optional[int] = None,
        # Batting stats
        plate_appearances: Optional[int] = None,
        at_bats: Optional[int] = None,
        runs: Optional[int] = None,
        hits: Optional[int] = None,
        doubles: Optional[int] = None,
        triples: Optional[int] = None,
        home_runs: Optional[int] = None,
        rbi: Optional[int] = None,
        stolen_bases: Optional[int] = None,
        caught_stealing: Optional[int] = None,
        walks: Optional[int] = None,
        strikeouts: Optional[int] = None,
        batting_average: Optional[float] = None,
        on_base_percentage: Optional[float] = None,
        slugging_percentage: Optional[float] = None,
        ops: Optional[float] = None,
        # Pitching stats
        wins: Optional[int] = None,
        losses: Optional[int] = None,
        saves: Optional[int] = None,
        holds: Optional[int] = None,
        innings_pitched: Optional[float] = None,
        hits_allowed: Optional[int] = None,
        runs_allowed: Optional[int] = None,
        earned_runs: Optional[int] = None,
        home_runs_allowed: Optional[int] = None,
        walks_allowed: Optional[int] = None,
        strikeouts_pitched: Optional[int] = None,
        era: Optional[float] = None,
        whip: Optional[float] = None,
        # Advanced stats (when available)
        war: Optional[float] = None,
        wrc_plus: Optional[int] = None,
        xwoba: Optional[float] = None,
        fip: Optional[float] = None,
        xfip: Optional[float] = None,
        # Metadata
        source: Optional[str] = None,
        last_updated: Optional[datetime] = None
    ):
        self.player_id = player_id
        self.season = season
        self.stats_type = stats_type
        self.team = team
        self.games = games
        
        # Batting stats
        self.plate_appearances = plate_appearances
        self.at_bats = at_bats
        self.runs = runs
        self.hits = hits
        self.doubles = doubles
        self.triples = triples
        self.home_runs = home_runs
        self.rbi = rbi
        self.stolen_bases = stolen_bases
        self.caught_stealing = caught_stealing
        self.walks = walks
        self.strikeouts = strikeouts
        self.batting_average = batting_average
        self.on_base_percentage = on_base_percentage
        self.slugging_percentage = slugging_percentage
        self.ops = ops
        
        # Pitching stats
        self.wins = wins
        self.losses = losses
        self.saves = saves
        self.holds = holds
        self.innings_pitched = innings_pitched
        self.hits_allowed = hits_allowed
        self.runs_allowed = runs_allowed
        self.earned_runs = earned_runs
        self.home_runs_allowed = home_runs_allowed
        self.walks_allowed = walks_allowed
        self.strikeouts_pitched = strikeouts_pitched
        self.era = era
        self.whip = whip
        
        # Advanced stats
        self.war = war
        self.wrc_plus = wrc_plus
        self.xwoba = xwoba
        self.fip = fip
        self.xfip = xfip
        
        # Metadata
        self.source = source
        self.last_updated = last_updated or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        data = {
            "player_id": self.player_id,
            "season": self.season,
            "stats_type": self.stats_type,
            "team": self.team.to_dict() if self.team else None,
            "games": self.games,
            "source": self.source,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }
        
        if self.stats_type == "batting":
            data.update({
                "plate_appearances": self.plate_appearances,
                "at_bats": self.at_bats,
                "runs": self.runs,
                "hits": self.hits,
                "doubles": self.doubles,
                "triples": self.triples,
                "home_runs": self.home_runs,
                "rbi": self.rbi,
                "stolen_bases": self.stolen_bases,
                "caught_stealing": self.caught_stealing,
                "walks": self.walks,
                "strikeouts": self.strikeouts,
                "batting_average": self.batting_average,
                "on_base_percentage": self.on_base_percentage,
                "slugging_percentage": self.slugging_percentage,
                "ops": self.ops
            })
        else:  # pitching
            data.update({
                "wins": self.wins,
                "losses": self.losses,
                "saves": self.saves,
                "holds": self.holds,
                "innings_pitched": self.innings_pitched,
                "hits_allowed": self.hits_allowed,
                "runs_allowed": self.runs_allowed,
                "earned_runs": self.earned_runs,
                "home_runs_allowed": self.home_runs_allowed,
                "walks_allowed": self.walks_allowed,
                "strikeouts": self.strikeouts_pitched,
                "era": self.era,
                "whip": self.whip
            })
        
        # Add advanced stats if available
        if self.war is not None:
            data["war"] = self.war
        if self.wrc_plus is not None:
            data["wrc_plus"] = self.wrc_plus
        if self.xwoba is not None:
            data["xwoba"] = self.xwoba
        if self.fip is not None:
            data["fip"] = self.fip
        if self.xfip is not None:
            data["xfip"] = self.xfip
            
        return data