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
        'standings_table': {}
    }

    # All table columns
    for rank, team in enumerate(league.teams, 1):
        league_dict['standings_table'][team.name] = {
            'expected_rank': rank,
            'name': team.name,
            'expected_wins': round(past_expected_wins(team, league), 2),
            'expected_losses': (
                round(league.curr_matchups_played - past_expected_wins(team, league), 2),
            ),
            'actual_wins': team.wins,
            'differential': round(team.wins - past_expected_wins(team, league), 2),
            'projected_wins': round(team.wins + future_expected_wins(team, league), 2),
            'projected losses': (
                round(league.total_matchups - team.wins - future_expected_wins(team, league), 2)
            ),
            'average_score': team.average_score
        }

    return league_dict


def export_team(team) -> dict:
    '''Export team object'''

    team_dict = {
        'name': team.name,
        'matchup_table': {},
        'win_total_probs_table': {}
    }

    export_matchup_stats(team, team_dict)
    export_win_total_probs(team, team_dict)

    return team_dict


def export_matchup_stats(team, team_dict: dict) -> None:
    '''Export team matchup stats'''

    total_matchups = len(team.win_likelihoods)
    curr_matchups_played = len(team.scores)

    # All the columns in matchup table
    for week in range(total_matchups):
        team_dict['matchup_table'][week + 1] = {
            'week': week + 1,
            'points_for': team.scores[week] if week < curr_matchups_played else None,
            'opponent': team.opponents[week].name,
            'opponent_average_score': team.opponent_average_scores[week],
            'opponent_adj_std_dev': team.opponent_std_devs[week],
            'expected_win_pct': round(team.win_likelihoods[week] * 100, 2)
        }


def export_win_total_probs(team, team_dict: dict) -> None:
    '''Export win total probabilities to csv'''

    total_matchups = len(team.win_likelihoods)
    curr_matchups_played = len(team.win_total_probs)

    # All the columns in win total probabilities table
    for num_wins in range(total_matchups + 1):
        team_dict['win_total_probs_table'][num_wins] = {
            'num_wins': num_wins,
            'curr_chance': (
                round(team.win_total_probs[num_wins] * 100, 2)
                if num_wins < curr_matchups_played else 0
            ),
            'end_chance': round(team.future_win_total_probs[num_wins] * 100, 2)
        }
