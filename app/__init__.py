# flask stuff
from flask import Flask, jsonify
from flask_restful import (
    Resource,
    Api,
    reqparse,
    abort
)

from app.analysis.fantasy_league_analysis.league import League
from app.analysis.fantasy_league_analysis.export import export_league, export_team

app = Flask(__name__)
api = Api(app)


class FantasyLeagueAnalysis(Resource):
    def get(self):
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
            # parser.add_argument('swid', type=str, help='SWID must be a string')

            fields = parser.parse_args()
            league = League(fields)

            league_export = {
                'league': export_league(league),
                'teams': [export_team(team) for team in league.teams]
            }
        except Exception as e:
            print(e)
            abort(400, message=str(e))

        return jsonify(league_export)


api.add_resource(FantasyLeagueAnalysis, '/api/v1/fantasy_league_analysis')

if __name__ == '__main__':
    app.run(debug=True)
