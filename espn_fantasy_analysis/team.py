from analysis import stdDev

class Team(object):
    def __init__(self, teamInfo):
        self.name = '{} {}'.format(teamInfo['location'].strip(), teamInfo['nickname'].strip())
        self.id = teamInfo['id']
        self.scores = []
        self.averageScore = 0
        self.scoreStdDev = 0
        self.matchups = []
        self.wins = teamInfo['record']['overall']['wins']
        self.opponents = []
        self.opponentAverageScores = []
        self.opponentStdDevs = []
        self.winLikelihoods = []
        self.winTotalProbs = []
        self.futureWinTotalProbs = []

        # This should be empty for football, but some fantasy baseball matchups are longer than 1 week and need to be scaled down
        # This dictionary should map from week number to multiplier
        # e.g. Week 1 was 11 days instead of 7 so I added 1:7/11 to the the dictionary
        # Fill this in as needed
        self.scoreMultipliers = {
            1:7/11,
            14:7/10
        }

    def getMetadata(self, league):
        '''Calculate team-specific score data'''
        self.getMatchups(league)
        self.averageScore = self.getAverageScore(league.currMatchupsPlayed)
        self.scoreStdDev = self.getAdjStdDev(league.currMatchupsPlayed)

    def getMatchups(self, league):
        '''Get matchups for a team'''
        for matchupJson in league.schedule:
            # Only get regular season matchups
            if matchupJson['matchupPeriodId'] > league.currMatchupsPlayed:
                break
            if matchupJson['away']['teamId'] == self.id or matchupJson['home']['teamId'] == self.id:
                matchup = {}
                matchup['week'] = matchupJson['matchupPeriodId']
                matchup['score'] = self.getScore(matchupJson, league.currMatchupsPlayed)
                matchup['opponent'] = self.getOpponent(matchupJson)
                self.matchups.append(matchup)

    def getScore(self, matchup, currMatchupsPlayed):
        '''Get score for a matchup'''
        if matchup['matchupPeriodId'] > currMatchupsPlayed:
            return None
        # First check if there is a score multiplier
        if matchup['away']['teamId'] == self.id:
            try:
                score = round(self.scoreMultipliers[matchup['matchupPeriodId']]*matchup['away']['totalPoints'], 2)
                self.scores.append(score)
                return score
            except KeyError:
                score = round(matchup['away']['totalPoints'], 2)
                self.scores.append(score)
                return score
        elif matchup['home']['teamId'] == self.id:
            try:
                score = round(self.scoreMultipliers[matchup['matchupPeriodId']]*matchup['home']['totalPoints'], 2)
                self.scores.append(score)
                return score
            except KeyError:
                score = round(matchup['home']['totalPoints'], 2)
                self.scores.append(score)
                return score
        else:
            raise Exception('Failed sanity check. getMatchups returned a matchup team {} isn\'t in'.format(self.id))

    def getOpponent(self, matchup):
        '''Get opponent for a matchup'''
        if matchup['away']['teamId'] == self.id:
            return matchup['home']['teamId']
        elif matchup['home']['teamId'] == self.id:
            return matchup['away']['teamId']
        else:
            raise Exception('Failed sanity check. getMatchups returned a matchup team {} isn\'t in'.format(self.id))

    def getOpponents(self, league):
        '''Get opponents for a team'''
        self.opponents = [league.getTeam(matchup['opponent']) for matchup in self.matchups]

    def getAverageScore(self, currMatchupsPlayed):
        '''Get average score for a team'''
        totalScore = 0
        for matchup in self.matchups[:currMatchupsPlayed]:
            totalScore += matchup['score']
        return round(totalScore/currMatchupsPlayed, 2)

    # I slightly increase standard deviation to reduce the confidence of the predictions
    # Fantasy scores aren't really random variables so I figured I should make the predictions slightly less confident
    # Adj std dev = std dev * (n+1)/n, where n is the number of games played
    def getAdjStdDev(self, currMatchupsPlayed):
        '''Get adjusted standard deviation of score for a team'''
        return round(stdDev(self.scores)*(currMatchupsPlayed+1)/currMatchupsPlayed, 2)
