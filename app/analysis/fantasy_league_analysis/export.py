from app.analysis.fantasy_league_analysis.league import League
from app.analysis.fantasy_league_analysis.team import Team


def is_win(team: Team, matchup) -> str:
    """Determine if a team won a given matchup"""
    if matchup.home_team_id == team.id:
        if matchup.home_score > matchup.away_score:
            return "Yes"
        elif matchup.home_score < matchup.away_score:
            return "No"
        else:
            return "Tie"
    else:
        if matchup.away_score > matchup.home_score:
            return "Yes"
        elif matchup.away_score < matchup.home_score:
            return "No"
        else:
            return "Tie"


def past_expected_wins(team, league) -> float:
    """Sum of expected wins for past matchups"""

    return sum(team.win_likelihoods[: league.curr_matchups_played])


def future_expected_wins(team, league) -> float:
    """Sum of expected wins for future matchups"""

    return sum(team.win_likelihoods[league.curr_matchups_played :])


def export_league(league) -> dict:
    """Export league object"""

    league_dict = {"name": league.name, "standings_table": []}

    # All table columns
    for rank, team in enumerate(league.teams, 1):
        league_dict["standings_table"].append(
            {
                "Expected Ranking": rank,
                "Name": team.name,
                "Expected Wins": round(past_expected_wins(team, league), 2),
                "Expected Losses": (
                    round(
                        league.curr_matchups_played - past_expected_wins(team, league),
                        2,
                    )
                ),
                "Actual Wins": team.wins,
                "Win Differential": round(
                    team.wins - past_expected_wins(team, league), 2
                ),
                "Projected Wins": round(
                    team.wins + future_expected_wins(team, league), 2
                ),
                "Projected Losses": (
                    round(
                        league.total_matchups
                        - team.wins
                        - future_expected_wins(team, league),
                        2,
                    )
                ),
                "Average Score": round(team.average_score, 2),
            }
        )

    return league_dict


def export_team(team, league) -> dict:
    """Export team object"""

    team_dict = {"name": team.name, "matchup_table": [], "win_total_probs": {}}

    export_matchup_stats(team, team_dict, league)
    export_win_total_probs(team, team_dict)

    return team_dict


def export_matchup_stats(team, team_dict: dict, league: League) -> None:
    """Export team matchup stats"""

    total_matchups = len(team.win_likelihoods)
    curr_matchups_played = len(team.scores)

    # All the columns in matchup table
    for week in range(total_matchups):
        opponent_id = team.opponents[week]
        opponent = league.team_map[opponent_id]
        matchup = team.matchups[week]
        
        # Calculate actual win status only for past matchups
        actual_win = is_win(team, matchup) if week < curr_matchups_played else None

        team_dict["matchup_table"].append(
            {
                "Week": week + 1,
                "Points For": round(team.scores[week], 2)
                if week < curr_matchups_played
                else None,
                "Opponent": opponent.name,
                "Opponent Average Score": round(team.opponent_average_scores[week], 2),
                "Opponent Adj. Std. Dev.": round(team.opponent_std_devs[week], 2),
                "Expected Win %": round(team.win_likelihoods[week] * 100, 2),
                "Actual Win?": actual_win,
            }
        )


def export_win_total_probs(team, team_dict: dict) -> None:
    """Export win total probabilities to csv"""

    # Win total probabilities data
    team_dict["win_total_probs"]["curr_wins"] = team.wins
    team_dict["win_total_probs"]["curr_probs"] = [
        round(team.win_total_probs[num_wins] * 100, 2)
        for num_wins in range(len(team.win_total_probs))
    ]
    team_dict["win_total_probs"]["end_probs"] = [
        round(team.future_win_total_probs[num_wins] * 100, 2)
        for num_wins in range(len(team.win_likelihoods) + 1)
    ]
