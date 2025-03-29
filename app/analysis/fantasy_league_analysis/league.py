from typing import Dict, List

from app.analysis.fantasy_league_analysis.models import League as LeagueModel, LeagueInfo, Platform, Sport, Team, Matchup
from app.analysis.fantasy_league_analysis.fetch_espn import fetch_league as fetch_espn_league
from app.analysis.fantasy_league_analysis.fetch_sleeper import fetch_league as fetch_sleeper_league


class League:
    def __init__(self, league_info: Dict):
        """Initialize a fantasy league with the given information"""
        platform = Platform(league_info["platform"])
        info = LeagueInfo(
            platform=platform,
            league_id=league_info["leagueId"],
            year=league_info.get("year", 2024) if platform == Platform.ESPN else 2024,  # ESPN requires year, Sleeper doesn't
            sport=league_info.get("sport", "football"),
            espn_s2=league_info.get("espnS2")
        )
        
        # Initialize empty league model
        self.model = LeagueModel(
            sport=info.sport,
            id=info.league_id,
            year=info.year,
            name="",
            schedule=[],
            teams=[],
            team_map={},
            curr_matchups_played=0,
            total_matchups=0,
            num_teams=0,
            score_multipliers={}
        )
        
        # Fetch league data based on platform
        if info.platform == Platform.ESPN:
            fetch_espn_league(self.model, info)
        elif info.platform == Platform.SLEEPER:
            fetch_sleeper_league(self.model, info)
        else:
            raise ValueError(f"Unsupported platform: {info.platform}")
            
        # Sort teams by win likelihood
        self.model.teams.sort(
            key=lambda team: sum(team.win_likelihoods[: self.model.curr_matchups_played]),
            reverse=True,
        )

    def get_team(self, team_id: int) -> Team:
        """Return a team object given a team id"""
        return self.model.team_map[team_id]
        
    @property
    def teams(self) -> List[Team]:
        return self.model.teams
        
    @property
    def name(self) -> str:
        return self.model.name
        
    @property
    def id(self) -> str:
        return self.model.id
        
    @property
    def year(self) -> int:
        return self.model.year

    @property
    def curr_matchups_played(self) -> int:
        return self.model.curr_matchups_played

    @property
    def total_matchups(self) -> int:
        return self.model.total_matchups

    @property
    def num_teams(self) -> int:
        return self.model.num_teams

    @property
    def sport(self) -> Sport:
        return self.model.sport

    @property
    def matchups(self) -> List[Matchup]:
        return self.model.matchups

    @property
    def schedule(self) -> List[Dict]:
        return self.model.schedule

    @property
    def team_map(self) -> Dict[str, Team]:
        return self.model.team_map

    @property
    def score_multipliers(self) -> Dict[str, float]:
        return self.model.score_multipliers
