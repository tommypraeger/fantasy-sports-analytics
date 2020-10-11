import requests

from app.analysis.fantasy_league_analysis.analysis import (
    std_dev,
    get_win_likelihoods,
    get_win_total_probs,
    get_future_win_total_probs
)
from app.analysis.fantasy_league_analysis.team import Team


def fetch_league(league, league_info) -> None:
    '''Load league and set metadata for league and teams'''

    league.id = league_info['leagueId']

    # Necessary Sleeper API URLs
    league_url = f'https://api.sleeper.app/v1/league/{league.id}'
    teams_url = f'https://api.sleeper.app/v1/league/{league.id}/rosters'
    users_url = f'https://api.sleeper.app/v1/league/{league.id}/users'

    with requests.Session() as session:
        exception_message = ('Something went wrong fetching your league. '
                             'Make sure your league ID is correct.')

        # Make requests and check if it succeeds
        league_resp = session.get(league_url)
        if league_resp.status_code >= 400:
            raise Exception(exception_message)
        teams_resp = session.get(teams_url)
        if teams_resp.status_code >= 400:
            raise Exception(exception_message)
        users_resp = session.get(users_url)
        if users_resp.status_code >= 400:
            raise Exception(exception_message)

        league_json = league_resp.json()
        teams = teams_resp.json()
        users = users_resp.json()

        league.name = league_json['name']
        league.total_matchups = league_json['settings']['playoff_week_start'] - 1
        get_league_schedule(league, session)
        league.curr_matchups_played = get_curr_matchups_played(teams[0])

    # Can't do analysis with less than 2 games played
    if league.curr_matchups_played < 2:
        raise Exception('There must have been at least 2 matchups played already.')

    league.num_teams = league_json['settings']['num_teams']

    for team_info in teams:
        team_obj = Team()
        get_team_metadata(team_obj, team_info, users, league)
        league.teams.append(team_obj)
        league.team_map[team_obj.id] = team_obj

    # Need other team data to be complete before this can be done
    for team in league.teams:
        get_opponents(team, league)


def get_league_schedule(league, session) -> None:
    '''Get schedule for league'''

    matchups_url = 'https://api.sleeper.app/v1/league/{}/matchups/{}'

    for week in range(1, league.total_matchups + 1):
        matchups = session.get(matchups_url.format(league.id, week))
        league.schedule.append(matchups.json())

def perform_team_analysis(league) -> None:
    '''Perform all the statistics and analysis for each team'''

    for team in league.teams:
        analyze_team(league, team)


def analyze_team(league, team) -> None:
    '''Calculate win expectancies'''

    get_win_likelihoods(league, team)
    get_win_total_probs(league, team)
    get_future_win_total_probs(league, team)


def get_curr_matchups_played(team: dict) -> int:
    '''Get current number of matchups played'''

    settings = team['settings']
    return settings['wins'] + settings['losses'] + settings['ties']


def get_team_metadata(team, team_info: dict, users: list, league) -> None:
    '''Calculate team-specific score data'''

    team.id = team_info['roster_id']
    team.name = get_user_name(users, team_info['owner_id'])
    team.wins = team_info['settings']['wins']
    get_matchups(team, league)
    team.average_score = get_average_score(team, league.curr_matchups_played)
    team.score_std_dev = get_adj_std_dev(team, league.curr_matchups_played)


def get_user_name(users: list, user_id: str) -> str:
    '''Get user name for a team'''

    for user in users:
        if user['user_id'] == user_id:
            return user['display_name']

    return 'User not found'


def get_matchups(team, league) -> None:
    '''Get matchups for a team'''

    for week, matchups in enumerate(league.schedule, 1):
        for matchup_json in matchups:
            if matchup_json['roster_id'] == team.id:
                matchup = {}
                matchup['week'] = week
                matchup['score'] = get_score(team,
                                             matchup_json['points'],
                                             week,
                                             league.curr_matchups_played)
                matchup['opponent'] = get_opponent(team, matchup_json['matchup_id'], matchups)
                matchup['won'] = is_win(team,
                                        matchup_json['matchup_id'],
                                        matchups,
                                        week,
                                        league.curr_matchups_played)
                team.matchups.append(matchup)


def get_opponent(team, matchup_id: int, matchups: list) -> int:
    '''Get opponent for a matchup'''

    # Opponent has same matchup_id and different roster_id
    for matchup in matchups:
        if matchup['matchup_id'] == matchup_id and matchup['roster_id'] != team.id:
            return matchup['roster_id']


def get_score(team, score: float, week: int, curr_matchups_played: int) -> float or None:
    '''Get score for a matchup'''

    if week > curr_matchups_played:
        return None

    team.scores.append(score)
    return score


def get_opponents(team, league) -> None:
    '''Get opponents for a team'''

    team.opponents = [
        league.get_team(matchup['opponent'])
        for matchup in team.matchups
    ]


def get_average_score(team, curr_matchups_played: int) -> float:
    '''Get average score for a team'''

    total_score = 0
    for matchup in team.matchups[:curr_matchups_played]:
        total_score += matchup['score']
    return round(total_score / curr_matchups_played, 2)


def is_win(team, matchup_id: int, matchups: list, week: int, curr_matchups_played: int) -> str:
    '''Returns if a team won a matchup'''

    for matchup in matchups:
        if week > curr_matchups_played:
            return 'Unknown'
        if matchup['matchup_id'] == matchup_id:
            if matchup['roster_id'] == team.id:
                points_for = matchup['points']
            else:
                points_against = matchup['points'] 

    if points_for > points_against:
        return 'Yes'
    else:
        return 'No'


# I slightly increase standard deviation to reduce the confidence of the predictions
# Fantasy scores aren't really random variables,
# so I figured I should make the predictions slightly less confident
# Adj std dev = std dev * (n+1)/n, where n is the number of games played


def get_adj_std_dev(team, curr_matchups_played: int) -> float:
    '''Get adjusted standard deviation of score for a team'''

    adj_std_dev = (std_dev(team.scores)
                   * (curr_matchups_played + 1)
                   / curr_matchups_played)
    return round(adj_std_dev, 2)
