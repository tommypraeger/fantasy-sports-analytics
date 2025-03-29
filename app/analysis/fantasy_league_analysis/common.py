from typing import List, Dict, Union
from app.analysis.fantasy_league_analysis.models import League as LeagueModel, Team, Matchup
from app.analysis.fantasy_league_analysis.analysis import (
    std_dev,
    get_win_likelihoods,
    get_win_total_probs,
    get_future_win_total_probs,
)


def perform_team_analysis(league: LeagueModel) -> None:
    """Analyze all teams in the league"""
    for team in league.teams:
        get_team_metadata(team, league)
    for team in league.teams:
        analyze_team(league, team)


def get_team_metadata(team: Team, league: LeagueModel) -> None:
    """Get metadata for a team pre-analysis"""
    initialize_team(team, league)
    get_matchups(team, league)
    get_opponents(team, league)
    get_average_score(team, league.curr_matchups_played)
    get_adj_std_dev(team, league.curr_matchups_played)


def analyze_team(league: LeagueModel, team: Team) -> None:
    """Analyze a single team's performance"""
    get_win_likelihoods(league, team)
    get_win_total_probs(league, team)
    get_future_win_total_probs(league, team)


def initialize_team(team: Team, league: LeagueModel) -> None:
    """Fill in team skeleton"""
    team.name = team.name  # This will be set by the platform-specific code
    team.id = team.id  # This will be set by the platform-specific code
    team.scores = []
    team.matchups = []
    team.wins = 0
    team.opponents = []
    team.opponent_average_scores = []
    team.opponent_std_devs = []
    team.win_likelihoods = []
    team.win_total_probs = []
    team.future_win_total_probs = []


def get_matchups(team: Team, league: LeagueModel) -> None:
    """Get all matchups for a team"""
    for matchup in league.matchups:
        if matchup.home_team_id == team.id:
            team.matchups.append(matchup)
            if matchup.home_score is not None:
                team.scores.append(matchup.home_score)
                if matchup.home_score > matchup.away_score:
                    team.wins += 1
        elif matchup.away_team_id == team.id:
            team.matchups.append(matchup)
            if matchup.away_score is not None:
                team.scores.append(matchup.away_score)
                if matchup.away_score > matchup.home_score:
                    team.wins += 1


def get_opponent(team: Team, matchup: Matchup) -> str:
    """Get the opponent ID for a given matchup"""
    if matchup.home_team_id == team.id:
        return matchup.away_team_id
    return matchup.home_team_id


def get_score(team: Team, score: float, week: int, curr_matchups_played: int) -> float:
    """Get a team's score for a given week"""
    if week > curr_matchups_played:
        return None
    return score


def get_opponents(team: Team, league: LeagueModel) -> None:
    """Get all opponents for a team"""
    for matchup in team.matchups:
        team.opponents.append(get_opponent(team, matchup))


def get_average_score(team: Team, curr_matchups_played: int) -> float:
    """Calculate average score for a team"""
    if not team.scores:
        return 0
    team.average_score = sum(team.scores) / len(team.scores)


def get_curr_matchups_played(league: LeagueModel) -> int:
    """Get the number of matchups played so far"""
    played = 0
    for matchup in league.matchups:
        if matchup.home_score is not None and matchup.away_score is not None:
            played += 1

    # Divide by number of teams to get number of matchups played
    # Multiply by 2 because 2 teams play each other
    return played // league.num_teams * 2


# I slightly increase standard deviation to reduce the confidence of the predictions
# Fantasy scores aren't really random variables,
# so I figured I should make the predictions slightly less confident
# Adj std dev = std dev * (n+1)/n, where n is the number of games played
def get_adj_std_dev(team: Team, curr_matchups_played: int) -> float:
    """Calculate adjusted standard deviation for a team's scores"""
    if len(team.scores) < 2:
        return 0
    adj_std_dev = std_dev(team.scores) * (curr_matchups_played + 1) / curr_matchups_played
    team.score_std_dev = adj_std_dev 