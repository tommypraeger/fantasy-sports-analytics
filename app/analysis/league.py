import re

import requests

import analysis
from team import Team

sportMap = {
    'football': 'ffl',
    'baseball': 'flb'
}


class League(object):
    def __init__(self, league_info: dict):
        '''League metadata and auth info'''

        self.name = ''
        self.sport = league_info['sport'].lower()
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
        self.score_multipliers = {}

    def fetch_league(self) -> None:
        '''Load league and set metadata for league and teams'''

        # Necessary ESPN API URLs
        url = (f'https://fantasy.espn.com/apis/v3/games/{sportMap[self.sport]}'
               f'/seasons/{self.year}/segments/0/leagues/{self.id}'
               '?view=mMatchupScore&view=mStatus&view=mSettings&view=mTeam&view=modular&view=mNav')
        matchup_url = (f'https://fantasy.espn.com/apis/v3/games/{sportMap[self.sport]}'
                       f'/seasons/{self.year}/segments/0/leagues/{self.id}?view=mMatchup')

        # Cookies needed for authentication
        cookies = {
            'SWID': self.swid,
            'espn_s2': self.espn_s2
        }

        # Make request and check if it succeeds
        resp = requests.get(url, cookies=cookies)
        matchup_resp = requests.get(matchup_url, cookies=cookies)
        if resp.status_code != 200 or matchup_resp.status_code != 200:
            raise Exception('401: Unauthorized. Did you forget to set the SWID and/or espn_s2?')
        else:
            resp_json = resp.json()
            matchup_json = matchup_resp.json()

            self.name = resp_json['settings']['name']
            self.schedule = resp_json['schedule']
            self.total_matchups = resp_json['settings']['scheduleSettings']['matchupPeriodCount']
            self.curr_matchups_played = self.get_curr_matchups_played(
                resp_json['status']['currentMatchupPeriod']
            )
            self.get_score_multipliers(matchup_json)

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

            # Need other team data to be complete before this can be done
            for team in self.teams:
                team.get_opponents(self)

    def get_score_multipliers(self, matchup_json: dict) -> None:
        '''Get score adjustments for matchups that are longer than usual'''

        # All football leagues have consistent scoring periods
        if self.sport == 'football':
            for week in range(1, self.curr_matchups_played + 1):
                self.score_multipliers[week] = 1

        # Mapping of how many scoring periods (active days in fantasy baseball) are in each matchup
        scoring_period_count = {}
        for matchup in matchup_json['schedule']:
            if matchup['matchupPeriodId'] > self.curr_matchups_played:
                # Can't check future matchups
                break
            if matchup['matchupPeriodId'] in scoring_period_count:
                continue
            scoring_period_count[matchup['matchupPeriodId']] = (
                len(matchup['away']['pointsByScoringPeriod'])
            )

        # Find most frequent number of scoring periods in a matchup
        usual_scoring_period_count = max(set(scoring_period_count.values()),
                                         key=list(scoring_period_count.values()).count)

        # Multiplier determined how to change a score to normalize it with the average
        # e.g. an 11-day matchup when average is 7 days would have its score multiplied by 7/11
        # Matchups of regular length have multipliers of one
        for matchup_period in scoring_period_count:
            self.score_multipliers[matchup_period] = (
                usual_scoring_period_count / scoring_period_count[matchup_period]
            )

    def perform_team_analysis(self) -> None:
        '''Perform all the statistics and analysis for each team'''

        for team in self.teams:
            self.analyze_team(team)

    def analyze_team(self, team: Team) -> None:
        '''Calculate win expectancies'''

        analysis.get_win_likelihoods(self, team)
        analysis.get_win_total_probs(self, team)
        analysis.get_future_win_total_probs(self, team)

    def get_team(self, teamId: int) -> Team:
        '''Return a team object given a team id'''

        return self.team_map[teamId]

    def get_curr_matchups_played(self, curr_matchup_period: int) -> int:
        '''Get current number of matchups played'''

        if curr_matchup_period > self.total_matchups:
            return self.total_matchups
        return curr_matchup_period - 1
