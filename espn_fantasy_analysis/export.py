import pandas as pd
import re

def export_league(league):
    '''Export league data to csv'''
    league_dict = {}
    # Create all the columns in the table
    league_dict['Expected Standings'] = list(range(1,league.num_teams+1))
    league_dict['Team Name'] = [team.name for team in league.teams]
    league_dict['Expected Wins'] = [round(sum(team.win_likelihoods[:league.curr_matchups_played]), 2) for team in league.teams]
    league_dict['Expected Losses'] = [round(league.curr_matchups_played - sum(team.win_likelihoods[:league.curr_matchups_played]), 2) for team in league.teams]
    league_dict['Actual Wins'] = [team.wins for team in league.teams]
    league_dict['Differential'] = [round(team.wins - sum(team.win_likelihoods[:league.curr_matchups_played]), 2) for team in league.teams]
    league_dict['Projected Wins'] = [round(team.wins + sum(team.win_likelihoods[league.curr_matchups_played:]), 2) for team in league.teams]
    league_dict['Projected Losses'] = [round(league.total_matchups - team.wins - sum(team.win_likelihoods[league.curr_matchups_played:]), 2) for team in league.teams]
    league_dict['Average Score'] = [team.average_score for team in league.teams]
    df = pd.DataFrame(league_dict)
    df.to_csv('csv/league.csv', index=False)#, quoting=QUOTE_NONE)
    df.to_html('index.html', index=False)
    #df.to_html('index.html', index=False)

def export_team(team):
    '''Export team data to csvs'''
    export_matchup_stats(team)
    export_win_total_probs(team)

def export_matchup_stats(team):
    '''Export matchup stats to csv'''
    team_dict = {}
    total_matchups = len(team.win_likelihoods)
    # Create all the columns in the table
    team_dict['Week'] = list(range(1,total_matchups+1))
    team_dict['Points For'] = pad_list(team.scores, total_matchups)
    team_dict['Opponent'] = [opponent.name for opponent in team.opponents]
    team_dict['Opponent Average Score'] = team.opponent_average_scores
    team_dict['Opponent Adjusted Standard Deviations'] = team.opponent_std_devs
    team_dict['Expected Win Percentage'] = [round(prob*100, 2) for prob in team.win_likelihoods]
    df = pd.DataFrame(team_dict)
    name = re.sub(r'[^\w\s]', '', team.name)
    df.to_csv('csv/{}_matchup_data.csv'.format(name.replace(' ', '_')), index=False)

def export_win_total_probs(team):
    '''Export win total probabilities to csv'''
    team_dict = {}
    total_matchups = len(team.win_likelihoods)
    # Create all the columns in the table
    team_dict['Amount of wins'] = list(range(total_matchups+1))
    team_dict['Percent chance of currently having this many wins'] = pad_list([round(prob*100, 2) for prob in team.win_total_probs], total_matchups+1)
    team_dict['Percent chance of ending with this many wins'] = [round(prob*100, 2) for prob in team.future_win_total_probs]
    df = pd.DataFrame(team_dict)
    name = re.sub(r'[^\w\s]', '', team.name)
    df.to_csv('csv/{}_win_total_probabilities.csv'.format(name.replace(' ', '_')), index=False)

def pad_list(_list, length):
    return _list + [''] * (length - len(_list))