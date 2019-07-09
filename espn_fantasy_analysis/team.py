class Team(object):
    def __init__(self, teamInfo):
        self.name = '{} {}'.format(teamInfo['location'].strip(), teamInfo['nickname'].strip())
        self.id = teamInfo['id']
        self.scores = []
        self.averageScore = 0