#import League

class Team(object):
    def __init__(self, teamInfo):
        self.name = '{} {}'.format(teamInfo['location'].strip(), teamInfo['nickname'].strip())
        self.id = teamInfo['id']
        self.scores = []
        self.averageScore = 0
        self.scoreStdDev = 0
        self.matchups = []
        self.opponents = []
        self.wins = teamInfo['record']['overall']['wins']

        # This should be empty for football, but some fantasy baseball matchups are longer than 1 week and need to be scaled down
        # Fill this in as needed
        self.scoreMultipliers = {
            1:7/11,
            14:7/10
        }

    def getMetadata(self, league):
        self.getMatchups(league)
        self.averageScore = self.getAverageScore(league.currMatchupsPlayed)
        self.getOpponents()

    def getMatchups(self, league):
        for matchup in league.schedule:
            if matchup['away']['teamId'] == self.id or matchup['home']['teamId'] == self.id:
                self.matchups.append(matchup)

    def getAverageScore(self, currMatchupsPlayed):
        totalPoints = 0
        for matchup in self.matchups:
            if matchup['matchupPeriodId'] > currMatchupsPlayed:
                break
            if matchup['away']['teamId'] == self.id:
                try:
                    totalPoints += self.scoreMultipliers[matchup['matchupPeriodId']]*matchup['away']['totalPoints']
                except KeyError:
                    totalPoints += matchup['away']['totalPoints']
            elif matchup['home']['teamId'] == self.id:
                try:
                    totalPoints += self.scoreMultipliers[matchup['matchupPeriodId']]*matchup['home']['totalPoints']
                except KeyError:
                    totalPoints += matchup['home']['totalPoints']
            else:
                raise Exception('Failed sanity check. getMatchups returned a matchup team {} isn\'t in'.format(self.id))
        return totalPoints/currMatchupsPlayed

    def getOpponents(self):
        for matchup in self.matchups:
            if matchup['away']['teamId'] == self.id:
                self.opponents.append(matchup['home']['teamId'])
            elif matchup['home']['teamId'] == self.id:
                self.opponents.append(matchup['away']['teamId'])
            else:
                raise Exception('Failed sanity check. getMatchups returned a matchup team {} isn\'t in'.format(self.id))