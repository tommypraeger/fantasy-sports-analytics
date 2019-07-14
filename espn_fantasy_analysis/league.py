import requests
from team import Team
import analysis

sportMap = {
    'football':'ffl',
    'baseball':'flb'
}

class League(object):
    def __init__(self, leagueInfo):
        '''League metadata and auth info'''
        self.sport = leagueInfo['sport']
        self.id = leagueInfo['leagueId']
        self.year = leagueInfo['year']
        self.swid = leagueInfo['swid']
        self.espn_s2 = leagueInfo['espn_s2']
        self.schedule = []
        self.teams = []
        self.teamMap = {}
        self.currMatchupsPlayed = 0
        self.totalMatchups = 0
        self.numTeams = 0

    def fetchLeague(self):
        '''Load league and set metadata for league and teams'''
        # ESPN's API URL
        url = 'https://fantasy.espn.com/apis/v3/games/{}/seasons/{}/segments/0/leagues/{}?view=mMatchupScore&view=mStatus&view=mSettings&view=mTeam&view=modular&view=mNav'.format(sportMap[self.sport],self.year,self.id)
        
        # Cookies needed for authentication
        cookies = {
            'SWID':self.swid,
            'espn_s2':self.espn_s2
        }

        # Make request and check if it succeeds
        resp = requests.get(url, cookies=cookies)
        if resp.status_code != 200:
            raise Exception('Error 401: Unauthorized. Did you forget to set the SWID and/or espn_s2?')
        else:
            # Convert returned value to JSON
            respJson = resp.json()

            # Set the schedule dictionary
            self.schedule = respJson['schedule']

            # Set some metadata variables
            self.totalMatchups = respJson['settings']['scheduleSettings']['matchupPeriodCount']
            self.currMatchupsPlayed = self.getCurrMatchupsPlayed()

            # Can't do analysis with less than 2 games played
            if self.currMatchupsPlayed < 2:
                raise Exception("There must have been at least 2 matchups played already.")

            # Fill in team metadata
            # Also create a map from ESPN's internal team id to team object
            teams = respJson['teams']
            self.numTeams = len(teams)
            for team in teams:
                teamObj = Team(team)
                Team.getMetadata(teamObj, self)
                self.teams.append(teamObj)
                self.teamMap[team['id']] = teamObj

    def performTeamAnalysis(self):
        '''Perform all the statistics and analysis for each team'''
        for team in self.teams:
            self.analyzeTeam(team)
            print(team.name, team.wins, team.averageScore, team.scoreStdDev, team.matchups, sep='\n', end='\n---------\n')

    def analyzeTeam(self, team):
        '''Calculate win expectancies'''
        analysis.getWinLikelihoods(self, team)
        analysis.getWinTotalProbs(self, team)

    def performLeagueAnalysis(self):
        '''Aggregate team analysis for league page'''
        pass

    def getTeam(self, teamId):
        '''Return a team object given a team id'''
        return self.teamMap[teamId]

    def getCurrMatchupsPlayed(self):
        '''Get current number of matchups played'''
        for matchup in self.schedule:
            # Current and future matchups have the winner field as UNDECIDED
            if matchup['winner'] != 'UNDECIDED':
                continue
            return matchup['matchupPeriodId'] - 1
