import unittest
import application


# Run like this: $ python3 -m unittest test_lambda.py
class TestLambda(unittest.TestCase):
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
        self.espn_football_league_id = '264572'
        self.old_espn_league_id = '1667842'
        self.baseball_league_id = '58769671'
        self.espn_s2 = 'AEBZdjDCIUphHU4R2CzpqU0nyreubFNqzmP%2FCzWFwfL%2BCLG%2BxVjYoVuW6poxYdqU8gT3F4ni3GtVrj%2ByB1lzMgSirVPEsly0STsdhOY8yfiPvB4opi7xjJs7x7y2al5hSKwq4L6xHrX%2FBQIOeG2GNUZ0U1ZyOiWFkOlCwpDxZ8wbofUb2wwbj0zicjYcdrnCGF0VT5dxpZZm0jOsvMbMREiAUk8DJkizayo%2FSFPzsAoQvcqSgl9nuciiD3pKwnt8RiXye810jW42eswyhhBN18Kr'
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
                'year': '2020',
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
            'badplatform': f'{self.fake_platform} is not a valid platform.',
            'espnbadyear': ('It looks like the league didn\'t take place in 2020. '
                            'Make sure the league ID, year, and sport are correct.'),
            'espnbadsport': f'{self.fake_sport} is not a valid sport for ESPN.',
            'espnbadleagueid': ('Something went wrong fetching your league. '
                                'Make sure the league ID, year, and sport are correct.'),
            'espnbads2': ('The request to access your league was unauthorized. '
                          'Make you provide the espn_s2 cookie if your league is private.'),
            'sleeperbadleagueid': ('Something went wrong fetching your league. '
                                   'Make sure your league ID is correct.')
        }

    def test_wakeup(self):
        result = application.handler(self.event_map['wakeupleagueanalysis'], {})
        self.assertEqual(result, {})

    def test_bad_platform(self):
        error_events = ['badplatform']
        for event in error_events:
            result = application.handler(self.event_map[event], {})
            self.assertEqual(result['errorMessage'], self.error_strings[event])

    def test_espn(self):
        error_events = ['espnbadyear', 'espnbadsport', 'espnbadleagueid', 'espnbads2']
        for event in error_events:
            result = application.handler(self.event_map[event], {})
            self.assertEqual(result['errorMessage'], self.error_strings[event])
        result = application.handler(self.event_map['espnfootball'], {})
        self.test_league(result)
        result = application.handler(self.event_map['espnbaseball'], {})
        self.test_league(result)

    def test_sleeper(self):
        error_events = ['sleeperbadleagueid']
        for event in error_events:
            result = application.handler(self.event_map[event], {})
            self.assertEqual(result['errorMessage'], self.error_strings[event])
        result = application.handler(self.event_map['sleeper'], {})
        self.test_league(result)

if __name__ == "__main__":
    unittest.main()
