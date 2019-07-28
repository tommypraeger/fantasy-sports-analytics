import re

import requests

import analysis
from team import Team

sportMap = {
    'football':'ffl',
    'baseball':'flb'
}

class League(object):
    def __init__(self, league_info):
        '''League metadata and auth info'''
        self.name = ''
        self.sport = league_info['sport']
        self.id = league_info['league_id']
        self.year = league_info['year']
        self.swid = league_info['swid']
        self.espn_s2 = league_info['espn_s2']
        self.schedule = []
        self.teams = []
        self.team_map = {}
        self.curr_matchups_played = 0
        self.total_matchups = 0
        self.num_teams = 0

    def fetch_league(self):
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
            resp_json = resp.json()

            self.name = resp_json['settings']['name']
            self.schedule = resp_json['schedule']
            self.total_matchups = resp_json['settings']['scheduleSettings']['matchupPeriodCount']
            self.curr_matchups_played = self.get_curr_matchups_played(resp_json['status']['currentMatchupPeriod'])

            # Can't do analysis with less than 2 games played
            if self.curr_matchups_played < 2:
                raise Exception("There must have been at least 2 matchups played already.")

            teams = resp_json['teams']
            self.num_teams = len(teams)
            for team in teams:
                team_obj = Team(team)
                team_obj.get_metadata(self)
                self.teams.append(team_obj)
                self.team_map[team['id']] = team_obj
            for team in self.teams:
                team.get_opponents(self)
            self.teams.sort(key=lambda team: re.sub(r'[^\w\s]', '', team.name))

    def perform_team_analysis(self):
        '''Perform all the statistics and analysis for each team'''
        for team in self.teams:
            self.analyze_team(team)

    def analyze_team(self, team):
        '''Calculate win expectancies'''
        analysis.get_win_likelihoods(self, team)
        analysis.get_win_total_probs(self, team)
        analysis.get_future_win_total_probs(self, team)

    def get_team(self, teamId):
        '''Return a team object given a team id'''
        return self.team_map[teamId]

    def get_curr_matchups_played(self, curr_matchup_period):
        '''Get current number of matchups played'''
        if curr_matchup_period > self.total_matchups:
            return self.total_matchups
        return curr_matchup_period - 1
