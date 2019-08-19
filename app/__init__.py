# flask stuff
from flask import Flask, jsonify
from flask_restful import (
    Resource,
    Api,
    reqparse
)

from .analysis.fantasy_league_analysis.league import League
from .analysis.fantasy_league_analysis.export import export_league, export_team

app = Flask(__name__)
api = Api(app)


class FantasyLeagueAnalysis(Resource):
    def get(self):
        print('Fetching league data...')
        fields = {
            'sport': 'baseball',
            'league_id': 58769671,
            'year': 2019,
            'swid': '{3912796D-CF3D-4297-ABA6-B5BF3051E861}',
            'espn_s2': 'AEARdPEFgZM61MMlwMZpD9S1%2BwZEES5M4ZSlJza2SqJtxziTh4BEf61305pT7vVBT833l%2BfNxGtcs%2BXilo5EPuVYVgjC7%2BxI%2F3Vw%2BX8zFc84XevaowFhMjWilUQp%2FyBqGW2cpQUDH%2BfOi0kQEAbwEsMmUuQKuTM7GuADcujUnkfm698xGK%2F0LDY7IxVXi%2FcPMuRwGbSXSVdcFOKS82XyeYOA0LSXD6T1Q0VitNSlFdTGlzIzv631ZvbL8vLyxB%2B1rgl71UZV7CccnzU4cnidMcWh'
        }
        league = League(fields)
        league.fetch_league()

        print('Doing calculations...')
        league.perform_team_analysis()
        league.teams.sort(key=lambda team: sum(team.win_likelihoods[:league.curr_matchups_played]),
                          reverse=True)

        print('Exporting data to html...')
        league_export = {
            'league': export_league(league),
            'teams': [export_team(team, league) for team in league.teams]
        }

        return jsonify(league_export)


api.add_resource(FantasyLeagueAnalysis, '/api/v1/fantasy_league_analysis')

if __name__ == '__main__':
        app.run(debug=True)
