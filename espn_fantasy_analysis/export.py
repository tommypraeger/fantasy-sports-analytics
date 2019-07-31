import re

import pandas as pd


def export_league(league):
    '''Export league data to html index'''
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
    
    # Write html file
    df = pd.DataFrame(league_dict)
    league_table = df.to_html(classes="league-table", index=False)
    index = open('docs/index.html', 'w')
    begin_html(index, league.name)
    nav_bar(index, league.teams)
    index.write('<p class="page-title">{} Analysis</p>'.format(league.name))
    index.write(league_table)
    end_html(index)
    index.close()

def export_team(team, league):
    '''Export team data to html files'''
    file_name = 'docs/' + name_file(team.name)
    page_title = team.name
    team_page = open(file_name, 'w')
    begin_html(team_page, page_title)
    nav_bar(team_page, league.teams)
    team_page.write('<p class="page-title">{} Analysis</p>'.format(team.name))
    export_matchup_stats(team, team_page)
    export_win_total_probs(team, team_page)
    end_html(team_page)

def export_matchup_stats(team, file_):
    '''Export matchup stats to html files'''
    team_dict = {}
    total_matchups = len(team.win_likelihoods)
    # Create all the columns in the table
    team_dict['Week'] = list(range(1,total_matchups+1))
    team_dict['Points For'] = pad_list(team.scores, total_matchups)
    team_dict['Opponent'] = [opponent.name for opponent in team.opponents]
    team_dict['Opponent Average Score'] = team.opponent_average_scores
    team_dict['Opponent Adjusted Standard Deviations'] = team.opponent_std_devs
    team_dict['Expected Win Percentage'] = [round(prob*100, 2) for prob in team.win_likelihoods]
    
    # Write html file
    df = pd.DataFrame(team_dict)
    matchup_table = df.to_html(classes="team-table", index=False)
    file_.write(matchup_table)

def export_win_total_probs(team, file_):
    '''Export win total probabilities to csv'''
    team_dict = {}
    total_matchups = len(team.win_likelihoods)
    # Create all the columns in the table
    team_dict['Amount of wins'] = list(range(total_matchups+1))
    team_dict['Percent chance of currently having this many wins'] = pad_list([round(prob*100, 2) for prob in team.win_total_probs], total_matchups+1)
    team_dict['Percent chance of ending with this many wins'] = [round(prob*100, 2) for prob in team.future_win_total_probs]
    
    # Write html file
    df = pd.DataFrame(team_dict)
    win_total_probs_table = df.to_html(index=False)
    file_.write(win_total_probs_table)

def name_file(name):
    return re.sub(r'[^\w\s]', '', name).replace(' ', '_') + '.html'

def pad_list(list_, length):
    '''Pads list with empty strings for table'''
    return list_ + [''] * (length - len(list_))

def begin_html(file_, title):
    '''Writes beginning of html file'''
    html_start = '''
    <html>
        <head>
            <title>{}</title>
            <link rel="stylesheet" href="index.css">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        </head>
    <body>
    '''.format(title)
    file_.write(html_start)

def end_html(file_):
    '''Writes end of html file'''
    html_end = '''
            <p class="credit">Created by <a href="https://tommypraeger.github.io" target="_blank">Tommy Praeger</a></p>
        </body>
    </html>'''
    file_.write(html_end)

def nav_bar(file_, teams):
    team_links = ['<a href="{}">{}</a>'.format(name_file(team.name), team.name) for team in sorted(teams, key=lambda team_: re.sub(r'[^\w\s]', '', team_.name))]
    nav_bar = '''
    <div class="navbar">
        <a href="/">Home</a>
        <div class="dropdown">
            <button class="dropbtn">Teams
                <i class="fa fa-caret-down"></i>
            </button>
            <div class="dropdown-content">
                {}
            </div>
        </div> 
    </div>
    '''.format('\n'.join(team_links))
    file_.write(nav_bar)