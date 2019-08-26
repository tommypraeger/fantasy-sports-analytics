from importlib import import_module


class League(object):
    def __init__(self, league_info: dict):
        '''League metadata and auth info'''

        # Import correct platform API wrapper to import
        platform_path = f'app.analysis.fantasy_league_analysis.fetch_{league_info["platform"]}'
        platform = import_module(platform_path)

        self.sport = ''
        self.id = ''
        self.year = ''
        self.swid = ''
        self.espn_s2 = ''
        self.name = ''
        self.schedule = []
        self.teams = []
        self.team_map = {}
        self.curr_matchups_played = 0
        self.total_matchups = 0
        self.num_teams = 0
        self.score_multipliers = {}

        platform.fetch_league(self, league_info)
        platform.perform_team_analysis(self)

        self.teams.sort(
            key=lambda team: sum(team.win_likelihoods[:self.curr_matchups_played]),
            reverse=True
        )

    def get_team(self, teamId: int):
        '''Return a team object given a team id'''

        return self.team_map[teamId]
