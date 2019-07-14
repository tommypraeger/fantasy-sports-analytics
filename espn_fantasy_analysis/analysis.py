import stats
import math

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
    return round(stats.winLikelihood(score, opponentAverageScore, opponentStdDev), 4)

def futureWinLikelihood(matchup, league, averageScore, stdDev):
    '''Win likelihood of a future matchup'''
    opponent = league.getTeam(matchup['opponent'])
    opponentAverageScore = opponent.averageScore
    opponentStdDev = opponent.scoreStdDev
    combinedStdDev = math.sqrt(stdDev**2 + opponentStdDev**2)
    return round(stats.winLikelihood(averageScore, opponentAverageScore, combinedStdDev), 4)

def getWinTotalProbs(league, team):
    '''Gets probabilities of having each possible amount of wins'''
    pass