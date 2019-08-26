# flask stuff
from flask import Flask, jsonify
from flask_restful import (
    Resource,
    Api,
    reqparse
)
import urllib.parse

from app.analysis.fantasy_league_analysis.league import League
from app.analysis.fantasy_league_analysis.export import export_league, export_team

app = Flask(__name__)
api = Api(app)


class FantasyLeagueAnalysis(Resource):
    def get(self):
        fields = {
            'platform': 'espn',
            'sport': 'baseball',
            'league_id': 58769671,
            'year': 2019,
            'swid': '{3912796D-CF3D-4297-ABA6-B5BF3051E861}',
            'espn_s2': 'AEARdPEFgZM61MMlwMZpD9S1%2BwZEES5M4ZSlJza2SqJtxziTh4BEf61305pT7vVBT833l%2BfNxGtcs%2BXilo5EPuVYVgjC7%2BxI%2F3Vw%2BX8zFc84XevaowFhMjWilUQp%2FyBqGW2cpQUDH%2BfOi0kQEAbwEsMmUuQKuTM7GuADcujUnkfm698xGK%2F0LDY7IxVXi%2FcPMuRwGbSXSVdcFOKS82XyeYOA0LSXD6T1Q0VitNSlFdTGlzIzv631ZvbL8vLyxB%2B1rgl71UZV7CccnzU4cnidMcWh'
        }
        try:
            # Argument reqs
            # ESPN: sport, league_id, year, (espn_s2, swid for private leagues)
            # Sleeper: league_id

            parser = reqparse.RequestParser()
            parser.add_argument('platform',
                                type=str,
                                help='Platform must be a string',
                                required=True)
            parser.add_argument('sport', type=str, help='Sport must be a string')
            parser.add_argument('league_id', required=True)
            parser.add_argument('year')
            # ESPN-specific for private leagues
            parser.add_argument('espn_s2', type=str, help='espn_s2 must be a string')
            parser.add_argument('swid', type=str, help='SWID must be a string')

            fields = parser.parse_args()
            league = League(fields)
            league.teams.sort(
                key=lambda team: sum(team.win_likelihoods[:league.curr_matchups_played]),
                reverse=True
            )

            league_export = {
                'league': export_league(league),
                'teams': [export_team(team) for team in league.teams]
            }
        except Exception as e:
            return jsonify({'Error': str(e)})

        return jsonify(league_export)


api.add_resource(FantasyLeagueAnalysis, '/api/v1/fantasy_league_analysis')

if __name__ == '__main__':
    app.run(debug=True)
