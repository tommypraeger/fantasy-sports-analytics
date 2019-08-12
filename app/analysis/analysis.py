import math
from functools import reduce

import numpy as np
from scipy.stats import norm

from poibin import PoiBin


def get_win_likelihoods(league, team):
    '''Gets win likelihoods for a team'''

    for matchup in team.matchups:
        # Separate win likelihood calculations into past and future
        if matchup['week'] <= league.curr_matchups_played:
            win_likelihood = past_win_likelihood(matchup,
                                                 league,
                                                 team)
        else:
            win_likelihood = future_win_likelihood(matchup,
                                                   league,
                                                   team.average_score,
                                                   team.score_std_dev,
                                                   team)

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

    return round(win_likelihood(score,
                                opponent_average_score,
                                opponent_std_dev),
                 4)


def future_win_likelihood(matchup, league, average_score, std_dev, team):
    '''Win likelihood of a future matchup'''

    opponent = league.get_team(matchup['opponent'])
    opponent_average_score = opponent.average_score
    team.opponent_average_scores.append(opponent_average_score)

    opponent_std_dev = opponent.score_std_dev
    team.opponent_std_devs.append(opponent_std_dev)

    combined_std_dev = math.sqrt(std_dev**2 + opponent_std_dev**2)

    return round(win_likelihood(average_score,
                                opponent_average_score,
                                combined_std_dev),
                 4)


def std_dev(arr):
    '''Standard deviation of an array of numbers'''

    return np.std(arr, ddof=1)


def win_likelihood(first, second, std_dev):
    '''Returns win likelihood given 2 scores and a standard deviation

    Implemented as determining the probability that the difference
    between the two scores is greater than 0.
    '''

    return norm.cdf(first - second, 0, std_dev)


def get_win_total_probs(league, team):
    '''Gets probabilities of having each possible amount of wins'''

    # Create Poisson binomial distribution using past expected win likelihoods
    pb = PoiBin(team.win_likelihoods[:league.curr_matchups_played])

    # Find probability of having every amount of wins from 0 to matchups played
    for win_amount in range(league.curr_matchups_played+1):
        team.win_total_probs.append(round(pb.pmf(win_amount), 4))


def get_future_win_total_probs(league, team):
    '''Gets probabilities of ending with each possible amount of wins'''

    # Create Poisson binomial distribution using future expected win likelihoods
    pb = PoiBin(team.win_likelihoods[league.curr_matchups_played:])

    # Impossible to end with fewer wins than what you have currently
    for win_amount in range(team.wins):
        team.future_win_total_probs.append(0)

    # Find probability of having every amount of wins from current wins to max wins
    losses = league.curr_matchups_played - team.wins
    max_wins = league.total_matchups - losses
    for win_amount in range(team.wins, max_wins+1):
        team.future_win_total_probs.append(round(pb.pmf(win_amount - team.wins), 4))

    # Impossible to end with more wins than current wins + matchups remaining
    for win_amount in range(max_wins+1, league.total_matchups+1):
        team.future_win_total_probs.append(0)
