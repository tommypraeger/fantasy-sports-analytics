import requests
from team import Team

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
        self.teamMap = {}
        self.currMatchupAmt = 0
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
            # Reset these in this called multiple times for some reason
            self.teams = []
            self.teamMap = {}

            # Convert returned value to JSON
            respJson = resp.json()

            # Set the schedule dictionary
            self.schedule = respJson['schedule']

            # Fill the teams array with Team objects
            # Also create a map from ESPN's internal team id to team object
            teams = respJson['teams']
            for team in teams:
                teamObj = Team(team)
                self.teams.append(teamObj)
                self.teamMap[team['id']] = teamObj
            
            # Set some variables
            self.numTeams = len(teams)
            self.totalMatchups = respJson['settings']['scheduleSettings']['matchupPeriodCount']
            self.currMatchupAmt = self.getCurrMatchupAmt()

    def getCurrMatchupAmt(self):
        '''Get current number of matchups played'''
        for matchup in self.schedule:
            # Current and future matchups have the winner field as UNDECIDED
            if matchup['winner'] != 'UNDECIDED':
                continue
            return matchup['matchupPeriodId'] - 1
