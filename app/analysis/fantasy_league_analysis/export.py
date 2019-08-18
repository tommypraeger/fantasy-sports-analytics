from app.analysis.fantasy_league_analysis.league import League
from app.analysis.fantasy_league_analysis.team import Team


def past_expected_wins(team, league) -> float:
    '''Sum of expected wins for past matchups'''

    return sum(team.win_likelihoods[:league.curr_matchups_played])


def future_expected_wins(team, league) -> float:
    '''Sum of expected wins for future matchups'''

    return sum(team.win_likelihoods[league.curr_matchups_played:])


def export_league(league) -> dict:
    '''Export league object'''

    league_dict = {
        'name': league.name,
        'table': {}
    }

    # All table columns

    # List from 1 to num teams
    league_dict['table']['Expected Standings'] = list(range(1, league.num_teams + 1))

    # Team names from list - sorted by win expectancy
    league_dict['table']['Team Name'] = [
        team.name
        for team in league.teams
    ]

    # Sum of expected wins for each team
    league_dict['table']['Expected Wins'] = [
        round(past_expected_wins(team, league), 2)
        for team in league.teams
    ]

    # Total matchups - expected wins
    league_dict['table']['Expected Losses'] = [
        round(league.curr_matchups_played - past_expected_wins(team, league), 2)
        for team in league.teams
    ]

    # Actual number of wins
    league_dict['table']['Actual Wins'] = [
        team.wins
        for team in league.teams
    ]

    # Actual wins - expected wins
    league_dict['table']['Differential'] = [
        round(team.wins - past_expected_wins(team, league), 2)
        for team in league.teams
    ]

    # Current wins + future expected wins
    league_dict['table']['Projected Wins'] = [
        round(team.wins + future_expected_wins(team, league), 2)
        for team in league.teams
    ]

    # Total matchups - current wins - future expected wins
    league_dict['table']['Projected Losses'] = [
        round(league.total_matchups - team.wins - future_expected_wins(team, league), 2)
        for team in league.teams
    ]

    # Average weekly score
    league_dict['table']['Average Score'] = [
        team.average_score
        for team in league.teams
    ]

    return league_dict


def export_team(team, league) -> dict:
    '''Export team object'''

    team_dict = {
        'name': team.name,
        'table': {}
    }

    export_matchup_stats(team, team_dict)
    export_win_total_probs(team, team_dict)

    return team_dict


def export_matchup_stats(team, team_dict: dict) -> None:
    '''Export team matchup stats'''

    total_matchups = len(team.win_likelihoods)

    # All the columns in matchup table

    # List from 1 to num total matchups
    team_dict['table']['Week'] = list(range(1, total_matchups + 1))

    # Points for in each week
    team_dict['table']['Points For'] = team.scores

    # Opponent for each week
    team_dict['table']['Opponent'] = [
        opponent.name
        for opponent in team.opponents
    ]

    # Opponent's average score for each week
    team_dict['table']['Opponent Average Score'] = team.opponent_average_scores

    # Opponent's adjusted std dev for each week
    team_dict['table']['Opponent Adjusted Standard Deviations'] = team.opponent_std_devs

    # Expected win percentage for each week
    team_dict['table']['Expected Win Percentage'] = [
        round(prob * 100, 2)
        for prob in team.win_likelihoods
    ]


def export_win_total_probs(team, team_dict: dict) -> None:
    '''Export win total probabilities to csv'''

    total_matchups = len(team.win_likelihoods)

    # All the columns in win total table

    # List from 0 to num total matchups
    team_dict['table']['Amount of wins'] = list(range(total_matchups + 1))

    # Percent chance to have currently have a certain number of wins
    team_dict['table']['Percent chance of currently having this many wins'] = [
        round(prob * 100, 2)
        for prob in team.win_total_probs
    ]

    # Percent chance to end with a certain number of wins
    team_dict['table']['Percent chance of ending with this many wins'] = [
        round(prob * 100, 2)
        for prob in team.future_win_total_probs
    ]
