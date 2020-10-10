import requests

from app.analysis.fantasy_league_analysis.analysis import (
    std_dev,
    get_win_likelihoods,
    get_win_total_probs,
    get_future_win_total_probs
)
from app.analysis.fantasy_league_analysis.team import Team

sport_map = {
    'football': 'ffl',
    'baseball': 'flb'
}


def fetch_league(league, league_info) -> None:
    '''Load league and set metadata for league and teams'''

    league.sport = league_info['sport']
    league.id = league_info['leagueId']
    league.year = league_info['year']
    league.espn_s2 = league_info['espnS2']

    if league.sport not in sport_map:
        raise Exception(f'{league.sport} is not a valid sport for ESPN.')

    # Necessary ESPN API URLs
    url = (f'https://fantasy.espn.com/apis/v3/games/{sport_map[league.sport]}'
           f'/seasons/{league.year}/segments/0/leagues/{league.id}'
           '?view=mMatchupScore&view=mStatus&view=mSettings&view=mTeam&view=modular&view=mNav')
    matchup_url = (f'https://fantasy.espn.com/apis/v3/games/{sport_map[league.sport]}'
                   f'/seasons/{league.year}/segments/0/leagues/{league.id}?view=mMatchup')

    # Cookies needed for authentication
    cookies = {
        'espn_s2': league.espn_s2
    }

    # Make request and check if it succeeds
    resp = requests.get(url, cookies=cookies)
    matchup_resp = requests.get(matchup_url, cookies=cookies)
    if resp.status_code == 401 or matchup_resp.status_code == 401:
        raise Exception('The request to access your league was unauthorized. '
                        'Make you provide the espn_s2 cookie if your league is private.')
    if resp.status_code >= 400 or matchup_resp.status_code >= 400:
        raise Exception('Something went wrong fetching your league. '
                        'Make sure the league ID, year, and sport are correct.')

    resp_json = resp.json()
    matchup_json = matchup_resp.json()

    league.name = resp_json['settings']['name']
    league.schedule = resp_json['schedule']
    league.total_matchups = resp_json['settings']['scheduleSettings']['matchupPeriodCount']
    league.curr_matchups_played = get_curr_matchups_played(
        league,
        resp_json['status']['currentMatchupPeriod']
    )
    get_score_multipliers(league, matchup_json)

    # Can't do analysis with less than 2 games played
    if league.curr_matchups_played < 2:
        raise Exception('There must have been at least 2 matchups played already.')

    teams = resp_json['teams']
    league.num_teams = len(teams)

    for team_info in teams:
        team_obj = Team()
        get_team_metadata(team_obj, team_info, league)
        league.teams.append(team_obj)
        league.team_map[team_info['id']] = team_obj

    # Need other team data to be complete before this can be done
    for team in league.teams:
        get_opponents(team, league)


def get_score_multipliers(league, matchup_json: dict) -> None:
    '''Get score adjustments for matchups that are longer than usual'''

    # All football leagues have consistent scoring periods
    if league.sport == 'football':
        for week in range(1, league.curr_matchups_played + 1):
            league.score_multipliers[week] = 1

    # Mapping of how many scoring periods (active days in fantasy baseball) are in each matchup
    scoring_period_count = {}
    for matchup in matchup_json['schedule']:
        if matchup['matchupPeriodId'] > league.curr_matchups_played:
            # Can't check future matchups
            break
        if matchup['matchupPeriodId'] in scoring_period_count:
            continue
        scoring_period_count[matchup['matchupPeriodId']] = (
            len(matchup['away']['pointsByScoringPeriod'])
        )

    # Find most frequent number of scoring periods in a matchup
    if len(scoring_period_count.values()) == 0:
        raise Exception(f'It looks like the league didn\'t take place in {league.year}. '
                        'Make sure the league ID, year, and sport are correct.')
    usual_scoring_period_count = max(set(scoring_period_count.values()),
                                     key=list(scoring_period_count.values()).count)

    # Multiplier determined how to change a score to normalize it with the average
    # e.g. an 11-day matchup when average is 7 days would have its score multiplied by 7/11
    # Matchups of regular length have multipliers of one
    for matchup_period in scoring_period_count:
        league.score_multipliers[matchup_period] = (
            usual_scoring_period_count /
            scoring_period_count[matchup_period]
        )


def perform_team_analysis(league) -> None:
    '''Perform all the statistics and analysis for each team'''

    for team in league.teams:
        analyze_team(league, team)


def analyze_team(league, team) -> None:
    '''Calculate win expectancies'''

    get_win_likelihoods(league, team)
    get_win_total_probs(league, team)
    get_future_win_total_probs(league, team)


def get_curr_matchups_played(league, curr_matchup_period: int) -> int:
    '''Get current number of matchups played'''

    if curr_matchup_period > league.total_matchups:
        return league.total_matchups
    return curr_matchup_period - 1


def get_team_metadata(team, team_info, league) -> None:
    '''Calculate team-specific score data'''

    team.name = f'{team_info["location"].strip()} {team_info["nickname"].strip()}'
    team.wins = team_info['record']['overall']['wins']
    team.id = team_info['id']
    get_matchups(team, league)
    team.average_score = get_average_score(team, league.curr_matchups_played)
    team.score_std_dev = get_adj_std_dev(team, league.curr_matchups_played)


def get_matchups(team, league) -> None:
    '''Get matchups for a team'''

    for matchup_json in league.schedule:
        # Only get regular season matchups
        if matchup_json['matchupPeriodId'] > league.total_matchups:
            break
        if (matchup_json['away']['teamId'] == team.id
                or matchup_json['home']['teamId'] == team.id):
            matchup = {}
            matchup['week'] = matchup_json['matchupPeriodId']
            matchup['score'] = get_score(team,
                                         matchup_json,
                                         league.curr_matchups_played,
                                         league.score_multipliers)
            matchup['opponent'] = get_opponent(team, matchup_json)
            matchup['won'] = is_win(team, matchup_json, league.curr_matchups_played)
            team.matchups.append(matchup)


def get_score(team,
              matchup: dict,
              curr_matchups_played: int,
              score_multipliers: dict) -> float or None:
    '''Get score for a matchup'''

    # No score for future games
    if matchup['matchupPeriodId'] > curr_matchups_played:
        return None

    # Check if team is home or away
    if matchup['away']['teamId'] == team.id:
        score = (score_multipliers[matchup['matchupPeriodId']]
                 * matchup['away']['totalPoints'])
    elif matchup['home']['teamId'] == team.id:
        score = (score_multipliers[matchup['matchupPeriodId']]
                 * matchup['home']['totalPoints'])
    else:
        raise Exception('Failed sanity check. '
                        f'getMatchups returned a matchup team {team.id} isn\'t in')

    score = round(score, 2)
    team.scores.append(score)
    return score


def get_opponent(team, matchup: dict) -> str:
    '''Get opponent for a matchup'''

    if matchup['away']['teamId'] == team.id:
        return matchup['home']['teamId']
    elif matchup['home']['teamId'] == team.id:
        return matchup['away']['teamId']
    else:
        raise Exception('Failed sanity check. '
                        f'getMatchups returned a matchup team {team.id} isn\'t in')


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


def is_win(team, matchup: dict, curr_matchups_played: int) -> str:
    '''Returns if a team won a matchup'''

    # No winner for future games
    if matchup['matchupPeriodId'] > curr_matchups_played:
        return 'Unknown'

    # Check if team is home or away
    if matchup['away']['teamId'] == team.id:
        if matchup['winner'] == 'AWAY':
            return 'Yes'
    elif matchup['home']['teamId'] == team.id:
        if matchup['winner'] == 'HOME':
            return 'Yes'
    else:
        raise Exception('Failed sanity check. '
                        f'getMatchups returned a matchup team {team.id} isn\'t in')

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
