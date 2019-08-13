from analysis import std_dev
from league import League


class Team(object):
    def __init__(self, team_info: dict) -> None:
        '''Team metadata'''

        self.name = f'{team_info["location"].strip()} {team_info["nickname"].strip()}'
        self.id = team_info['id']
        self.scores = []
        self.average_score = 0
        self.score_std_dev = 0
        self.matchups = []
        self.wins = team_info['record']['overall']['wins']
        self.opponents = []
        self.opponent_average_scores = []
        self.opponent_std_devs = []
        self.win_likelihoods = []
        self.win_total_probs = []
        self.future_win_total_probs = []

    def get_metadata(self, league: League) -> None:
        '''Calculate team-specific score data'''

        self.get_matchups(league)
        self.average_score = self.get_average_score(league.curr_matchups_played)
        self.score_std_dev = self.get_adj_std_dev(league.curr_matchups_played)

    def get_matchups(self, league: League) -> None:
        '''Get matchups for a team'''

        for matchup_json in league.schedule:
            # Only get regular season matchups
            if matchup_json['matchupPeriodId'] > league.total_matchups:
                break
            if (matchup_json['away']['teamId'] == self.id
                    or matchup_json['home']['teamId'] == self.id):
                matchup = {}
                matchup['week'] = matchup_json['matchupPeriodId']
                matchup['score'] = self.get_score(matchup_json,
                                                  league.curr_matchups_played,
                                                  league.score_multipliers)
                matchup['opponent'] = self.get_opponent(matchup_json)
                self.matchups.append(matchup)

    def get_score(self,
                  matchup: dict,
                  curr_matchups_played: int,
                  score_multipliers: dict) -> float or None:
        '''Get score for a matchup'''

        # No score for future games
        if matchup['matchupPeriodId'] > curr_matchups_played:
            return None

        # Check if team is home or away
        if matchup['away']['teamId'] == self.id:
            score = (score_multipliers[matchup['matchupPeriodId']]
                     * matchup['away']['totalPoints'])
        elif matchup['home']['teamId'] == self.id:
            score = (score_multipliers[matchup['matchupPeriodId']]
                     * matchup['home']['totalPoints'])
        else:
            raise Exception('Failed sanity check. '
                            f'getMatchups returned a matchup team {self.id} isn\'t in')

        score = round(score, 2)
        self.scores.append(score)
        return score

    def get_opponent(self, matchup: dict) -> str:
        '''Get opponent for a matchup'''

        if matchup['away']['teamId'] == self.id:
            return matchup['home']['teamId']
        elif matchup['home']['teamId'] == self.id:
            return matchup['away']['teamId']
        else:
            raise Exception('Failed sanity check. '
                            f'getMatchups returned a matchup team {self.id} isn\'t in')

    def get_opponents(self, league: League) -> None:
        '''Get opponents for a team'''

        self.opponents = [
            league.get_team(matchup['opponent'])
            for matchup in self.matchups
        ]

    def get_average_score(self, curr_matchups_played: int) -> float:
        '''Get average score for a team'''

        total_score = 0
        for matchup in self.matchups[:curr_matchups_played]:
            total_score += matchup['score']
        return round(total_score / curr_matchups_played, 2)

    # I slightly increase standard deviation to reduce the confidence of the predictions
    # Fantasy scores aren't really random variables,
    # so I figured I should make the predictions slightly less confident
    # Adj std dev = std dev * (n+1)/n, where n is the number of games played
    def get_adj_std_dev(self, curr_matchups_played: int) -> float:
        '''Get adjusted standard deviation of score for a team'''

        adj_std_dev = (std_dev(self.scores)
                       * (curr_matchups_played + 1)
                       / curr_matchups_played)
        return round(adj_std_dev, 2)