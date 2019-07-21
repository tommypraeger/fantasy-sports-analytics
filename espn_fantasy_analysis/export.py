import pandas as pd
import re

def exportLeague(league):
    '''Export league data to csv'''
    leagueDict = {}
    # Create all the columns in the table
    leagueDict['Expected Standings'] = list(range(1,league.numTeams+1))
    leagueDict['Team Name'] = [team.name for team in league.teams]
    leagueDict['Expected Wins'] = [round(sum(team.winLikelihoods[:league.currMatchupsPlayed]), 2) for team in league.teams]
    leagueDict['Expected Losses'] = [round(league.currMatchupsPlayed - sum(team.winLikelihoods[:league.currMatchupsPlayed]), 2) for team in league.teams]
    leagueDict['Actual Wins'] = [team.wins for team in league.teams]
    leagueDict['Differential'] = [round(sum(team.winLikelihoods[:league.currMatchupsPlayed]) - team.wins, 2) for team in league.teams]
    leagueDict['Projected Wins'] = [round(team.wins + sum(team.winLikelihoods[league.currMatchupsPlayed:]), 2) for team in league.teams]
    leagueDict['Projected Losses'] = [round(league.totalMatchups - team.wins - sum(team.winLikelihoods[league.currMatchupsPlayed:]), 2) for team in league.teams]
    leagueDict['Average Score'] = [team.averageScore for team in league.teams]
    df = pd.DataFrame(leagueDict)
    df.to_csv('csv/league.csv', index=False)#, quoting=QUOTE_NONE)

def exportTeam(team):
    '''Export team data to csvs'''
    exportMatchupStats(team)
    exportWinTotalProbs(team)

def exportMatchupStats(team):
    '''Export matchup stats to csv'''
    teamDict = {}
    totalMatchups = len(team.winLikelihoods)
    # Create all the columns in the table
    teamDict['Week'] = list(range(1,totalMatchups+1))
    teamDict['Points For'] = padList(team.scores, totalMatchups)
    teamDict['Opponent'] = [opponent.name for opponent in team.opponents]
    teamDict['Opponent Average Score'] = team.opponentAverageScores
    teamDict['Opponent Adjusted Standard Deviations'] = team.opponentStdDevs
    teamDict['Expected Win Percentage'] = [round(prob*100, 2) for prob in team.winLikelihoods]
    df = pd.DataFrame(teamDict)
    name = re.sub(r'[^\w\s]', '', team.name)
    df.to_csv('csv/{}_matchup_data.csv'.format(name.replace(' ', '_')), index=False)

def exportWinTotalProbs(team):
    '''Export win total probabilities to csv'''
    teamDict = {}
    totalMatchups = len(team.winLikelihoods)
    # Create all the columns in the table
    teamDict['Amount of wins'] = list(range(totalMatchups+1))
    teamDict['Percent chance of currently having this many wins'] = padList([round(prob*100, 2) for prob in team.winTotalProbs], totalMatchups+1)
    teamDict['Percent chance of ending with this many wins'] = [round(prob*100, 2) for prob in team.futureWinTotalProbs]
    df = pd.DataFrame(teamDict)
    name = re.sub(r'[^\w\s]', '', team.name)
    df.to_csv('csv/{}_win_total_probabilities.csv'.format(name.replace(' ', '_')), index=False)

def padList(_list, length):
    return _list + [''] * (length - len(_list))