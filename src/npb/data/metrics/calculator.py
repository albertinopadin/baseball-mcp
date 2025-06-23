"""Calculate advanced metrics for NPB players."""

import logging
from typing import Dict, Any, List, Optional

from .constants import (
    NPB_FIP_CONSTANT,
    NPB_WOBA_WEIGHTS,
    NPB_LEAGUE_FACTORS,
    NPB_REPLACEMENT_LEVEL_BATTING,
    NPB_REPLACEMENT_LEVEL_PITCHING,
    NPB_RUNS_PER_WIN
)

logger = logging.getLogger(__name__)


class NPBMetricsCalculator:
    """Calculate advanced metrics for NPB statistics."""
    
    @staticmethod
    def calculate_fip(hr: int, bb: int, hbp: int, k: int, ip: float) -> Optional[float]:
        """Calculate Fielding Independent Pitching (FIP).
        
        FIP = ((13*HR + 3*(BB + HBP) - 2*K) / IP) + FIP_constant
        
        Args:
            hr: Home runs allowed
            bb: Walks
            hbp: Hit by pitch
            k: Strikeouts
            ip: Innings pitched
            
        Returns:
            FIP value or None if IP is 0
        """
        if ip <= 0:
            return None
        
        fip = ((13 * hr + 3 * (bb + hbp) - 2 * k) / ip) + NPB_FIP_CONSTANT
        return round(fip, 2)
    
    @staticmethod
    def calculate_woba(bb: int, hbp: int, singles: int, doubles: int, 
                      triples: int, hr: int, ab: int, sf: int) -> Optional[float]:
        """Calculate weighted On-Base Average (wOBA).
        
        Uses NPB-specific linear weights.
        
        Args:
            bb: Walks
            hbp: Hit by pitch
            singles: Singles (hits - doubles - triples - hr)
            doubles: Doubles
            triples: Triples
            hr: Home runs
            ab: At bats
            sf: Sacrifice flies
            
        Returns:
            wOBA value or None if denominator is 0
        """
        denominator = ab + bb + sf + hbp
        if denominator <= 0:
            return None
        
        numerator = (
            NPB_WOBA_WEIGHTS['bb'] * bb +
            NPB_WOBA_WEIGHTS['hbp'] * hbp +
            NPB_WOBA_WEIGHTS['1b'] * singles +
            NPB_WOBA_WEIGHTS['2b'] * doubles +
            NPB_WOBA_WEIGHTS['3b'] * triples +
            NPB_WOBA_WEIGHTS['hr'] * hr
        )
        
        woba = numerator / denominator
        return round(woba, 3)
    
    @staticmethod
    def calculate_ops_plus(ops: float, league_ops: float = 0.750) -> Optional[int]:
        """Calculate OPS+ (park and league adjusted).
        
        Simplified version without park factors.
        100 is league average.
        
        Args:
            ops: Player's OPS
            league_ops: League average OPS (default 0.750 for NPB)
            
        Returns:
            OPS+ value
        """
        if league_ops <= 0:
            return None
        
        ops_plus = 100 * (ops / league_ops)
        return round(ops_plus)
    
    @staticmethod
    def calculate_era_plus(era: float, league_era: float = 3.50) -> Optional[int]:
        """Calculate ERA+ (park and league adjusted).
        
        Simplified version without park factors.
        100 is league average. Higher is better for pitchers.
        
        Args:
            era: Player's ERA
            league_era: League average ERA (default 3.50 for NPB)
            
        Returns:
            ERA+ value
        """
        if era <= 0:
            return None
        
        era_plus = 100 * (league_era / era)
        return round(era_plus)
    
    @staticmethod
    def calculate_basic_batting_war(
        runs_created: float,
        games: int,
        position: str = "DH",
        league: str = "pacific"
    ) -> float:
        """Calculate a simplified batting WAR.
        
        This is a very basic implementation without:
        - Defensive runs
        - Baserunning runs
        - Proper positional adjustment
        - Park factors
        
        Args:
            runs_created: Runs created by the player
            games: Games played
            position: Defensive position
            league: Central or Pacific
            
        Returns:
            Basic WAR estimate
        """
        # Simple positional adjustment (runs per 162 games)
        positional_adjustments = {
            "C": 12.5,    # Catcher
            "SS": 7.5,    # Shortstop
            "2B": 2.5,    # Second base
            "3B": 2.5,    # Third base
            "CF": 2.5,    # Center field
            "RF": -7.5,   # Right field
            "LF": -7.5,   # Left field
            "1B": -12.5,  # First base
            "DH": -17.5   # Designated hitter
        }
        
        # Get positional adjustment
        pos_adjustment = positional_adjustments.get(position, 0)
        
        # Scale to games played
        games_factor = games / 162.0
        
        # Calculate runs above replacement
        replacement_runs = NPB_REPLACEMENT_LEVEL_BATTING * NPB_RUNS_PER_WIN * games_factor
        runs_above_replacement = runs_created - replacement_runs + (pos_adjustment * games_factor)
        
        # Convert to wins
        war = runs_above_replacement / NPB_RUNS_PER_WIN
        
        return round(war, 1)
    
    @staticmethod
    def calculate_basic_pitching_war(
        fip: float,
        ip: float,
        league_fip: float = 3.80
    ) -> float:
        """Calculate a simplified pitching WAR based on FIP.
        
        Args:
            fip: Fielding Independent Pitching
            ip: Innings pitched
            league_fip: League average FIP
            
        Returns:
            Basic WAR estimate
        """
        # Calculate runs above average
        runs_above_average = ((league_fip - fip) / 9) * ip
        
        # Add replacement level
        replacement_level_runs = (NPB_REPLACEMENT_LEVEL_PITCHING * NPB_RUNS_PER_WIN * (ip / 200))
        
        # Total runs above replacement
        runs_above_replacement = runs_above_average + replacement_level_runs
        
        # Convert to wins
        war = runs_above_replacement / NPB_RUNS_PER_WIN
        
        return round(war, 1)
    
    @classmethod
    def enhance_batting_stats(cls, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Add calculated advanced metrics to batting statistics.
        
        Args:
            stats: Dictionary of batting statistics
            
        Returns:
            Enhanced stats dictionary with calculated metrics
        """
        # Calculate singles
        hits = stats.get('hits', 0)
        doubles = stats.get('doubles', 0)
        triples = stats.get('triples', 0)
        home_runs = stats.get('home_runs', 0)
        singles = hits - doubles - triples - home_runs
        
        # Calculate wOBA if we have the necessary stats
        if all(k in stats for k in ['walks', 'hit_by_pitch', 'at_bats', 'sacrifice_flies']):
            woba = cls.calculate_woba(
                bb=stats['walks'],
                hbp=stats.get('hit_by_pitch', 0),
                singles=singles,
                doubles=doubles,
                triples=triples,
                hr=home_runs,
                ab=stats['at_bats'],
                sf=stats.get('sacrifice_flies', 0)
            )
            if woba:
                stats['woba'] = woba
        
        # Calculate OPS+ if we have OPS
        if 'ops' in stats and stats['ops'] > 0:
            ops_plus = cls.calculate_ops_plus(stats['ops'])
            if ops_plus:
                stats['ops_plus'] = ops_plus
        
        # Simple runs created estimate (basic runs created formula)
        if all(k in stats for k in ['hits', 'walks', 'at_bats']):
            # Basic runs created: ((H + BB) * TB) / (AB + BB)
            total_bases = singles + 2*doubles + 3*triples + 4*home_runs
            numerator = (hits + stats['walks']) * total_bases
            denominator = stats['at_bats'] + stats['walks']
            if denominator > 0:
                runs_created = numerator / denominator
                stats['runs_created'] = round(runs_created, 1)
                
                # Calculate basic WAR if we have games
                if 'games' in stats:
                    war = cls.calculate_basic_batting_war(
                        runs_created=runs_created,
                        games=stats['games']
                    )
                    stats['war_estimate'] = war
        
        return stats
    
    @classmethod
    def enhance_pitching_stats(cls, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Add calculated advanced metrics to pitching statistics.
        
        Args:
            stats: Dictionary of pitching statistics
            
        Returns:
            Enhanced stats dictionary with calculated metrics
        """
        # Calculate FIP if we have the necessary stats
        if all(k in stats for k in ['home_runs_allowed', 'walks', 'strikeouts', 'innings_pitched']):
            if stats['innings_pitched'] > 0:
                fip = cls.calculate_fip(
                    hr=stats['home_runs_allowed'],
                    bb=stats['walks'],
                    hbp=stats.get('hit_batters', 0),
                    k=stats['strikeouts'],
                    ip=stats['innings_pitched']
                )
                if fip:
                    stats['fip'] = fip
                    
                    # Calculate basic pitching WAR
                    war = cls.calculate_basic_pitching_war(
                        fip=fip,
                        ip=stats['innings_pitched']
                    )
                    stats['war_estimate'] = war
        
        # Calculate ERA+ if we have ERA
        if 'era' in stats and stats['era'] > 0:
            era_plus = cls.calculate_era_plus(stats['era'])
            if era_plus:
                stats['era_plus'] = era_plus
        
        return stats