from scipy.stats import norm
import numpy as np
import math
from functools import reduce
from poibin import PoiBin

def get_win_likelihoods(league, team):
    '''Gets win likelihoods for a team'''
    for matchup in team.matchups:
        if matchup['week'] <= league.curr_matchups_played:
            win_likelihood = past_win_likelihood(matchup, league, team)
        else:
            win_likelihood = future_win_likelihood(matchup, league, team.average_score, team.score_std_dev, team)
        team.win_likelihoods.append(win_likelihood)
        matchup['win_likelihood'] = win_likelihood

def past_win_likelihood(matchup, league, team):
    '''Win likelihood of a past matchup'''
    score = matchup['score']
    opponent = league.get_team(matchup['opponent'])
    opponent_average_score = opponent.average_score
    team.opponent_average_scores.append(opponent_average_score)
    opponent_std_dev = opponent.score_std_dev
    team.opponent_std_devs.append(opponent_std_dev)
    return round(win_likelihood(score, opponent_average_score, opponent_std_dev), 4)

def future_win_likelihood(matchup, league, average_score, std_dev, team):
    '''Win likelihood of a future matchup'''
    opponent = league.get_team(matchup['opponent'])
    opponent_average_score = opponent.average_score
    team.opponent_average_scores.append(opponent_average_score)
    opponent_std_dev = opponent.score_std_dev
    team.opponent_std_devs.append(opponent_std_dev)
    combined_std_dev = math.sqrt(std_dev**2 + opponent_std_dev**2)
    return round(win_likelihood(average_score, opponent_average_score, combined_std_dev), 4)

def std_dev(arr):
    '''Standard deviation of an array of numbers'''
    return np.std(arr, ddof=1)

def win_likelihood(first, second, std_dev):
    '''Probalilty that a value will be above 0 given a mean and standard deviation'''
    return norm.cdf(first - second, 0, std_dev)

def get_win_total_probs(league, team):
    '''Gets probabilities of having each possible amount of wins'''
    pb = PoiBin(team.win_likelihoods[:league.curr_matchups_played])
    for win_amount in range(league.curr_matchups_played+1):
        team.win_total_probs.append(round(pb.pmf(win_amount), 4))

def get_future_win_total_probs(league, team):
    '''Gets probabilities of ending with each possible amount of wins'''
    pb = PoiBin(team.win_likelihoods[league.curr_matchups_played:])
    for win_amount in range(team.wins):
        team.future_win_total_probs.append(0)
    losses = league.curr_matchups_played - team.wins
    max_wins = league.total_matchups - losses
    for win_amount in range(team.wins, max_wins+1):
        team.future_win_total_probs.append(round(pb.pmf(win_amount - team.wins), 4))
    for win_amount in range(max_wins+1, league.total_matchups+1):
        team.future_win_total_probs.append(0)