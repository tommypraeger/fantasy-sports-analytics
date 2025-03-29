from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from enum import Enum


class Platform(str, Enum):
    ESPN = "espn"
    SLEEPER = "sleeper"


class Sport(str, Enum):
    FOOTBALL = "football"
    BASEBALL = "baseball"
    BASKETBALL = "basketball"


@dataclass
class Matchup:
    """Standardized matchup data across platforms"""
    matchup_id: str  # Platform-specific matchup ID
    week: int
    home_team_id: str
    away_team_id: str
    home_score: Optional[float] = None
    away_score: Optional[float] = None
    is_playoffs: bool = False
    platform: Platform = field(init=False)  # Set by platform-specific code


@dataclass
class LeagueInfo:
    """Information needed to fetch a league"""
    platform: Platform
    league_id: str
    year: int
    sport: Sport = Sport.FOOTBALL
    espn_s2: Optional[str] = None  # Only needed for private ESPN leagues


@dataclass
class Team:
    """Team data"""
    id: str
    name: str
    scores: List[float] = field(default_factory=list)
    matchups: List[Matchup] = field(default_factory=list)  # List of Matchup objects
    wins: int = 0
    opponents: List[str] = field(default_factory=list)  # List of opponent team IDs
    opponent_average_scores: List[float] = field(default_factory=list)
    opponent_std_devs: List[float] = field(default_factory=list)
    win_likelihoods: List[float] = field(default_factory=list)
    win_total_probs: List[float] = field(default_factory=list)
    future_win_total_probs: List[float] = field(default_factory=list)
    average_score: float = 0
    score_std_dev: float = 0


@dataclass
class League:
    """League data"""
    id: str = ""
    name: str = ""
    year: int = 0
    sport: Sport = Sport.FOOTBALL
    total_matchups: int = 0
    num_teams: int = 0
    curr_matchups_played: int = 0
    teams: List[Team] = field(default_factory=list)
    matchups: List[Matchup] = field(default_factory=list)  # All matchups in the league
    schedule: List[Dict] = field(default_factory=list)  # Raw schedule data from platform
    team_map: Dict[str, Team] = field(default_factory=dict)
    score_multipliers: Dict[str, float] = field(default_factory=dict) 