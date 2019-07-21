from scipy.stats import norm
import numpy as np
import math
from functools import reduce
from poibin import PoiBin

def getWinLikelihoods(league, team):
    '''Gets win likelihoods for a team'''
    for matchup in team.matchups:
        if matchup['week'] <= league.currMatchupsPlayed:
            winLikelihood = pastWinLikelihood(matchup, league, team)
        else:
            winLikelihood = futureWinLikelihood(matchup, league, team.averageScore, team.scoreStdDev, team)
        team.winLikelihoods.append(winLikelihood)
        matchup['winLikelihood'] = winLikelihood

def pastWinLikelihood(matchup, league, team):
    '''Win likelihood of a past matchup'''
    score = matchup['score']
    opponent = league.getTeam(matchup['opponent'])
    opponentAverageScore = opponent.averageScore
    team.opponentAverageScores.append(opponentAverageScore)
    opponentStdDev = opponent.scoreStdDev
    team.opponentStdDevs.append(opponentStdDev)
    return round(winLikelihood(score, opponentAverageScore, opponentStdDev), 4)

def futureWinLikelihood(matchup, league, averageScore, stdDev, team):
    '''Win likelihood of a future matchup'''
    opponent = league.getTeam(matchup['opponent'])
    opponentAverageScore = opponent.averageScore
    team.opponentAverageScores.append(opponentAverageScore)
    opponentStdDev = opponent.scoreStdDev
    team.opponentStdDevs.append(opponentStdDev)
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
    for winAmount in range(league.currMatchupsPlayed+1):
        team.winTotalProbs.append(round(pb.pmf(winAmount), 4))

def getFutureWinTotalProbs(league, team):
    '''Gets probabilities of ending with each possible amount of wins'''
    pb = PoiBin(team.winLikelihoods[league.currMatchupsPlayed:])
    for winAmount in range(team.wins):
        team.futureWinTotalProbs.append(0)
    losses = league.currMatchupsPlayed - team.wins
    maxWins = league.totalMatchups - losses
    for winAmount in range(team.wins, maxWins+1):
        team.futureWinTotalProbs.append(round(pb.pmf(winAmount - team.wins), 4))
    for winAmount in range(maxWins+1, league.totalMatchups+1):
        team.futureWinTotalProbs.append(0)