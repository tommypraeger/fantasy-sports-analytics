from scipy.stats import norm
import numpy as np
import math
from functools import reduce
from poibin import PoiBin

def getWinLikelihoods(league, team):
    '''Gets win likelihoods for a team'''
    for matchup in team.matchups:
        if matchup['week'] <= league.currMatchupsPlayed:
            winLikelihood = pastWinLikelihood(matchup, league)
        else:
            winLikelihood = futureWinLikelihood(matchup, league, team.averageScore, team.scoreStdDev)
        team.winLikelihoods.append(winLikelihood)
        matchup['winLikelihood'] = winLikelihood

def pastWinLikelihood(matchup, league):
    '''Win likelihood of a past matchup'''
    score = matchup['score']
    opponent = league.getTeam(matchup['opponent'])
    opponentAverageScore = opponent.averageScore
    opponentStdDev = opponent.scoreStdDev
    return round(winLikelihood(score, opponentAverageScore, opponentStdDev), 4)

def futureWinLikelihood(matchup, league, averageScore, stdDev):
    '''Win likelihood of a future matchup'''
    opponent = league.getTeam(matchup['opponent'])
    opponentAverageScore = opponent.averageScore
    opponentStdDev = opponent.scoreStdDev
    combinedStdDev = math.sqrt(stdDev**2 + opponentStdDev**2)
    return round(winLikelihood(averageScore, opponentAverageScore, combinedStdDev), 4)

def stdDev(arr):
    '''Standard deviation of an array of numbers'''
    return np.std(arr, ddof=1)

def winLikelihood(first, second, stdDev):
    '''Probalilty that a value will be above 0 given a mean and standard deviation'''
    return norm.cdf(first - second, 0, stdDev)

# This is based on the recursive formula given here: https://en.wikipedia.org/wiki/Poisson_binomial_distribution
def getWinTotalProbs(league, team):
    '''Gets probabilities of having each possible amount of wins'''
    pb = PoiBin(team.winLikelihoods[:league.currMatchupsPlayed])
    for winAmount in range(league.currMatchupsPlayed):
        team.winTotalProbs.append(round(pb.pmf(winAmount), 4))