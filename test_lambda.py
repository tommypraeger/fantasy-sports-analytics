import json
import unittest
import application


# Run like this: `python3 -m unittest test_lambda.py`
# Must be in venv to run (first run `source venv/bin/activate`)
class TestLambda(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.test_league = lambda result: (
            self.assertIn('league', result),
            self.assertIn('teams', result),
            self.assertIsInstance(result['league'], dict),
            self.assertIsInstance(result['teams'], list),
            self.assertGreater(len(result['teams']), 0),
            self.assertIsInstance(result['teams'][0], dict)
        )
        self.league_analysis = 'league-analysis'
        self.wakeup_league_analysis = 'wakeup-league-analysis'
        self.espn = 'espn'
        self.football = 'football'
        self.baseball = 'baseball'
        self.basketball = 'basketball'
        self.espn_football_league_id = '264572'
        self.old_espn_league_id = '1667842'
        self.baseball_league_id = '58769671'
        self.basketball_league_id = '1436496933'
        self.espn_s2 = 'AEA%2BWys%2B%2B93TnQkDxRuqJNTTBJzJflHeTboyroHLq12Z0Idl%2BFQP7fM4VLCmOa7U1UR0kVCKtmdkblitAYFLbHq7aA7SOXOQA%2BaXzCOXn6LhjMwfynESSpqOLykGymZfvf%2F4AfsVDm2fNa19fX%2BtH6xLnOcWv%2BAFBPiuERAhsACC0G05LNFgIaOxtmq42848gvH0mUJa6SUz1aA%2FI%2FExEBtEbQyQUQK2uuozIkYwMch2IOQ47AV0pw5Vr8%2FKkV4dwkm7g7HO1JnGjvgmVaddNid0BZdLtTGPjrv9n%2B0nK8uQew%3D%3D'
        self.fake_platform = 'notespn'
        self.fake_league_id = 'fakeleagueid'
        self.fake_sport = 'foosball'
        self.fake_espn_s2 = 'fakes2'
        self.sleeper = 'sleeper'
        self.sleeper_league_id = '607346879230963712'
        self.event_map = {
            'wakeupleagueanalysis': {
                'method': self.wakeup_league_analysis,
            },
            'badplatform': {
                'method': self.league_analysis,
                'sport': self.football,
                'platform': self.fake_platform,
                'leagueId': self.espn_football_league_id,
                'year': '2020',
                'espnS2': self.espn_s2
            },
            'espnfootball': {
                'method': self.league_analysis,
                'sport': self.football,
                'platform': self.espn,
                'leagueId': self.espn_football_league_id,
                'year': '2020',
                'espnS2': self.espn_s2
            },
            'espnbadyear': {
                'method': self.league_analysis,
                'sport': self.football,
                'platform': self.espn,
                'leagueId': self.old_espn_league_id,
                'year': '2016',
                'espnS2': self.espn_s2
            },
            'espnbadsport': {
                'method': self.league_analysis,
                'sport': self.fake_sport,
                'platform': self.espn,
                'leagueId': self.espn_football_league_id,
                'year': '2020',
                'espnS2': self.espn_s2
            },
            'espnbadleagueid': {
                'method': self.league_analysis,
                'sport': self.football,
                'platform': self.espn,
                'leagueId': self.fake_league_id,
                'year': '2020',
                'espnS2': self.espn_s2
            },
            'espnbads2': {
                'method': self.league_analysis,
                'sport': self.football,
                'platform': self.espn,
                'leagueId': self.espn_football_league_id,
                'year': '2020',
                'espnS2': self.fake_espn_s2
            },
            'espnbaseball': {
                'method': self.league_analysis,
                'sport': self.baseball,
                'platform': self.espn,
                'leagueId': self.baseball_league_id,
                'year': '2019',
                'espnS2': self.espn_s2
            },
            'espnbasketball': {
                'method': self.league_analysis,
                'sport': self.basketball,
                'platform': self.espn,
                'leagueId': self.basketball_league_id,
                'year': '2021',
                'espnS2': self.espn_s2
            },
            'sleeper': {
                'method': self.league_analysis,
                'platform': self.sleeper,
                'leagueId': self.sleeper_league_id
            },
            'sleeperbadleagueid': {
                'method': self.league_analysis,
                'platform': self.sleeper,
                'leagueId': self.fake_league_id
            }
        }
        self.error_strings = {
            'badplatform': f"'{self.fake_platform}' is not a valid Platform",
            'espnbadyear': ('Failed to fetch league data. '
                            'Check your league ID and ESPN S2 cookie if needed.'),
            'espnbadsport': f'{self.fake_sport} is not a valid sport for ESPN.',
            'espnbadleagueid': ('Failed to fetch league data. '
                                'Check your league ID and ESPN S2 cookie if needed.'),
            'espnbads2': ('Failed to fetch league data. '
                          'Check your league ID and ESPN S2 cookie if needed.'),
            'sleeperbadleagueid': ('Failed to fetch league data. '
                                   'Check your league ID.')
        }

    def test_wakeup(self):
        result = application.handler({
            "body": json.dumps(self.event_map['wakeupleagueanalysis'])
        }, {})
        self.assertEqual(result, "{}")

    def test_bad_platform(self):
        error_events = ['badplatform']
        for event in error_events:
            result = application.handle_league_analysis(self.event_map[event])
            self.assertEqual(result['errorMessage'], self.error_strings[event])

    def test_espn(self):
        error_events = ['espnbadyear', 'espnbadsport', 'espnbadleagueid', 'espnbads2']
        for event in error_events:
            result = application.handle_league_analysis(self.event_map[event])
            self.assertEqual(result['errorMessage'], self.error_strings[event])
        result = application.handle_league_analysis(self.event_map['espnfootball'])
        self.test_league(result)
        result = application.handle_league_analysis(self.event_map['espnbaseball'])
        self.test_league(result)
        result = application.handle_league_analysis(self.event_map['espnbasketball'])
        self.test_league(result)

    def test_sleeper(self):
        error_events = ['sleeperbadleagueid']
        for event in error_events:
            result = application.handle_league_analysis(self.event_map[event])
            self.assertEqual(result['errorMessage'], self.error_strings[event])
        result = application.handle_league_analysis(self.event_map['sleeper'])
        self.test_league(result)


if __name__ == "__main__":
    unittest.main()
